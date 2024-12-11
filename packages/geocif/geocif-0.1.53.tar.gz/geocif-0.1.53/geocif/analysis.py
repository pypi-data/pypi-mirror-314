import ast
import os
import sqlite3
import warnings
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import arrow as ar
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import palettable as pal
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from geocif import logger as log
from geocif import utils
from .viz import plot

warnings.simplefilter(action="ignore", category=FutureWarning)


@dataclass
class Geoanalysis:
    path_config_files: List[Path] = field(default_factory=list)
    logger: log = None
    parser: ConfigParser = field(default_factory=ConfigParser)

    def __post_init__(self):
        self.country: str = None
        self.countries: list = None
        self.crop: str = None
        self.table: str = None
        self.forecast_season: int = None
        self.model_names: list = []
        self.df_analysis: pd.DataFrame = None
        self.lag_yield_as_feature: bool = None
        self.number_lag_years: int = None
        self.all_seasons_with_yield: list = None

        self.dir_out = Path(self.parser.get("PATHS", "dir_output"))
        self._date = ar.utcnow().to("America/New_York")
        self.today = self._date.format("MMMM_DD_YYYY")

        self.dir_ml = self.dir_out / "ml"
        self.dir_db = self.dir_ml / "db"
        self.dir_analysis = self.dir_ml / "analysis" / self.today
        os.makedirs(self.dir_db, exist_ok=True)
        os.makedirs(self.dir_analysis, exist_ok=True)

        self.db_forecasts = self.parser.get("DEFAULT", "db")
        self.db_path = self.dir_db / self.db_forecasts

        dir_input = Path(self.parser.get("PATHS", "dir_input"))
        self.dir_shapefiles = dir_input / "Global_Datasets" / "Regions" / "Shps"

    def table_exists(self, db_path, table_name):
        # Create a connection to the SQLite database
        with sqlite3.connect(db_path) as con:
            # Create a cursor object using the cursor() method
            cursor = con.cursor()

            # Define the query to find the table
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"

            # Execute the prepared query passing the table_name as a parameter
            cursor.execute(query, (table_name,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the cursor
            cursor.close()

        # Return True if a result is found, False otherwise
        return result is not None

    def query(self):
        self.logger.info(f"Query {self.country} {self.crop}")
        con = sqlite3.connect(self.db_path)

        # Read from database, where country and crop match
        query = "SELECT * FROM " + self.table
        try:
            self.df_analysis = pd.read_sql_query(query, con)

            # Select just Country and Crop
            self.df_analysis = self.df_analysis[
                (self.df_analysis["Country"] == self.country)
                & (self.df_analysis["Crop"] == self.crop)
                & (self.df_analysis["Model"] == self.model)
            ]
        except Exception as e:
            pass

        con.commit()
        con.close()

    def annual_metrics(self, df):
        """
        Compute metrics for a given dataframe
        :param df: dataframe containing Observed and Forecast data
        """
        import scipy.stats
        from sklearn.metrics import mean_squared_error, mean_absolute_error

        if len(df) < 3:
            return pd.Series()

        # Compute metrics
        rmse = np.sqrt(mean_squared_error(df[self.observed], df[self.predicted]))
        nse = utils.nse(df[self.observed], df[self.predicted])
        r2 = scipy.stats.pearsonr(df[self.observed], df[self.predicted])[0] ** 2
        mae = mean_absolute_error(df[self.observed], df[self.predicted])
        mape = utils.mape(df[self.observed], df[self.predicted])
        pbias = utils.pbias(df[self.observed], df[self.predicted])

        # Return as a dictionary
        dict_results = {
            "Root Mean Square Error": rmse,
            "Nash-Sutcliff Efficiency": nse,
            "$r^2$": r2,
            "Mean Absolute Error": mae,
            "Mean Absolute\nPercentage Error": mape,
            "Percentage Bias": pbias,
        }

        return pd.Series(dict_results)

    def regional_metrics(self, df):
        # Compute MAPE for each region, compute within this function
        # Compute metrics

        actual, predicted = df[self.observed], df[self.predicted]
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        return pd.Series({"Mean Absolute Percentage Error": mape})

    def add_stage_information(self, df):
        """
        Create a new column called Dekad which contains the last dekad
        :param df: dataframe containing the column Stages for which we will compute Dekad information
        """
        for i, row in df.iterrows():
            # Get the latest stage
            stage = row["Stage Name"].split("-")[0]
            df.loc[i, "Date"] = stage

        return df

    def select_top_N_years(self, group, N=5):
        return group.nsmallest(N, "Mean Absolute Percentage Error")

    def analyze(self):
        self.logger.info(f"Analyze {self.country} {self.crop}")

        df = self._clean_data()
        if df.empty:
            return pd.DataFrame(), pd.DataFrame()

        df_metrics = self._compute_metrics(df)
        df_metrics = self._process_metrics(df_metrics)

        self._plot_metrics(df_metrics)
        df_regional_metrics_by_year = self._compute_regional_metrics(
            df, by="Harvest Year"
        )
        df_regional_metrics_by_year = self._select_top_years(
            df_regional_metrics_by_year
        )
        df_regional_metrics = self._average_mape(df_regional_metrics_by_year)

        self._store_results(
            df_metrics, df_regional_metrics, df_regional_metrics_by_year
        )
        df_national_yield = self._compute_national_yield(df)
        self._plot_national_yield(df_national_yield)
        self._plot_regional_yield_scatter(df)

        return df_metrics, df_regional_metrics, df_national_yield

    def _clean_data(self):
        # Hack exclude 2012 if country == "illinois"
        if self.country == "illinois":
            self.df_analysis = self.df_analysis[
                self.df_analysis["Harvest Year"] != 2012
            ]
        # Remove rows with missing values in Observed Yield (tn per ha)
        return self.df_analysis.dropna(subset=["Observed Yield (tn per ha)"])

    def _compute_metrics(self, df):
        # For each Harvest Year, Stages combination, compute metrics
        df_metrics = (
            df.groupby(
                ["Country", "Model", "Harvest Year", "Stage Name", "Stage Range"]
            )
            .apply(self.annual_metrics)
            .reset_index()
        )

        # return df_metrics.pivot_table(
        #    index=["Country", "Model", "Harvest Year", "Stage Name", "Stage Range"],
        #    columns="level_5",
        #    values=0,
        # ).reset_index()
        return df_metrics

    def _process_metrics(self, df_metrics):
        # Assign each unique Stage Name a unique integer identifier
        df_metrics["Stage_ID"] = pd.Categorical(df_metrics["Stage Name"]).codes

        # Order by Harvest Year and Number Stages (ascending)
        df_metrics = df_metrics.sort_values(by=["Harvest Year", "Stage_ID"])

        # Add columns with the name of the country and crop
        df_metrics["Country"] = self.country
        df_metrics["Crop"] = self.crop

        # Add stage information for plotting
        return self.add_stage_information(df_metrics)

    def _plot_metrics(self, df_metrics):
        metrics = [
            "Root Mean Square Error",
            "$r^2$",
            "Mean Absolute Error",
            "Mean Absolute\nPercentage Error",
            "Percentage Bias",
        ]
        for metric in metrics:
            self.plot_metric(df_metrics, metric)

    def _compute_regional_metrics(self, df, by=None):
        cols = [
            "Country",
            "Region",
            "% of total Area (ha)",
            "Model",
            "Crop",
            "Stage Name",
            "Stage Range",
        ]

        if by:
            return df.groupby(cols + [by]).apply(self.regional_metrics).reset_index()
        else:
            return df.groupby(cols).apply(self.regional_metrics).reset_index()

    def _select_top_years(self, df_regional_metrics, top_N=-1):
        if top_N == -1:
            return df_regional_metrics
        else:
            return (
                df_regional_metrics.groupby(["Country", "Region"])
                .apply(lambda x: self.select_top_N_years(x, 10))
                .reset_index(drop=True)
            )

    def _average_mape(self, df_regional_metrics):
        cols = [
            "Country",
            "Region",
            "% of total Area (ha)",
            "Model",
            "Crop",
            "Stage Name",
            "Stage Range",
        ]
        return (
            df_regional_metrics.groupby(cols)["Mean Absolute Percentage Error"]
            .mean()
            .reset_index()
        )

    def _store_results(
        self, df_metrics, df_regional_metrics, df_regional_metrics_by_year
    ):
        # Create an index based on specific columns
        df_metrics.index = df_metrics.apply(
            lambda row: "_".join(
                [
                    str(row[col])
                    for col in [
                        "Country",
                        "Crop",
                        "Model",
                        "Harvest Year",
                        "Stage Name",
                    ]
                ]
            ),
            axis=1,
        )
        df_metrics.index.set_names(["Index"], inplace=True)

        df_regional_metrics.index = df_regional_metrics.apply(
            lambda row: "_".join(
                [
                    str(row[col])
                    for col in ["Country", "Region", "Model", "Crop", "Stage Name"]
                ]
            ),
            axis=1,
        )
        df_regional_metrics.index.set_names(["Index"], inplace=True)

        df_regional_metrics_by_year.index = df_regional_metrics_by_year.apply(
            lambda row: "_".join(
                [
                    str(row[col])
                    for col in [
                        "Country",
                        "Region",
                        "Model",
                        "Crop",
                        "Stage Name",
                        "Harvest Year",
                    ]
                ]
            ),
            axis=1,
        )
        df_regional_metrics_by_year.index.set_names(["Index"], inplace=True)

        # Format with 3 places after the decimal point
        df_metrics = df_metrics.round(3)
        df_regional_metrics = df_regional_metrics.round(3)
        df_regional_metrics_by_year = df_regional_metrics_by_year.round(3)

        # Store results in database
        with sqlite3.connect(self.db_path) as con:
            utils.to_db(self.db_path, "country_metrics", df_metrics)
            utils.to_db(self.db_path, "regional_metrics", df_regional_metrics)
            utils.to_db(
                self.db_path, "regional_metrics_by_year", df_regional_metrics_by_year
            )

            con.commit()

    def _compute_national_yield(self, df_region):
        # Define column names
        observed = "Observed Yield (tn per ha)"
        predicted = "Predicted Yield (tn per ha)"
        area_ha = "Area (ha)"

        df_tmp = df_region.copy()

        # Fill
        df_tmp[area_ha] = df_tmp.groupby("Country")[area_ha].transform(lambda x: x.fillna(x.median()))

        # Log that we are filling missing values with the median
        self.logger.info(
            f"Filling missing values in {area_ha} with the median for each country"
        )

        # Compute observed and predicted national yield by multiplying Yield (tn per ha) by Area (ha)
        df_tmp[observed] = df_tmp[observed] * df_tmp[area_ha]
        df_tmp[predicted] = df_tmp[predicted] * df_tmp[area_ha]

        # Group by Country and Harvest Year, then sum the National Yield and Area
        df_national_yield = (
            df_tmp.groupby(["Country", "Harvest Year"])
            .agg({observed: "sum", predicted: "sum", area_ha: "sum"})
            .reset_index()
        )

        # Compute observed and predicted yield per ha for each Harvest Year
        df_national_yield[observed] = (
            df_national_yield[observed] / df_national_yield[area_ha]
        )
        df_national_yield[predicted] = (
            df_national_yield[predicted] / df_national_yield[area_ha]
        )

        return df_national_yield

    def _plot_regional_yield_scatter(self, df):
        """
        Plot observed vs predicted yield for all regions and all years.
        """
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

        # Ensure 'Harvest Year' is numeric
        df["Harvest Year"] = pd.to_numeric(df["Harvest Year"], errors="coerce")

        # Extract data
        y_observed = df["Observed Yield (tn per ha)"]
        y_predicted = df["Predicted Yield (tn per ha)"]
        years = df["Harvest Year"]

        # Generate colors for years
        cmap = plt.cm.viridis  # Colormap for years
        norm = plt.Normalize(vmin=years.min(), vmax=years.max())  # Normalize years to colormap
        colors = [cmap(norm(year)) for year in years]

        # Create the plot
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 6))

            # Add gridlines
            ax.grid(True, linestyle="--", alpha=0.5)

            # Scatter plot with colors representing years
            scatter = ax.scatter(y_observed, y_predicted, color=colors, s=50)

            # Add 1:1 diagonal line
            max_yield = max(y_observed.max(), y_predicted.max()) * 1.25
            ax.plot([0, max_yield], [0, max_yield], color="gray", linestyle="--")

            # Calculate and display metrics
            rmse = np.sqrt(mean_squared_error(y_observed, y_predicted))
            mape = mean_absolute_percentage_error(y_observed, y_predicted)
            r2 = r2_score(y_observed, y_predicted)

            textstr = f"RMSE: {rmse:.2f} tn/ha\nMAPE: {mape:.2%}\n$r^2$: {r2:.2f}"
            ax.annotate(
                textstr,
                xy=(0.05, 0.95),
                xycoords="axes fraction",
                fontsize=12,
                verticalalignment="top",
            )

            # Set axis limits and labels
            ax.set_xlabel("Observed Yield (tn/ha)")
            ax.set_ylabel("Predicted Yield (tn/ha)")
            ax.set_xlim(0, max_yield)
            ax.set_ylim(0, max_yield)

            # Add colorbar for years
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = fig.colorbar(sm, ax=ax, aspect=50, pad=0.02)
            cbar.set_label("Harvest Year")

            # Set equispaced ticks for exactly 5 points
            ticks = np.linspace(years.min(), years.max(), 5, dtype=int)  # 5 equispaced ticks
            cbar.set_ticks(ticks)
            cbar.ax.set_yticklabels([str(tick) for tick in ticks])

            plt.tight_layout()

            # Save the plot
            fname = f"scatter_all_regions_{self.country}_{self.crop}.png"
            plt.savefig(self.dir_analysis / fname, dpi=250)
            plt.close()

    def _plot_national_yield(self, df_national_yield):
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

        # Ensure 'Harvest Year' is numeric
        df_national_yield["Harvest Year"] = pd.to_numeric(df_national_yield["Harvest Year"], errors="coerce")

        # Extract data
        x = df_national_yield["Harvest Year"]
        y_observed = df_national_yield["Observed Yield (tn per ha)"]
        y_predicted = df_national_yield["Predicted Yield (tn per ha)"]

        # Generate colors for years
        cmap = plt.cm.viridis  # Colormap for years
        norm = plt.Normalize(vmin=x.min(), vmax=x.max())  # Normalize years to colormap
        colors = [cmap(norm(year)) for year in x]

        # Create the plot
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 6))  # Explicitly define axes

            max_yield = max(y_observed.max(), y_predicted.max()) * 1.25

            # Add gridlines
            ax.grid(True, linestyle="--", alpha=0.5)

            # Scatter plot with uniform size and dynamic colors
            for year, obs, pred, color in zip(x, y_observed, y_predicted, colors):
                ax.scatter(obs, pred, color=color, s=50, label=year)

            # Add 1:1 diagonal line
            ax.plot([0, max_yield], [0, max_yield], color="gray", linestyle="--")

            # Calculate and display metrics
            rmse = np.sqrt(mean_squared_error(y_observed, y_predicted))
            mape = mean_absolute_percentage_error(y_observed, y_predicted)
            r2 = r2_score(y_observed, y_predicted)

            textstr = f"RMSE: {rmse:.2f} tn/ha\nMAPE: {mape:.2%}\nr²: {r2:.2f}"
            ax.annotate(
                textstr,
                xy=(0.05, 0.95),
                xycoords="axes fraction",
                fontsize=12,
                verticalalignment="top",
            )

            # Set axis limits and labels
            ax.set_xlabel("Observed Yield (tn/ha)")
            ax.set_ylabel("Predicted Yield (tn/ha)")
            ax.set_xlim(0, max_yield)
            ax.set_ylim(0, max_yield)

            # Add legend for years
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = fig.colorbar(sm, ax=ax, aspect=50, pad=0.02)  # Specify the axis explicitly
            cbar.set_label("Harvest Year")

            # Set equispaced ticks for exactly 5 points
            ticks = np.linspace(x.min(), x.max(), 5, dtype=int)  # 5 equispaced ticks
            cbar.set_ticks(ticks)
            cbar.ax.set_yticklabels([str(tick) for tick in ticks])

            plt.tight_layout()

            # Save the plot
            fname = f"scatter_{self.country}_{self.crop}.png"
            plt.savefig(self.dir_analysis / fname, dpi=250)
            plt.close()

    def get_historic_production(self):
        # Read in historic production data
        dir_output = Path(self.parser.get("PATHS", "dir_output"))
        dir_statistics = dir_output / "cei" / "indices" / self.method / "global"
        country = self.country.title().replace("_", " ")
        crop = self.crop.title().replace("_", " ")
        file = dir_statistics / f"{country}_{crop}_statistics_s1_{self.method}.csv"
        df_historic = pd.read_csv(file)

        df_historic = df_historic[["Region", "Harvest Year", "Yield (tn per ha)"]]

        # Drop rows with NaN values
        df_historic = df_historic.dropna()

        # Determine unique years
        years = df_historic["Harvest Year"].unique()

        # Subset dataframe to only include the last years of the dataset
        df_historic = df_historic[df_historic["Harvest Year"].isin(years[-5:])]

        # For each region, compute the % of the total production
        df_historic = (
            df_historic.groupby("Region")["Yield (tn per ha)"]
            .sum()
            .pipe(lambda x: x / x.sum() * 100)
            .to_frame(name="% of total Area (ha)")
            .reset_index()
        )
        # Find median yield for each region
        # df_historic = (
        #     df_historic.groupby("Region")["Yield (tn per ha)"]
        #     .median()
        #     .to_frame(name="Median Yield (tn per ha)")
        #     .reset_index()
        # )

        return df_historic

    def preprocess(self):
        if self.df_analysis.empty:
            return

        # Add a column called N year average that contains the average of the yield of the last 10 years
        # this will be the same for each dekad in any year
        df_lag_yield = self.df_analysis.copy()

        df_lag_yield = (
            df_lag_yield.groupby("Region")["Median Yield (tn per ha)"]
            .median()
            .reset_index()
        )
        df_lag_yield.columns = ["Region", f"{self.number_lag_years} year average"]

        self.df_analysis = self.df_analysis.merge(df_lag_yield, on="Region", how="left")

        df_historic = self.get_historic_production()
        self.df_analysis = self.df_analysis.merge(df_historic, on="Region", how="left")

        # Add a column called anomaly that is the ratio between the predicted yield and the N year average
        self.df_analysis["Anomaly"] = (
            self.df_analysis[self.predicted]
            * 100.0
            / self.df_analysis["Median Yield (tn per ha)"]
        )

        # Compute the yield from the last year
        # Add a column called Ratio Last Year that is the ratio between the predicted yield and the last year yield
        # self.df_analysis["Ratio Last Year"] = (
        #     self.df_analysis[self.predicted]
        #     * 100.0
        #     / self.df_analysis[f"Last Year Yield (tn per ha)"]
        # )

        return self.df_analysis

    def map(self, df_plot):
        # df_plot = self.df_analysis.copy()
        models = df_plot["Model"].unique()

        for model in models:
            df_model = df_plot[df_plot["Model"] == model]

            countries = df_model["Country"].unique().tolist()
            if len(countries) > 1:
                self.dir_plot = self.dir_analysis
                fname_prefix = f"{len(countries)}_countries"
            else:
                self.dir_plot = self.dir_analysis / self.country / self.crop
                fname_prefix = f"{self.country}"
            countries = [country.title().replace("_", " ") for country in countries]
            df_model["Country Region"] = (
                df_model["Country"].str.lower().str.replace("_", " ")
                + " "
                + df_model["Region"].str.lower().str.replace("_", " ")
            )

            # Change Harvest year to type int
            df_model["Harvest Year"] = df_model["Harvest Year"].astype(int)
            annotate_region_column = (
                "ADM1_NAME" if self.admin_zone == "admin_1" else "ADM2_NAME"
            )
            analysis_years = df_model["Harvest Year"].unique()
            pbar = tqdm(analysis_years, leave=False)
            for idx, year in enumerate(pbar):
                pbar.set_description(f"Map {year}")
                pbar.update()

                df_harvest_year = df_model[df_model["Harvest Year"] == year]

                for time_period in tqdm(
                    df_harvest_year["Stage Name"].unique(), desc="Map"
                ):
                    df_time_period = df_harvest_year[
                        df_harvest_year["Stage Name"] == time_period
                    ]
                    #
                    #                 """ % of total area """
                    if idx == 0:
                        fname = f"{self.country}_{self.crop}_perc_area.png"
                        col = "% of total Area (ha)"
                        plot.plot_df_shpfile(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_model,  # dataframe containing information that will be mapped
                            merge_col="Country Region",  # Column on which to merge
                            name_country=countries,  # Plot global map
                            name_col=col,  # Which column to plot
                            dir_out=self.dir_plot / str(year),  # Output directory
                            fname=fname,  # Output file name
                            label=f"% of Total Area (ha)\n{self.crop.title()}",
                            vmin=df_model[col].min(),
                            vmax=df_model[col].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",
                            show_bg=False,
                            annotate_regions=True,
                            annotate_region_column=annotate_region_column,
                            loc_legend="lower left",
                        )
                    #
                    """ Unique regions """
                    fname = f"{self.country}_{self.crop}_region_ID.png"
                    col = "Region_ID"
                    df_model[col] = df_model[col].astype(int) + 1
                    if len(df_model["Region_ID"].unique() > 1):
                        # Create a dictionary with each region assigned a unique integer identifier and name
                        dict_region = {
                            int(key): key
                            for key in df_time_period["Region_ID"].unique()
                        }

                        # plot.plot_df_shpfile(
                        #     self.dg,  # dataframe containing adm1 name and polygon
                        #     df_model,  # dataframe containing information that will be mapped
                        #     dict_lup=dict_region,
                        #     merge_col="Country Region",  # Column on which to merge
                        #     name_country=countries,  # Plot global map
                        #     name_col=col,  # Which column to plot
                        #     dir_out=self.dir_plot / str(year),  # Output directory
                        #     fname=fname,  # Output file name
                        #     label=f"Region Cluster\n{self.crop.title()}",
                        #     vmin=df_model[col].min(),
                        #     vmax=df_model[col].max(),
                        #     cmap=pal.tableau.Tableau_20.mpl_colors,
                        #     series="qualitative",
                        #     show_bg=False,
                        #     alpha_feature=1,
                        #     use_key=True,
                        #     annotate_regions=True,
                        #     annotate_region_column=annotate_region_column,
                        #     loc_legend="lower left",
                        # )
                    #                     breakpoint()

                    # """ Anomaly """
                    # fname = (
                    #     f"{fname_prefix}_{self.crop}_{time_period}_{year}_anomaly.png"
                    # )
                    # plot.plot_df_shpfile(
                    #     self.dg,  # dataframe containing adm1 name and polygon
                    #     df_harvest_year,  # dataframe containing information that will be mapped
                    #     merge_col="Country Region",  # Column on which to merge
                    #     name_country=countries,  # Plot global map
                    #     name_col="Anomaly",  # Which column to plot
                    #     dir_out=self.dir_plot / str(year),  # Output directory
                    #     fname=fname,  # Output file name
                    #     label=f"% of {self.number_lag_years}-year Median Yield\n{self.crop.title()}, {year}",
                    #     vmin=df_harvest_year["Anomaly"].min(),
                    #     vmax=110,  # df_harvest_year["Anomaly"].max(),
                    #     cmap=pal.cartocolors.diverging.Geyser_5_r,
                    #     series="sequential",
                    #     show_bg=False,
                    #     annotate_regions=True,
                    #     annotate_region_column=annotate_region_column,
                    #     loc_legend="lower left",
                    # )

                    """ Predicted Yield """
                    fname = f"{fname_prefix}_{self.crop}_{time_period}_{year}_predicted_yield.png"
                    plot.plot_df_shpfile(
                        self.dg,  # dataframe containing adm1 name and polygon
                        df_harvest_year,  # dataframe containing information that will be mapped
                        merge_col="Country Region",  # Column on which to merge
                        name_country=countries,  # Plot global map
                        name_col="Predicted Yield (tn per ha)",  # Which column to plot
                        dir_out=self.dir_plot / str(year),  # Output directory
                        fname=fname,  # Output file name
                        label=f"Predicted Yield (Mg/ha)\n{self.crop.title()}, {year}",
                        vmin=df_harvest_year[self.predicted].min(),
                        vmax=df_harvest_year[self.predicted].max(),
                        cmap=pal.scientific.sequential.Bamako_20_r,
                        series="sequential",
                        show_bg=False,
                        annotate_regions=True,
                        annotate_region_column=annotate_region_column,
                        loc_legend="lower left",
                    )

                    """ Ratio of Predicted to last Year Yield """
                    # fname = f"{self.country}_{self.crop}_{time_period}_{year}_ratio_last_year_yield.png"
                    # plot.plot_df_shpfile(
                    #     self.dg,  # dataframe containing adm1 name and polygon
                    #     df_time_period,  # dataframe containing information that will be mapped
                    #     merge_col="Country Region",  # Column on which to merge
                    #     name_country=countries,  # Plot global map
                    #     name_col="Ratio Last Year",  # Which column to plot
                    #     dir_out=self.plot_dir / str(year),  # Output directory
                    #     fname=fname,  # Output file name
                    #     label=f"Ratio Last Year to {self.predicted}\n{self.crop.title()}, {time_period} {year}",
                    #     vmin=df_time_period["Ratio Last Year"].min(),
                    #     vmax=df_time_period["Ratio Last Year"].max(),
                    #     cmap=pal.scientific.sequential.Bamako_20_r,
                    #     series="sequential",
                    #     show_bg=False,
                    #     annotate_regions=True,
                    #     annotate_region_column=annotate_region_column,
                    #     loc_legend="lower left",
                    # )

                    # Area
                    # breakpoint()
                    if df_time_period["Area (ha)"].notna().all():
                        fname = f"{self.country}_{self.crop}_{year}_area.png"
                        plot.plot_df_shpfile(
                            self.dg,  # dataframe containing adm1 name and polygon
                            df_time_period,  # dataframe containing information that will be mapped
                            merge_col="Country Region",  # Column on which to merge
                            name_country=countries,  # Plot global map
                            name_col="Area (ha)",  # Which column to plot
                            dir_out=self.dir_plot / str(year),  # Output directory
                            fname=fname,  # Output file name
                            label=f"Area (ha)\n{self.crop.title()}, {time_period}",
                            vmin=df_time_period["Area (ha)"].min(),
                            vmax=df_time_period["Area (ha)"].max(),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",
                            show_bg=False,
                            annotate_regions=True,
                            loc_legend="lower left",
                        )

    def plot_metric(self, df, metric="$r^2$"):
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax = sns.lineplot(data=df, x="Date", y=metric, ax=ax)  # "$r^2$"
            ax.set_xlabel("")
            ax.set_ylabel(metric)
            plt.xticks(rotation=0)
            plt.tight_layout()

            # If metric is $r^2$ or NSE, do not plot values below 0
            if metric in ["$r^2$", "Nash-Sutclwiiff Efficiency"]:
                plt.ylim(0, 1)

            # Replace \n in metric
            metric = metric.replace("\n", " ")
            fname = f"{self.country}_{self.crop}_{metric}.png"

            plt.savefig(self.dir_analysis / fname, dpi=250)
            plt.close()

    def execute(self):
        self.query()
        df = self.preprocess()
        self.analyze()

        return df

    def get_config_data(self):
        try:
            with sqlite3.connect(self.db_path) as con:
                # Find names of all tables starting with 'config'
                query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'config%'"
                df = pd.read_sql_query(query, con)

                if df.empty:
                    raise ValueError("No configuration tables found")

                # Extract datetime from the table names
                re = "(\d{4} \d{2}:\d{2})$"
                df["datetime"] = pd.to_datetime(
                    df["name"].str.extract(re)[0], format="%Y %H:%M"
                )

                # Sort the DataFrame by datetime in descending order and get the latest config file
                latest_config = df.sort_values(by="datetime", ascending=False).iloc[0][
                    "name"
                ]

                self.logger.info("=====================================")
                self.logger.info(f"\t{latest_config}")
                self.logger.info("=====================================")
                # Read the latest config file
                query = f"SELECT * FROM {latest_config}"
                self.df_config = pd.read_sql_query(query, con)
        except Exception as e:
            self.logger.error(f"Failed to get configuration data: {e}")

    def setup(self):
        """

        Args:
            country:
            crop:
            model:

        Returns:

        """
        self.dict_config = {}

        self.observed = "Observed Yield (tn per ha)"
        self.predicted = "Predicted Yield (tn per ha)"

        # Get the ML section
        df_ml = self.df_config[self.df_config["Section"] == "ML"]

        self.countries = ast.literal_eval(
            df_ml[df_ml["Option"] == "countries"]["Value"].values[0]
        )
        for country in self.countries:
            df = self.df_config[self.df_config["Section"] == country]

            method = df[df["Option"] == "method"]["Value"].values[0]
            crops = ast.literal_eval(df[df["Option"] == "crops"]["Value"].values[0])
            models = ast.literal_eval(df[df["Option"] == "models"]["Value"].values[0])
            admin_zone = df[df["Option"] == "admin_zone"]["Value"].values[0]
            name_shapefile = df[df["Option"] == "boundary_file"]["Value"].values[0]

            for crop in crops:
                # Does a table with the name {country}_{crop} exist in the database?
                table = f"{country}_{crop}"
                if self.table_exists(self.db_path, table):
                    self.dict_config[f"{country}_{crop}"] = {
                        "method": method,
                        "crops": crop,
                        "models": models,
                        "admin_zone": admin_zone,
                        "name_shapefile": name_shapefile,
                    }

        shp_file = self.parser.get(country, "boundary_file")
        self.dg = gpd.read_file(
            self.dir_shapefiles / shp_file,
            engine="pyogrio",
        )
        self.admin_col_name = self.parser.get(country, "admin_col_name")

        # If ADMIN0 or ADM0_NAME is not in the shapefile, then add ADM0_NAME
        if "ADMIN0" or "ADM0_NAME" not in self.dg.columns:
            self.dg.loc[:, "ADMIN0"] = country.title().replace("_", " ")
        # if ADMIN1 or ADM1_NAME is not in the shapefile, then rename admin_col_name to ADM1_NAME
        if "ADMIN1" or "ADM1_NAME" not in self.dg.columns:
            if admin_zone == "admin_1":
                self.dg.rename(columns={self.admin_col_name: "ADMIN1"}, inplace=True)

        # Hack rename Tanzania to United Republic of Tanzania
        self.dg["ADMIN0"] = self.dg["ADMIN0"].replace(
            "Tanzania", "United Republic of Tanzania"
        )

        # Rename ADMIN0 to ADM0_NAME and ADMIN1 to ADM1_NAME and ADMIN2 to ADM2_NAME
        self.dg = self.dg.rename(
            columns={
                "ADMIN0": "ADM0_NAME",
                "ADMIN1": "ADM1_NAME",
                "ADMIN2": "ADM2_NAME",
            }
        )

        # Create a new column called Country Region that is the concatenation of ADM0_NAME and ADM1_NAME
        # however if ADM2_NAME is not null, then it is the concatenation of ADM0_NAME and ADM2_NAME
        self.dg["Country Region"] = self.dg["ADM0_NAME"]
        self.dg["Country Region"] = self.dg["Country Region"].str.cat(
            self.dg["ADM1_NAME"], sep=" "
        )
        if "ADM2_NAME" in self.dg.columns:
            self.dg.loc[self.dg["ADM2_NAME"].notna(), "Country Region"] = (
                self.dg["ADM0_NAME"] + " " + self.dg["ADM2_NAME"]
            )
        # Make it lower case
        self.dg["Country Region"] = (
            self.dg["Country Region"].str.lower().replace("_", " ")
        )


