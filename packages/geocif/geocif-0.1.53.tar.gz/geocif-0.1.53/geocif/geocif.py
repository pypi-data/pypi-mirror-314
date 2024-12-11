# panel serve climate_risk_dashboard.py
import ast
import os
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import wandb
import arrow as ar
import geopandas as gp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from geocif import logger as log
from geocif import utils
from .cei import definitions as di
from .ml import correlations
from .ml import spatial_autocorrelation as sa
from .ml import feature_engineering as fe
from .ml import feature_selection as fs
from .ml import output
from .ml import stages
from .ml import stats
from .ml import trainers
from .ml import trend
from .ml import xai

plt.style.use("default")

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


@dataclass
class Geocif:
    method: str = "dekad_r"
    group_by: List[str] = field(
        default_factory=lambda: ["Index", "Country", "Region", "Crop", "Season"]
    )
    metrics: List[str] = field(default_factory=lambda: ["$r^2$", "RMSE", "MAE", "MAPE"])
    logger: log = None
    parser: ConfigParser = field(default_factory=ConfigParser)
    project_name: str = "geocif"

    def __post_init__(self):
        self.dir_output = Path(self.parser.get("PATHS", "dir_output"))
        self.dir_condition = Path(self.parser.get("PATHS", "dir_condition"))
        os.makedirs(self.dir_output / "ml", exist_ok=True)

        self.country: str = None
        self.crop: str = None
        self.forecast_season: int = None
        self.all_stages: list = []
        self.all_seasons: list = []
        self.all_seasons_with_yield: list = []
        self.model_names: list = []
        self.feature_names: list = []
        self.selected_features: list = []

        self._date = ar.utcnow().to("America/New_York")
        self.today = self._date.format("MMMM_DD_YYYY")
        self.today_year = self._date.year
        self.today_doy = int(self._date.format("DDD"))
        self.today_full = self._date.format("MMMM_DD_YYYY_HH_mm")

        self.df_forecast = pd.DataFrame()
        """
        ====================================================================
                                        Config file: Logging
        ====================================================================
        """
        self.log_level = self.parser.get("LOGGING", "log_level")

        """
        ====================================================================
                                Config file: Default
        ====================================================================
        """
        self.method = self.parser.get("DEFAULT", "method")
        self.db_forecasts = self.parser.get("DEFAULT", "db")
        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.do_parallel = self.parser.getboolean("DEFAULT", "do_parallel")
        self.update_input_file = self.parser.getboolean("DEFAULT", "update_input_file")
        self.correlation_plots = self.parser.getboolean("DEFAULT", "correlation_plots")
        self.national_correlation = self.parser.getboolean(
            "DEFAULT", "national_correlation"
        )
        self.plot_map_for_correlation_plot = self.parser.getboolean(
            "DEFAULT", "plot_map_for_correlation_plot"
        )
        self.correlation_plot_groupby = self.parser.get(
            "DEFAULT", "correlation_plot_groupby"
        )
        self.run_ml = self.parser.getboolean("DEFAULT", "run_ml")

        """
        ====================================================================
                                Config file: ML
        ====================================================================
        """
        self.model_type = self.parser.get("ML", "model_type")
        self.classify_target = self.parser.getboolean("ML", "classify_target")
        self.number_classes = self.parser.getint("ML", "number_classes")
        self.target = self.parser.get("ML", "target")
        self.rename_target = self.parser.getboolean("ML", "rename_target")
        self.new_name_target = self.parser.get("ML", "new_name_target")
        self.fraction_simulate = self.parser.getint("ML", "fraction_simulate")
        self.analogous_year_yield_as_feature = self.parser.getboolean(
            "ML", "analogous_year_yield_as_feature"
        )
        self.correlation_threshold = self.parser.getfloat("ML", "correlation_threshold")
        self.include_lat_lon_as_feature = self.parser.getboolean(
            "ML", "include_lat_lon_as_feature"
        )
        self.spatial_autocorrelation = self.parser.getboolean(
            "ML", "spatial_autocorrelation"
        )
        self.sa_method = self.parser.get("ML", "sa_method")
        self.last_year_yield_as_feature = self.parser.getboolean(
            "ML", "last_year_yield_as_feature"
        )
        self.panel_model = self.parser.getboolean("ML", "panel_model")
        self.panel_model_region = self.parser.get("ML", "panel_model_region")
        self.use_outlook_as_feature = self.parser.getboolean(
            "ML", "use_outlook_as_feature"
        )
        self.use_single_time_period_as_feature = self.parser.getboolean(
            "ML", "use_single_time_period_as_feature"
        )
        self.lag_yield_as_feature = self.parser.getboolean("ML", "lag_yield_as_feature")
        self.number_median_years = self.parser.getint("ML", "median_years")
        self.median_yield_as_feature = self.parser.getboolean(
            "ML", "median_yield_as_feature"
        )
        self.median_area_as_feature = self.parser.getboolean(
            "ML", "median_area_as_feature"
        )
        self.number_lag_years = self.parser.getint("ML", "lag_years")
        self.cluster_strategy = self.parser.get("ML", "cluster_strategy")
        self.feature_selection = self.parser.get("ML", "feature_selection")
        self.check_yield_trend = self.parser.getboolean("ML", "check_yield_trend")
        self.run_latest_time_period = self.parser.getboolean(
            "ML", "run_latest_time_period"
        )
        self.run_every_time_period = self.parser.get("ML", "run_every_time_period")
        self.cat_features: list = ast.literal_eval(
            self.parser.get("ML", "cat_features")
        )

        self.use_cumulative_features = self.parser.getboolean(
            "DEFAULT", "use_cumulative_features"
        )
        """
        ====================================================================
                                Variables, Paths
        ====================================================================
        """
        # If ML model is run for individual region or cluster, then Region_ID is the same for each region
        # or cluster and therefore redundant for the ML model
        # if self.cluster_strategy in ["individual", "auto_detect"]:
        #    self.cat_features.remove("Region_ID")

        self.target_bins = {}

        self.fixed_columns: list = [
            "Country",
            "Region",
            "Crop",
            "Area",
            "Season",
            "Harvest Year",
        ]
        self.target: str = "Yield (tn per ha)"
        self.statistics_columns: list = [
            "Area (ha)",
            "Production (tn)",
        ]

        self.combined_dict = {
            **di.dict_indices,
            **di.dict_ndvi,
            **di.dict_gcvi,
            **di.dict_esi4wk,
            **di.dict_hindex,
        }

        self.combined_keys = list(self.combined_dict.keys())

        self.dir_ml = self.dir_output / "ml"
        self.dir_db = self.dir_ml / "db"
        self.dir_analysis = self.dir_ml / "analysis" / self.today
        dir_input = Path(self.parser.get("PATHS", "dir_input"))
        self.dir_shapefiles = dir_input / "Global_Datasets" / "Regions" / "Shps"

        os.makedirs(self.dir_db, exist_ok=True)
        os.makedirs(self.dir_analysis, exist_ok=True)

        self.db_path = self.dir_db / self.db_forecasts

        # self.pickle_file = self.base_dir / self.parser.get("outlook", "pickle_file")
        # obj_pickle = outlook.Outlook(self.pickle_file)
        # self.df_outlook = obj_pickle.read_outlook_file()

    def train(self, df_region, scaler=None):
        """

        Args:
            df_region:
            scaler:

        Returns:

        """

        """ Perform feature selection """
        if self.model_type == "REGRESSION":
            target_column = (
                f"Detrended {self.target}" if self.check_yield_trend else self.target
            )
        elif self.model_type == "CLASSIFICATION":
            target_column = self.target_class

        # Drop rows where target_column is NaN
        df_region = df_region.dropna(subset=[target_column])

        X_train = df_region[self.feature_names]
        # Drop any columns with NaNs
        X_train = X_train.dropna(axis=1, how="any")
        y_train = df_region[target_column]

        if self.ml_model:
            if self.model_name in ["cumulative_1", "cumulative_2", "cumulative_3"]:
                all_features = X_train.columns

                # Select the columns with use_ceis in it
                self.selected_features = [
                    column
                    for column in all_features
                    if any(cei in column for cei in self.use_ceis)
                ]
            else:
                # self.logger.info(f"Selecting features for {self.country} {self.crop}")
                selector, _, self.selected_features = fs.select_features(
                    X_train, y_train, method=self.feature_selection
                )
                # self.logger.info(f"Selected features: {self.selected_features}")

            """ Update model to include conformal estimates """
            if "lat" not in self.selected_features and self.include_lat_lon_as_feature:
                self.selected_features.append("lat")
            if "lon" not in self.selected_features and self.include_lat_lon_as_feature:
                self.selected_features.append("lon")
            X_train = df_region[self.selected_features + self.cat_features]

            dir_output = (
                self.dir_analysis
                / self.country
                / self.crop
                / self.model_name
                / str(self.forecast_season)
            )

            region_id = df_region["Region_ID"].unique()[0]
            X_train.to_csv(dir_output / f"X_train_{region_id}.csv", index=False)
            if scaler:
                X_train_nocat = X_train.drop(
                    columns=[
                        item for item in self.cat_features if item != "Harvest Year"
                    ]
                )
                X_train_scaled = scaler.fit_transform(X_train_nocat)
            else:
                X_train_scaled = X_train

            """ Train model """
            self.best_hyperparams, self.model = trainers.auto_train(
                self.cluster_strategy,
                self.model_name,
                self.model_type,
                False,
                "Harvest Year",
                df_region[self.selected_features + self.cat_features + [self.target]],
                X_train_scaled,
                y_train,
                feature_names=self.selected_features,
                target_col=target_column,
                optimize=self.optimize,
                fraction_loocv=self.fraction_loocv,
                cat_features=self.cat_features,
            )

            """ Estimate CI only if flag is True """
            if self.estimate_ci:
                if self.estimate_ci_for_all or self.forecast_season == self.today_year:
                    self.model = trainers.estimate_ci(
                        self.model_type, self.model_name, self.model
                    )

            try:
                if self.model_name == "catboost":
                    self.model.fit(
                        X_train,
                        y_train,
                        cat_features=self.cat_features,
                        verbose=False,
                    )
                elif self.model_name == "ngboost":
                    self.model.fit(X_train, y_train)
                elif self.model_name in ["oblique"]:
                    self.model.fit(X_train, y_train)
                elif self.model_name == "ydf":
                    # Combine X_train and y_train
                    df_train = pd.concat([X_train, y_train], axis=1)

                    self.model = self.model.train(df_train)
                elif self.model_name == "geospaNN":
                    self.model.fit(
                        X_train,
                        y_train,
                        # callbacks=[TQDMCallback(self.best_hyperparams["iterations"])],
                    )
                elif self.model_name == "merf":
                    Z_train = np.ones((len(X_train), 1))
                    clusters_train = df_region["Region"]
                    clusters_train.reset_index(drop=True, inplace=True)

                    self.model.fit(
                        X_train,
                        Z_train,
                        clusters_train.astype("object"),
                        y_train.values,
                    )
                elif self.model_name == "linear":
                    self.model.fit(X_train_scaled, y_train)
                elif self.model_name == "gam":
                    self.model.fit(X_train_scaled.values, y_train.values)
                    self.best_hyperparams = {}
                elif self.model_name in ["cubist"]:
                    self.model.fit(X_train, y_train)
                elif self.model_name in [
                    "cumulative_1",
                    "cumulative_2",
                    "cumulative_3",
                ]:
                    from sklearn.preprocessing import StandardScaler, LabelEncoder

                    if self.model_name == "cumulative_1":
                        num_columns = 1
                    elif self.model_name == "cumulative_2":
                        num_columns = 2
                    elif self.model_name == "cumulative_3":
                        num_columns = 3

                    # Standardize the numeric features
                    scaler = StandardScaler()
                    X_numeric = X_train.iloc[:, :num_columns]
                    X_scaled_numeric = pd.DataFrame(
                        scaler.fit_transform(X_numeric),
                        columns=X_numeric.columns,
                        index=X_train.index,
                    )

                    # Encode the Region as categorical
                    le = LabelEncoder()
                    X_region = pd.Series(
                        le.fit_transform(X_train["Region"]),
                        name="Region",
                        index=X_train.index,
                    )

                    # Combine scaled numeric features and encoded region
                    X_train_scaled = pd.concat([X_scaled_numeric, X_region], axis=1)

                    self.model.fit(X_train_scaled, y_train)
            except Exception as e:
                self.logger.error(
                    f"Error fitting model for {self.country} {self.crop} {e}"
                )

    def predict(self, df_region, scaler=None):
        """
        Predict yield for the current stage
        :param df_region:
        :param scaler:
        """
        """ Select dataframe for prediction"""
        X_test = df_region[self.selected_features + self.cat_features]
        y_test = df_region[self.target].values
        best_hyperparameters = {}

        """ Do prediction based on model type"""
        if not self.ml_model:
            best_hyperparameters = np.nan
            if self.model_name == "analog":
                y_pred = np.full(len(X_test), df_region["Analogous Year Yield"].values)
            elif self.model_name == "median":
                y_pred = np.full(len(X_test), df_region[f"Median {self.target}"].values)
            elif self.model_name == "last_year":
                y_pred = np.full(
                    len(X_test), df_region[f"Last Year {self.target}"].values
                )
        else:
            if self.model_name in ["linear", "gam"]:
                # Drop cat_features from X_test
                X_test = X_test.drop(
                    columns=[
                        item for item in self.cat_features if item != "Harvest Year"
                    ]
                )
                X_test = scaler.transform(X_test)
                best_hyperparameters = {}

            if self.estimate_ci:
                if self.estimate_ci_for_all or self.forecast_season == self.today_year:
                    if self.model_name in ["logistic", "catboost"] and self.model_type == "CLASSIFICATION":
                        y_pred = self.model.predict(X_test)
                        y_pred_ci = self.model.predict_proba(X_test)
                    elif self.model_name == "ngboost":
                        y_pred = self.model.predict(X_test)

                        if self.model_type == "REGRESSION":
                            y_dists = self.model.pred_dist(X_test)
                            z_value = utils.get_z_value(self.alpha)

                            # Extract means and standard deviations from the distribution predictions
                            means = y_dists.loc
                            std_devs = y_dists.scale

                            # Calculate lower and upper bounds of the prediction intervals
                            lower_bounds = means - z_value * std_devs
                            upper_bounds = means + z_value * std_devs

                            # Output would be similar to Mapie: point predictions, lower bounds, and upper bounds
                            y_pred_ci = np.vstack([lower_bounds, means, upper_bounds]).T
                        elif self.model_type == "CLASSIFICATION":
                            y_pred_ci = self.model.predict_proba(X_test)

                            # Output should be similar to Mapie: point predictions, lower bounds, and upper bounds
                            y_pred_ci = np.vstack(
                                [y_pred_ci[:, 0], y_pred, y_pred_ci[:, 1]]
                            ).T
                    else:
                        y_pred, y_pred_ci = self.model.predict(X_test, alpha=self.alpha)
                        best_hyperparameters = self.model.get_params().copy()
                        # If estimator key is in best_hyperparameters, remove it
                        if "estimator" in best_hyperparameters:
                            del best_hyperparameters["estimator"]
            elif self.model_name == "merf":
                Z_test = np.ones((len(X_test), 1))
                clusters_test = df_region["Region"]
                clusters_test.reset_index(drop=True, inplace=True)

                y_pred = self.model.predict(
                    X_test, Z_test, clusters_test.astype("object")
                )
                best_hyperparameters = self.model.fe_model.get_params().copy()
            elif self.model_name in ["cumulative_1", "cumulative_2", "cumulative_3"]:
                from sklearn.preprocessing import StandardScaler, LabelEncoder

                if self.model_name == "cumulative_1":
                    num_columns = 1
                elif self.model_name == "cumulative_2":
                    num_columns = 2
                elif self.model_name == "cumulative_3":
                    num_columns = 3

                # Standardize the numeric features
                scaler = StandardScaler()
                X_numeric = X_test.iloc[:, :num_columns]
                try:
                    X_scaled_numeric = pd.DataFrame(
                        scaler.fit_transform(X_numeric),
                        columns=X_numeric.columns,
                        index=X_test.index,
                    )
                except:
                    breakpoint()

                # Encode the Region as categorical
                le = LabelEncoder()
                X_region = pd.Series(
                    le.fit_transform(X_test["Region"]),
                    name="Region",
                    index=X_test.index,
                )

                # Combine scaled numeric features and encoded region
                X_test_scaled = pd.concat([X_scaled_numeric, X_region], axis=1)
                y_pred = self.model.predict(X_test_scaled)
                best_hyperparameters = {}  # self.model.get_params().copy()
            elif self.model_name == "geospaNN":
                import torch
                import geospaNN

                # Remove any categorical features
                X_test = X_test.drop(columns=self.cat_features)
                X = torch.from_numpy(X_test.to_numpy()).float()
                coord = torch.from_numpy(
                    self.df_test[["lon", "lat"]].to_numpy()
                ).float()

                p = X.shape[1]
                n = X.shape[0]
                nn = 5

                data = geospaNN.make_graph(X, Y, coord, nn)

                # remove categorical features from df_train
                data_train = df_region[
                    self.selected_features + self.cat_features + [self.target]
                ]
                w_train = data_train.y - self.estimate(data_train.x)
            elif self.model_name == "ydf":
                y_pred = self.model.evaluate(X_test)
                best_hyperparameters = {}
            else:
                y_pred = self.model.predict(X_test)
                best_hyperparameters = self.model.get_params().copy()

        if self.check_yield_trend:
            # Get information for retrending
            for idx, region in enumerate(df_region["Region"].unique()):
                mask_region = self.df_train["Region"] == df_region["Region"].unique()[0]
                df_tmp = self.df_train[mask_region]

                obj_trend = trend.DetrendedData(
                    df_tmp[f"Detrended {self.target}"],
                    df_tmp["Detrended Model"],
                    df_tmp["Detrended Model Type"],
                )

                # Retrend the predicted yield
                y_pred[idx] += trend.compute_trend(
                    obj_trend, df_region.iloc[idx][["Harvest Year"]]
                )[0]

                df_region.loc[
                    idx, "Detrended Model Type"
                ] = obj_trend.model_type.unique()[0]

        # Create a dataframe with forecast results
        shp = len(X_test)
        experiment_id = f"{self.country}_{self.crop}"
        now = ar.utcnow().to("America/New_York").format("MMMM-DD-YYYY HH:mm:ss")
        selected_features = self.selected_features + self.cat_features
        # Compute percentage difference between y_pred and y_test
        if self.model_type == "REGRESSION":
            ape = np.abs((y_pred - y_test) / y_test) * 100
        elif self.model_type == "CLASSIFICATION":
            # Create numpy array full of naNs with the same shape as y_test
            ape = np.full(shp, np.nan)

        df = pd.DataFrame(
            {
                "Experiment_ID": np.full(shp, experiment_id),
                "Experiment Name": np.full(shp, self.experiment_name),
                "Date": np.full(shp, self.today),
                "Time": np.full(shp, now),
                "Country": np.full(shp, self.country),
                "Crop": np.full(shp, self.crop),
                "Cluster Strategy": np.full(shp, self.cluster_strategy),
                "Frequency": np.full(shp, self.method),
                "Selected Features": [selected_features.copy() for _ in range(shp)],
                "Best Hyperparameters": np.full(shp, best_hyperparameters),
                "Stage_ID": np.full(shp, self.stage_info["Stage_ID"]),
                "Stage Range": np.full(shp, self.stage_info["Stage Range"]),
                "Stage Name": np.full(shp, self.stage_info["Stage Name"]),
                "Starting Stage": np.full(shp, self.stage_info["Starting Stage"]),
                "Ending Stage": np.full(shp, self.stage_info["Ending Stage"]),
                "Model": np.full(shp, self.model_name),
                "Region_ID": df_region["Region_ID"].values,
                "Region": df_region["Region"].values,
                "Harvest Year": df_region["Harvest Year"].values,
                "Area (ha)": df_region["Area (ha)"].values,
                f"Observed {self.target}": np.around(y_test, 3).ravel(),
                f"Predicted {self.target}": np.around(y_pred, 3).ravel(),
                "APE": np.around(ape, 3).ravel(),
            }
        )

        if self.median_yield_as_feature:
            # Add median yield to dataframe
            df.loc[:, f"Median {self.target}"] = np.around(
                df_region[f"Median {self.target}"].values, 3
            )

        if self.estimate_ci:
            if self.estimate_ci_for_all or self.forecast_season == self.today_year:
                # Iterate over each element in y_pred_ci
                for idx, ci in enumerate(y_pred_ci):
                    df.loc[idx, "alpha"] = self.alpha
                    if self.model_type == "REGRESSION":
                        # Flatten the list
                        y_pred_ci_ = [item for sublist in ci for item in sublist]

                        df.loc[idx, f"lower CI"] = np.around(y_pred_ci_[0], 3)
                        df.loc[idx, f"upper CI"] = np.around(y_pred_ci_[1], 3)
                    elif self.model_type == "CLASSIFICATION":
                        df.loc[idx, f"CI"] = ", ".join(map(str, ci.flatten()))

        if self.check_yield_trend:
            df.loc[:, "Detrended Model Type"] = df_region["Detrended Model Type"].values

        if self.last_year_yield_as_feature:
            # Add last year yield to dataframe
            df.loc[:, f"Last Year {self.target}"] = np.around(
                df_region[f"Last Year {self.target}"].values, 3
            )

        if self.analogous_year_yield_as_feature:
            try:
                # Add analogous year and yield to dataframe
                df.loc[:, "Analogous Year"] = df_region["Analogous Year"].values
                df.loc[:, "Analogous Year Yield"] = np.around(
                    df_region["Analogous Year Yield"].values, 3
                )
            except:
                breakpoint()

        # if self.spatial_autocorrelation:
        #     # Compute spatial autocorrelation
        #     df = sa.compute_spatial_autocorrelation(
        #         self.dg_country
        #     )

        for col in [
            f"Median {self.target}",
            "Analogous Year",
            "Analogous Year Yield",
            "Detrended Model Type",
            "Detrended Model",
        ]:
            if col not in df.columns:
                df.loc[:, col] = np.NaN

        # Create an index based on following columns
        index_columns = [
            "Experiment Name",
            "Model",
            "Cluster Strategy",
            "Country",
            "Region",
            "Crop",
            "Harvest Year",
            "Stage Name",
            "Time",
        ]

        df.index = df.apply(
            lambda row: "_".join([str(row[col]) for col in index_columns]), axis=1
        )

        # name the index level
        df.index.set_names(["Index"], inplace=True)

        return experiment_id, df

    def create_feature_names(self, stages_features, selected_features):
        """
        Create feature names for machine learning stages.

        Args:
            stages_features (list): List of features for different stages.
            selected_features (dict): Dictionary of selected features.

        Returns:
            None
        """
        # Assert stages_features is a list
        assert isinstance(stages_features, list), "stages_features should be a list"

        # Clear out feature names
        self.feature_names = []

        """
        Select stages that will be used for ML
         1. method = "latest" - Select the latest stage
         2. method = "fraction" - Select a fraction (1-100) of all stages
        """
        method = "fraction"
        if self.model_name in ["cumulative_1", "cumulative_2", "cumulative_3"]:
            method = "latest"

        stages_features = stages.select_stages_for_ml(
            stages_features, method=method, n=60
        )

        for stage in stages_features:
            # Convert each element of stage to str and join with _
            _stage = "_".join(map(str, stage))

            # Create a list appending _stage to each element of combined_keys
            _tmp = [f"{col}_{_stage}" for col in self.combined_keys]

            for _t in _tmp:
                parts = _t.split("_")
                cei = parts[0] if parts[1].isdigit() else "_".join(parts[:2])

                try:
                    if self.model_name in [
                        "cumulative_1",
                        "cumulative_2",
                        "cumulative_3",
                    ]:
                        dict_fn = stages.get_stage_information_dict(_t, self.method)
                        tmp_col = f"{dict_fn['CEI']}"

                        if tmp_col in self.df_train.columns:
                            self.feature_names.append(tmp_col)
                    else:
                        # Check if any element of dict_selected_features is in _t
                        if selected_features["CEI"].any():
                            for x in selected_features["CEI"].values:
                                if x not in cei:
                                    continue

                                dict_fn = stages.get_stage_information_dict(
                                    _t, self.method
                                )
                                tmp_col = f"{dict_fn['CEI']} {dict_fn['Stage Name']}"

                                if tmp_col in self.df_train.columns:
                                    self.feature_names.append(tmp_col)
                except:
                    breakpoint()
        self.feature_names = list(set(self.feature_names))

        if self.median_yield_as_feature:
            self.feature_names.append(f"Median {self.target}")

        if self.lag_yield_as_feature:
            # For the number of years specified in self.number_lag_years
            for i in range(1, self.number_lag_years + 1):
                self.feature_names.append(f"t -{i} {self.target}")

        if self.analogous_year_yield_as_feature:
            self.feature_names.extend(["Analogous Year", "Analogous Year Yield"])

        if self.use_outlook_as_feature:
            self.feature_names.append("FCST")

        # Add lat and lon to feature names
        if self.include_lat_lon_as_feature:
            self.feature_names.extend(["lat", "lon"])

        self.selected_features = []

    def loop_ml(self, stages, dict_selected_features, dict_best_cei):
        """

        Args:
            stages:
            dict_selected_features:
            dict_best_cei:

        Returns:

        """
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler() if self.model_name in ["linear", "gam"] else None

        """ Train, Predict, Explain and Store results for each region """
        pbar = tqdm(self.df_train["Region_ID"].unique(), leave=False)
        for idx, region in enumerate(pbar):
            if self.model_name in ["linear", "gam"]:
                self.create_feature_names(stages, dict_best_cei[region][0:3].tolist())
            elif self.model_name in ["cumulative_1", "cumulative_2", "cumulative_3"]:
                self.create_feature_names(stages, {})
            elif self.ml_model:
                self.create_feature_names(stages, dict_selected_features[region])
            elif self.model_name in ["median"]:
                self.feature_names = [f"Median {self.target}"]
                self.last_year_yield_as_feature = False
                self.analogous_year_yield_as_feature = False
            elif self.model_name in ["analog"]:
                self.feature_names = [f"Analogous Year", f"Analogous Year Yield"]
                self.last_year_yield_as_feature = False
                self.median_yield_as_feature = False

            mask_train = self.df_train["Region_ID"] == region
            mask_test = self.df_test["Region_ID"] == region

            num_regions_in_cluster = self.df_train[mask_train]["Region"].unique()

            if self.cluster_strategy == "individual":
                region_name = self.df_train["Region"].unique()[idx]
                pbar.set_description(f"Fit/Predict for {region_name}")
                pbar.update()
            elif self.cluster_strategy in ["auto_detect", "single"]:
                pbar.set_description(f"Fit/Predict for group {idx + 1}")
                pbar.update()

            common_columns = (
                [self.target, self.target_class]
                + self.statistics_columns
                + self.feature_names
                + ["Region_ID"]
            )
            if self.check_yield_trend:
                common_columns += [
                    f"Detrended {self.target}",
                    "Detrended Model Type",
                    "Detrended Model",
                ]

            if self.last_year_yield_as_feature:
                common_columns += [f"Last Year {self.target}"]

            """ Train """
            # Filter dataframe based on region and self.feature_names
            df_region_train = self.df_train[mask_train]
            df_region_train = df_region_train[self.fixed_columns + common_columns]
            df_region_train.reset_index(drop=True, inplace=True)
            self.train(df_region_train, scaler)

            """ Predict """
            if self.check_yield_trend:
                # Exclude [f"Detrended {self.target}", "Detrended Model Type", "Detrended Model"]
                common_columns = common_columns[:-3]
            df_region_test = self.df_test[mask_test]
            df_region_test = df_region_test[self.fixed_columns + common_columns]
            df_region_test.reset_index(drop=True, inplace=True)
            experiment_id, df = self.predict(df_region_test, scaler)
            # df.reset_index(inplace=True)

            """ XAI """
            if self.do_xai:
                assert not self.estimate_ci, "Cannot perform XAI if estimate_ci is True"

                kwargs = {
                    "cluster_strategy": self.cluster_strategy,
                    "model": self.model,
                    "model_name": self.model_name,
                    "forecast_season": self.forecast_season,
                    "crop": self.crop,
                    "country": self.country,
                    "analysis_dir": self.dir_analysis,
                }
                df_xai = xai.explain(df_region_train, df_region_test, **kwargs)
                # df.set_index("Index", inplace=True)

            """ Output results to database """
            if not self.ml_model:
                model = self.model_name
            elif self.estimate_ci:
                try:
                    model = self.model.estimator_
                except:
                    if self.model_name == "catboost":
                        model = self.model
                    else:
                        model = self.model.estimator
            else:
                model = self.model

            try:
                output.store(self.db_path, experiment_id, df, model, self.model_name)
                wandb.log({experiment_id: df})
            except Exception as e:
                self.logger.error(f"Error storing results for {experiment_id} {e}")

    def get_cei_column_names(self, df):
        all_cei_columns = [
            col
            for col in df.columns
            if col not in self.fixed_columns + [self.target] + self.statistics_columns
        ]

        return all_cei_columns

    def create_ml_dataframe(self, df):
        """
        Create ML ready dataframe
        :param df:
        """
        _str = f"{self.country} {self.crop}"
        self.logger.info(f"Creating ML dataframe {_str}")

        # Convert from long to wide format
        df = df[
            ["Index", "Stage_ID", "CEI"]
            + self.fixed_columns
            + [self.target]
            + self.statistics_columns
        ]

        # For each combination of Index and Stage_ID, new columns have been
        # created and filled with the corresponding CEI value from the original dataframe
        # The new column names are a combination of the original Index and Stage_ID values
        # Use pivot_table to create the new columns and flatten the multi-index columns
        # HACK: Set missing values in self.target_col and self.statistics_columns to -1
        df.loc[:, [self.target] + self.statistics_columns] = df[
            [self.target] + self.statistics_columns
        ].fillna(-1)

        # HACK, replace later
        df.loc[:, "Area"] = df["Area"].fillna(-1)
        df = df.pivot_table(
            index=self.fixed_columns + [self.target] + self.statistics_columns,
            columns=["Index", "Stage_ID"],
            values="CEI",
        ).reset_index()

        # Reset self.target_col and self.statistics_columns to NaN
        df[[self.target] + self.statistics_columns] = df[
            [self.target] + self.statistics_columns
        ].replace(-1, np.nan)

        # Flatten the multi-index columns
        df.columns = [f"{i}_{j}" if j != "" else f"{i}" for i, j in df.columns]

        # Get all the columns apart from the fixed columns, target column and stats columns
        all_cei_columns = self.get_cei_column_names(df)
        parts = all_cei_columns[-1].split("_")
        cei = parts[0] if parts[1].isdigit() else "_".join(parts[:2])

        # For each region, find the column with the longest string in cei_column
        group_by = ["Region"]
        groups = df.groupby(group_by)
        if self.use_cumulative_features:
            frames = []
            for name, group in groups:
                # Drop columns with all NaNs
                group.dropna(axis=1, how="all", inplace=True)

                cei_column = group[
                    group.columns[group.columns.str.contains(cei)]
                ].columns
                max_cei_col = max(cei_column, key=len)
                self.stage_info = stages.get_stage_information_dict(
                    max_cei_col, self.method
                )

                # Subset dataframes to columns that contain self.stage_info["Stage_ID"]
                all_columns = group.columns[
                    group.columns.str.contains(self.stage_info["Stage_ID"])
                ].tolist()

                try:
                    group = group[
                        self.fixed_columns
                        + [self.target]
                        + self.statistics_columns
                        + all_columns
                    ]
                except:
                    continue
                # rename all_columns to self.stage_info["CEI"]
                group.rename(
                    columns={
                        col: stages.get_stage_information_dict(col, self.method)["CEI"]
                        for col in all_columns
                    },
                    inplace=True,
                )

                frames.append(group)

            df = pd.concat(frames)
        else:
            # HACK: Get feature name with GD4 in it to extract first and last stage id and name
            cei_column = df[df.columns[df.columns.str.contains(cei)]].columns
            # Select the longest string in cei_column
            cei_col = max(cei_column, key=len)
            self.stage_info = stages.get_stage_information_dict(cei_col, self.method)

        """ Only select those features that span a single time-period """
        """ e.g. vDTR_7_6 is ok but vDTR_7_6_5 is not """
        if self.use_single_time_period_as_feature:
            df = stages.select_single_time_period_features(df)

        # Change column name
        # e.g. 'vDTR_7_6_5_4_3_2_1_37_36_35_34_33_32_31' to 'vDTR Mar 1-Oct 27'
        df = stages.update_feature_names(df, self.method)

        all_cei_columns = self.get_cei_column_names(df)
        # Fill in any missing values with 0
        df.loc[:, all_cei_columns].fillna(0, inplace=True)

        df = fe.compute_last_year_yield(df, self.target)

        df = fe.compute_median_statistics(
            df, self.all_seasons_with_yield, self.number_median_years, self.target
        )

        if self.median_area_as_feature:
            df = fe.compute_median_statistics(
                df, self.all_seasons_with_yield, self.number_median_years, "Area (ha)"
            )

        if self.lag_yield_as_feature:
            df = fe.compute_lag_yield(
                df, self.all_seasons_with_yield, self.number_lag_years, self.target
            )

        if self.analogous_year_yield_as_feature:
            df = fe.compute_analogous_yield(
                df, self.all_seasons_with_yield, self.number_median_years, self.target
            )

        # Create Region_ID column based on Region column category code
        df["Region"] = df["Region"].astype("category")
        if self.cluster_strategy == "single":
            df["Region_ID"] = 1
        elif self.cluster_strategy == "individual":
            df["Region_ID"] = df["Region"].cat.codes
        elif self.cluster_strategy == "auto_detect":
            clusters_assigned = fe.detect_clusters(df, self.target)
            # Merge the cluster labels with the original DataFrame
            df = df.merge(clusters_assigned, on="Region")

            # Region_ID should be type category
            df["Region_ID"] = df["Region_ID"].astype("category")

        return df

    def execute(self):
        """

        Returns:

        """
        """ Get dataframe including all simulation stages """
        # convert self.simulation_stages to a list of strings
        _stages = []
        for stage in self.simulation_stages:
            stage = stages.convert_stage_string(stage, to_array=False)
            _stages.append(stage)

        mask = self.df_inputs["Stage_ID"].isin(_stages)
        df = self.df_inputs[mask]
        """ Select which CEI categories to use for ML """
        if "all" in self.use_ceis:
            pass
        else:
            if self.select_cei_by == "Type":
                df = df[df["Type"].isin(self.use_ceis)]
            elif self.select_cei_by == "Index":
                df = df[df["Index"].isin(self.use_ceis)]

        """ Convert this dataframe into an ML ready format and save to disk """
        df = self.create_ml_dataframe(df)
        dir_output = (
            self.dir_analysis
            / self.country
            / self.crop
            / self.model_name
            / str(self.forecast_season)
        )
        os.makedirs(dir_output, exist_ok=True)
        df.to_csv(
            dir_output / f"{self.country}_{self.crop}_{self.forecast_season}.csv",
            index=False,
        )

        # cat_features should be converted to category type
        df[self.cat_features] = df[self.cat_features].astype("category")

        """  Heatmap of correlation of various features with yield at each time step"""
        # For each time step, determine the number of occurences of each feature
        # when it is most correlated with the target for a region
        # Use this to plot a heatmap showing which features are most correlated
        # with yield at each time step
        # Add a Country Region column to df and make it lower case
        df["Country Region"] = (
            df["Country"].astype(str) + " " + df["Region"].astype(str)
        ).str.lower()

        # Join with dg based on Country Region column, only keeping rows that are in df
        # Only use geometry column from self.dg
        self.dg_country = self.dg_country[["Country Region", "geometry"]].merge(
            df[["Country Region", self.correlation_plot_groupby]],
            on="Country Region",
            how="outer",
        )

        # Add a lat and lon column to self.dg_country
        self.dg_country["lat"] = self.dg_country.centroid.y
        self.dg_country["lon"] = self.dg_country.centroid.x

        # Add lat and lon columns to df by merging on Country Region column
        df = df.merge(
            self.dg_country[["Country Region", "lat", "lon"]].drop_duplicates(),
            on="Country Region",
            how="left",
        )

        dict_kwargs = {}
        dict_kwargs["all_stages"] = self.all_stages
        dict_kwargs["target_col"] = self.target
        dict_kwargs["country"] = self.country
        dict_kwargs["crop"] = self.crop
        dict_kwargs["dir_output"] = (
            self.dir_analysis
            / self.country
            / self.crop
            / self.model_name
            / str(self.forecast_season)
        )
        dict_kwargs["forecast_season"] = self.forecast_season
        dict_kwargs["method"] = self.method
        dict_kwargs["national_correlation"] = self.national_correlation
        dict_kwargs["groupby"] = self.correlation_plot_groupby
        dict_kwargs["cluster_strategy"] = self.cluster_strategy
        dict_kwargs["dg_country"] = self.dg_country
        dict_kwargs["combined_dict"] = self.combined_dict
        dict_kwargs["plot_map"] = self.plot_map_for_correlation_plot
        dict_kwargs["correlation_threshold"] = self.correlation_threshold

        if self.spatial_autocorrelation:
            sa.compute_spatial_autocorrelation(self.df_inputs, **dict_kwargs)

        dict_selected_features = {}
        dict_best_cei = {}
        if self.correlation_plots:
            self.logger.info(f"Correlation plot for {self.country} {self.crop}")
            (
                dict_selected_features,
                dict_best_cei,
            ) = correlations.all_correlated_feature_by_time(df, **dict_kwargs)

        """ Add Yield_class column and set to NaN """
        df[f"{self.target}_class"] = np.NaN

        """ Separate into train and test datasets based on forecast_season """
        mask = df["Harvest Year"] == self.forecast_season
        self.df_train = df[~mask]
        self.df_test = df[mask]

        # Drop rows with missing values for self.target_col in df_train
        self.df_train = self.df_train.dropna(subset=[self.target])

        """ Groupby Region column and compute detrended yield """
        self.df_train[f"Detrended {self.target}"] = np.NaN
        self.df_train["Detrended Model"] = np.NaN
        self.df_train["Detrended Model Type"] = np.NaN
        group_by = ["Region"]
        groups = self.df_train.groupby(group_by)
        for key, group in groups:
            if self.check_yield_trend:
                if group[self.target].any():
                    detrended_data = trend.detrend_dataframe(
                        group, column_name=self.target, model_type="linear"
                    )
                    self.df_train.loc[
                        group.index, f"Detrended {self.target}"
                    ] = detrended_data.detrended_series
                    self.df_train.loc[
                        group.index, "Detrended Model"
                    ] = detrended_data.trend_model
                    self.df_train.loc[
                        group.index, "Detrended Model Type"
                    ] = detrended_data.model_type

            # Create categorical classes for target column
            group, new_target_column, bins = fe.classify_target(
                group, self.target, self.number_classes
            )
            self.target_bins[key[0]] = bins
            self.target_class = new_target_column
            self.df_train.loc[group.index, new_target_column] = group[new_target_column]

        # 6. Exclude years without yields from df_train
        # self.df_train = self.df_train[
        #     self.df_train["Harvest Year"].isin(self.all_seasons_with_yield)
        # ]

        """ Run ML code for each stage """
        if self.run_ml:
            self.logger.info(f"Running ML for {self.country} {self.crop}")
            setup_stages = [self.simulation_stages]
            if self.run_latest_time_period:
                # setup_stages = stages.select_stages_for_ml(setup_stages, method="latest")
                setup_stages = [setup_stages[-1]]

            num_regions = len(self.df_train["Region_ID"].unique())
            pbar = tqdm(setup_stages)
            for stage in pbar:
                pbar.set_description(
                    f"ML {num_regions} regions, {len(setup_stages)} stages"
                )
                pbar.update()

                self.loop_ml(stage, dict_selected_features, dict_best_cei)
        wandb.finish()

    def setup(self, forecast_season, model):
        """

        :param country:
        :param crop:
        :param forecast_season:
        :param model:
        """
        _str = f"{self.country} {self.crop} {model} {forecast_season}"
        config_dict = {section: dict(self.parser.items(section)) for section in self.parser.sections()}
        wandb.init(project=self.project_name, name=_str, config=config_dict)
        self.logger.info(f"Setup {_str}")

        self.forecast_season = forecast_season
        self.model_name = model
        self.experiment_name = self.parser.get("ML", "experiment_name")
        self.ml_model = self.parser.getboolean(self.model_name, "ML_model")
        self.select_cei_by = self.parser.get(self.model_name, "select_cei_by")
        self.use_ceis = ast.literal_eval(self.parser.get(self.model_name, "use_ceis"))
        self.model_names = ast.literal_eval(self.parser.get(self.country, "models"))
        self.optimize = self.parser.getboolean(self.country, "optimize")
        self.fraction_loocv = self.parser.getfloat(self.country, "fraction_loocv")
        self.all_seasons = self.df_inputs["Harvest Year"].unique()

        # If model_type if regression then set classify_target to False
        if self.model_type == "REGRESSION" and self.classify_target:
            raise ValueError("Model type is regression but classify_target is True")
        elif self.model_type == "CLASSIFICATION" and not self.classify_target:
            raise ValueError(
                "Model type is classification but classify_target is False"
            )

        """ For a classification model, only catboost is supported currently """
        if self.model_type == "CLASSIFICATION":
            self.do_xai = False
            self.alpha = self.parser.getfloat("ML", "alpha")
            self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
            self.estimate_ci_for_all = self.parser.getboolean(
                "ML", "estimate_ci_for_all"
            )
            self.check_yield_trend = False
            if self.model_name == "ngboost":
                # Remove Region from cat_features as it is object type
                self.cat_features = [
                    col for col in self.cat_features if col != "Region"
                ]
        elif self.model_type == "REGRESSION":
            """If not using a ML model then set XAI and CI to False"""
            if not self.ml_model or self.model_name in ["linear", "gam", "merf"]:
                self.do_xai = False
                self.estimate_ci = False
                self.check_yield_trend = False
                self.estimate_ci_for_all = False
            elif self.model_name in ["cumulative_1", "cumulative_2", "cumulative_3"]:
                self.correlation_plots = False
                self.lag_yield_as_feature = False
                self.median_yield_as_feature = False
                self.median_area_as_feature = False
                self.analogous_year_yield_as_feature = False
                self.last_year_yield_as_feature = False
                self.include_lat_lon_as_feature = False
                self.do_xai = False
                self.estimate_ci = False
                self.estimate_ci_for_all = False
                self.check_yield_trend = True
                self.cluster_strategy = "single"
                self.select_cei_by = "Index"
                self.use_cumulative_features = True
            elif self.model_name in ["oblique", "ydf"]:
                self.do_xai = False
                self.estimate_ci = False
                # Remove Region from cat_features as it is object type
                self.cat_features = [
                    col for col in self.cat_features if col != "Region"
                ]
            elif self.model_name == "ngboost":
                self.do_xai = False
                self.alpha = self.parser.getfloat("ML", "alpha")
                self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
                self.estimate_ci_for_all = self.parser.getboolean(
                    "ML", "estimate_ci_for_all"
                )
                # Remove Region from cat_features as it is object type
                self.cat_features = [
                    col for col in self.cat_features if col != "Region"
                ]
            else:
                self.do_xai = self.parser.getboolean("ML", "do_xai")
                self.estimate_ci = self.parser.getboolean("ML", "estimate_ci")
                self.estimate_ci_for_all = self.parser.getboolean(
                    "ML", "estimate_ci_for_all"
                )
                self.alpha = self.parser.getfloat("ML", "alpha")
                self.check_yield_trend = self.parser.getboolean(
                    "ML", "check_yield_trend"
                )

        # 1. Get all seasons with yield, these are the seasons for which Yield is available
        self.all_seasons_with_yield = self.df_inputs[
            self.df_inputs[self.target].notna()
        ]["Harvest Year"].unique()

        if self.method.endswith("_r"):
            if self.forecast_season == self.today_year:
                mask = self.df_inputs["Harvest Year"] == self.forecast_season
                self.all_stages = self.df_inputs[mask]["Stage_ID"].unique()
            else:
                self.all_stages = self.df_inputs["Stage_ID"].unique()
        else:
            raise NotImplementedError(f"Method {self.method} not implemented")

        # Create a list of numpy arrays, for each string in _stages,
        # create a numpy array by splitting by _ and converting to int
        # then store in self.simulation_stages
        # e.g. _stages = ['13_12_11', '13_12_11_10', '13_12_11_10_9']
        # then self.simulation_stages = [array([13, 12, 11]), array([13, 12, 11, 10]), array([13, 12, 11, 10, 9])]
        # Drop stages in self.all_stages that do not have _ in them
        self.all_stages = [element for element in self.all_stages if "_" in element]

        self.simulation_stages = [
            np.array([int(stage) for stage in s.split("_")]) for s in self.all_stages
        ]

        self.name_shapefile = self.parser.get(self.country, "boundary_file")
        self.admin_zone = self.parser.get(self.country, "admin_zone")
        self.dg = gp.read_file(
            self.dir_shapefiles / self.name_shapefile,
            engine="pyogrio",
        )

        if "ADMIN0" in self.dg.columns:
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

        if self.country == "nepal":
            self.dg["ADM0_NAME"] = "nepal"
            self.dg["Country Region"] = self.dg["ADM0_NAME"] + " " + self.dg["PR_NAME"]
        elif self.admin_zone == "admin_1":
            self.dg["Country Region"] = (
                self.dg["ADM0_NAME"] + " " + self.dg["ADM1_NAME"]
            )
        elif self.country == "illinois":
            self.dg["ADM0_NAME"] = "illinois"
            self.dg["Country Region"] = self.dg["ADM0_NAME"] + " " + self.dg["NAME"]
        else:
            self.dg["Country Region"] = (
                self.dg["ADM0_NAME"] + " " + self.dg["ADM2_NAME"]
            )
        self.dg["Country Region"] = self.dg["Country Region"].str.lower()
        self.dg_country = self.dg[
            self.dg["ADM0_NAME"].str.lower().str.replace(" ", "_") == self.country
        ]

    def read_data(self, country, crop, season):
        """

        Args:
            country:
            crop:
            season:

        Returns:

        """
        self.logger.info(f"Reading data for {country} {crop} {season}")

        self.country = country
        self.crop = crop

        """Figure out path to file containing CEI data"""
        admin_zone = self.parser.get(country, "admin_zone")
        country_str = country.title().replace("_", " ")
        crop_str = crop.title().replace("_", " ")

        dir_statistics = self.dir_output / "cei" / "indices" / self.method / "global"
        os.makedirs(dir_statistics, exist_ok=True)
        file = (
            dir_statistics / f"{country_str}_{crop_str}_statistics_s1_{self.method}.csv"
        )

        """ Add area, yield and prod stats from either GEOGLAM or FEWSNET warehouse database"""
        if not os.path.exists(file) or self.update_input_file:
            _dir_country = (
                self.dir_output
                / "cei"
                / "indices"
                / self.method
                / admin_zone
                / country
                / crop
            )
            file_name = f"{country}_{crop}_s1*.csv"
            all_files = _dir_country.glob(file_name)
            # TODO ignore file with _2000 in its name
            all_files = [f for f in all_files if "_2000" not in f.name]

            # Assert that all_files is not empty
            assert all_files, f"No files found in {_dir_country} with {file_name}"

            self.df_inputs = pd.concat(
                (pd.read_csv(f) for f in all_files), ignore_index=True
            )

            self.df_inputs = stats.add_statistics(
                self.dir_condition / "yield",
                self.df_inputs,
                country_str,
                crop_str,
                admin_zone,
                [self.target] + self.statistics_columns,
                self.method,
            )
            """ Add information on starting and ending time period for each stage"""
            self.df_inputs = stages.add_stage_information(self.df_inputs, self.method)

            self.df_inputs.to_csv(file, index=False)
        else:
            self.df_inputs = pd.read_csv(file)

        # Rename target column
        if self.rename_target:
            self.df_inputs.rename(
                columns={self.target: self.new_name_target}, inplace=True
            )
            self.target = "Yield"