@dataclass
class RegionalMapper(Geoanalysis):
    path_config_files: List[Path] = field(default_factory=list)
    logger: log = None
    parser: ConfigParser = field(default_factory=ConfigParser)

    def __post_init__(self):
        # Call the parent class constructor
        super().__post_init__()
        self.get_config_data()
        self.setup()

    def map_regional(self):
        """Main function to read data and generate plots."""
        self.read_data()

        self.clean_data()
        self.plot_heatmap()
        self.plot_kde()
        self.plot_mape_map()
        self.plot_mape_by_year()

    def read_data(self):
        """Read data from the database."""
        con = sqlite3.connect(self.db_path)

        query = "SELECT * FROM regional_metrics"
        self.df_regional = pd.read_sql_query(query, con)
        query = "SELECT * FROM regional_metrics_by_year"
        self.df_regional_by_year = pd.read_sql_query(query, con)

        con.close()

    def clean_data(self):
        """Clean and format the data."""
        self.df_regional["Country"] = (
            self.df_regional["Country"].str.replace("_", " ").str.title()
        )
        self.df_regional["Model"] = self.df_regional["Model"].str.title()

    def plot_heatmap(self):
        """Generate heatmaps of MAPE bins vs. % total area bins."""
        models = self.df_regional["Model"].unique()
        for model in models:
            df_model = self.df_regional[self.df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 0.5)
                & (df_model["Mean Absolute Percentage Error"] > 100)
            ]

            df_model = df_model.drop(df_tmp.index)
            bin_edges = np.linspace(0, df_model["% of total Area (ha)"].max() + 1, 6)
            df_model["Area Bins"] = pd.cut(
                df_model["% of total Area (ha)"], bins=bin_edges, precision=0
            )
            df_model["MAPE Bins"] = pd.cut(
                df_model["Mean Absolute Percentage Error"],
                bins=5,
                right=False,
                precision=1,
            )
            area_mape_counts = (
                df_model.groupby(["Area Bins", "MAPE Bins"])
                .size()
                .unstack(fill_value=0)
            )
            self._plot_heatmap(area_mape_counts, model)

    def _plot_heatmap(self, area_mape_counts, model):
        """
        Plot heatmap helper function
        Args:
            area_mape_counts:
            model:

        Returns:

        """
        plt.figure(figsize=(10, 8))

        ax = sns.heatmap(
            area_mape_counts,
            annot=True,
            square=True,
            cmap=pal.scientific.sequential.Bamako_20_r.mpl_colormap,
            fmt="d",
        )
        for text in ax.texts:
            if text.get_text() == "0":
                text.set_text("")
                text.set_color("white")
        plt.ylabel("% of Total Area (ha) Bins")
        plt.xlabel("MAPE Bins")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.invert_yaxis()

        plt.tight_layout()
        plt.savefig(self.dir_analysis / f"heatmap_{model}.png", dpi=250)
        plt.close()

    def plot_kde(self):
        """Generate KDE plots of MAPE for each country."""
        models = self.df_regional["Model"].unique()

        for model in models:
            df_model = self.df_regional[self.df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 0.5)
                & (df_model["Mean Absolute Percentage Error"] > 100)
                ]

            df_model = df_model.drop(df_tmp.index)

            with plt.style.context("science"):
                plt.figure(figsize=(12, 8))
                for label, group_data in df_model.groupby("Country"):
                    sns.histplot(
                        group_data["Mean Absolute Percentage Error"],
                        label=label,
                    )

                # Plot a dashed gray line at x=20
                plt.axvline(x=20, color="gray", linestyle="--")

                plt.minorticks_on()
                plt.xlabel("Mean Absolute Percentage Error (%)")
                plt.ylabel("Frequency")
                plt.legend(title="Country", title_fontsize="13")

                # Adding the title at the top-right corner
                plt.text(
                    0.95, 0.95,  # Coordinates in axes fraction
                    f"Model: {model}",
                    transform=plt.gca().transAxes,
                    fontsize=14,
                    verticalalignment="top",
                    horizontalalignment="right",
                    bbox=dict(facecolor="white", alpha=0.6, edgecolor="none")
                )

                plt.tight_layout()
                plt.savefig(self.dir_analysis / f"mape_histogram_{model}.png", dpi=250)
                plt.close()

    def plot_mape_map(self):
        """Plot the map of MAPE."""
        self.df_regional["Country Region"] = (
            self.df_regional["Country"].str.lower().str.replace("_", " ")
            + " "
            + self.df_regional["Region"].str.lower()
        )
        models = self.df_regional["Model"].unique()

        for model in models:
            df_model = self.df_regional[self.df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 0.5)
                & (df_model["Mean Absolute Percentage Error"] > 100)
            ]

            df_model = df_model.drop(df_tmp.index)

            col = "Mean Absolute Percentage Error"
            countries = df_model["Country"].unique().tolist()
            countries = [country.title().replace("_", " ") for country in countries]
            crop = df_model["Crop"].unique()[0].title().replace('_', ' ')
            df = df_model[df_model["Country"].isin(countries)]
            self.dg = self.dg[self.dg["ADM0_NAME"].isin(countries)]

            fname = f"mape_{crop}_{df_model['Model'].iloc[0]}.png"
            plot.plot_df_shpfile(
                self.dg,
                df,
                merge_col="Country Region",
                name_country=countries,
                name_col=col,
                dir_out=self.dir_analysis,
                fname=fname,
                label="MAPE (%)",
                vmin=df[col].min(),
                vmax=df[col].max(),
                cmap=pal.scientific.sequential.Bamako_20_r,
                series="sequential",
                show_bg=False,
                annotate_regions=True,
                loc_legend="lower left",
            )

    def plot_mape_by_year(self):
        """Compute MAPE by year and plot using a bar chart."""
        # Compute the Mean Absolute Percentage Error (MAPE) by year
        mape_by_year = (
            self.df_regional_by_year.groupby("Harvest Year")[
                "Mean Absolute Percentage Error"
            ]
            .mean()
            .reset_index()
        )

        # Plot MAPE by year
        with plt.style.context("science"):
            plt.figure(figsize=(10, 6))
            sns.barplot(
                x="Harvest Year", y="Mean Absolute Percentage Error", data=mape_by_year
            )
            # Draw a dashed gray line at y=20
            plt.axhline(y=20, color="gray", linestyle="--")

            plt.xlabel("")
            plt.ylabel("Mean Absolute Percentage Error (%)")
            plt.xticks(rotation=0)

            plt.tight_layout()
            plt.savefig(self.dir_analysis / "mape_by_year.png", dpi=250)
            plt.close()


def run(path_config_files=[Path("../config/geocif.txt")]):
    logger, parser = log.setup_logger_parser(path_config_files)

    obj = Geoanalysis(path_config_files, logger, parser)
    obj.get_config_data()
    obj.setup()

    """ Loop over each country, crop, model combination in dict_config """
    frames = []
    for country_crop, value in obj.dict_config.items():
        obj.crop = value["crops"]
        # to get country, remove obj.crops from country_crop
        obj.country = country_crop.replace(f"_{obj.crop}", "")

        obj.admin_zone = value["admin_zone"]
        obj.boundary_file = value["name_shapefile"]
        obj.method = value["method"]
        obj.number_lag_years = 5

        obj.table = f"{obj.country}_{obj.crop}"
        models = value["models"]
        for model in models:
            obj.model = model

            df_tmp = obj.execute()
            frames.append(df_tmp)

    df = pd.concat(frames)

    """ Map regional error metrics """
    mapper = RegionalMapper(path_config_files, logger, parser)
    mapper.map_regional()

    """ For each country, plot yields, conditions, anomalies, etc. """
    obj.map(df)


if __name__ == "__main__":
    run()
