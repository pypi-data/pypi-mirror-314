import os

import icclim
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path

from geocif import utils
import definitions as di


def adjust_dataframes(df):
    unique_years = df["time"].dt.year.unique()
    if len(unique_years) == 1:
        pass
    else:
        # Dynamically set the desired start date to the first day of the
        # year following the earliest date in the dataset
        earliest_year = df["time"].dt.year.min()
        desired_start_year = earliest_year + 1
        desired_start_date_dynamic = pd.Timestamp(f"{desired_start_year}-01-01")

        # Calculate the difference between the earliest date in the dataset and the desired start date
        min_date_new = df["time"].min()
        date_difference_dynamic = desired_start_date_dynamic - min_date_new

        # Adjust all dates in the 'time' column forward by the calculated difference
        df["time"] = df["time"] + date_difference_dynamic

    return df


def df_to_xarray(vals):
    """

    :param df:
    :param vals:
    :param harvest_year:
    :return:
    """
    vals_ix = vals.set_index(["lat", "lon", "time"])
    dx = vals_ix.to_xarray()

    # Add attributes to dx
    dx["tasmax"].attrs["units"] = "C"
    dx["tasmin"].attrs["units"] = "C"
    dx["tg"].attrs["units"] = "C"
    dx["pr"].attrs["units"] = "mm/day"
    dx["snd"].attrs["units"] = "cm"

    # Missing value for tasmax, tasmin, tg, pr and snd is NaN
    for var in ["tasmax", "tasmin", "tg", "pr", "snd"]:
        dx[var].attrs["missing_value"] = np.nan

    return dx, vals_ix


def get_icclim_dates(df_all_years, df_harvest_year):
    """

    :param df_all_years:
    :param df_harvest_year:
    :return:
    """
    from dateutil.relativedelta import relativedelta

    # Starting and ending dates for base period
    start_br = str(df_all_years.index[0][2] + relativedelta(years=1))
    # end_br should be 2 years behind its current value to ensure that
    # all phenological seasons are present in the base period
    end_br = str(df_all_years.index[-1][2] - relativedelta(years=2))

    # Assert that each season in df_all_years has all phenological stages
    # This is done to ensure that the base period has all phenological stages
    # so that the indices can be computed for the entire season
    # assert all(
    #     df_all_years.groupby(["adm0_name", "Season"])
    #     .filter(lambda x: all(i in x["crop_cal"].values for i in PHENOLOGICAL_STAGES))
    #     .Season.value_counts()
    #     == 1
    # )

    # Starting and ending dates for time range period
    start_tr = np.datetime_as_string(df_harvest_year.time.values[0])
    end_tr = np.datetime_as_string(df_harvest_year.time.values[-1])

    return start_br, end_br, start_tr, end_tr


def compute_indices(df_time_period, df_base_period, index_name):
    """
    Function that computes the climate indices using icclim

    :param df_time_period:
    :param df_base_period:
    :param index_name:
    :return:
    """
    ds = None

    unique_years = df_time_period["time"].dt.year.unique()
    if len(unique_years) > 1:
        df_time_period = adjust_dataframes(df_time_period)
        df_base_period = adjust_dataframes(df_base_period)

    # icclim runs on xarray dataset so convert dataframe to one
    dx, vals_ix = df_to_xarray(df_base_period)

    # Get start and end dates for base period and time range
    # base period: Temporal range of the reference period
    # time range: Temporal range of the period for which the index is computed
    # Reference: https://icclim.readthedocs.io/en/stable/references/ecad_functions_api.html#icclim._generated_api.spi3
    start_br, end_br, start_tr, end_tr = get_icclim_dates(vals_ix, df_time_period)

    # Create a string like so ("season", ("19 july", "14 august")) where start_tr and end_tr are dates
    # By specifying start and end dates, icclim will compute the index for the entire season
    slice_mode = (
        "season",
        (
            f"{df_time_period.time.iloc[0].strftime('%d %B')}",
            f"{df_time_period.time.iloc[-1].strftime('%d %B')}",
        ),
    )

    try:
        # SPI calculations fail if slice_mode is specified
        if index_name in ["SPI3", "SPI6"]:
            ds = icclim.index(
                index_name=index_name,
                in_files=dx,
                base_period_time_range=[start_br, end_br],
                time_range=[start_tr, end_tr],
            )
        else:
            ds = icclim.index(
                index_name=index_name,
                in_files=dx,
                base_period_time_range=[start_br, end_br],
                time_range=[start_tr, end_tr],
                slice_mode="year",
            )
    except Exception as e:
        print(e)
        print(
            f"Error computing {index_name} for {start_tr} to {end_tr},"
            f" {df_base_period.adm0_name.unique()}"
            f" {df_base_period.adm1_name.unique()}"
        )

    return ds


class CEIs:
    def __init__(
        self, parser, process_type, file_path, file_name, admin_zone, method, harvest_year, redo
    ):
        self.parser = parser
        self.process_type = process_type
        self.file_path = file_path
        self.file_name = file_name
        self.admin_zone = admin_zone
        self.method = method
        self.harvest_year = harvest_year
        self.redo = redo

        # Intitialize variables later
        self.country = None
        self.crop = None
        self.season = None

        # Directories
        self.dir_output = None
        self.dir_intermediate = None

        # Dataframes
        self.df_country_crop = pd.DataFrame()
        self.df_harvest_year = pd.DataFrame()

        # Paths
        self.dir_base = Path(self.parser.get("PATHS", "dir_output"))

    def get_unique_country_name(self, df=None, col="adm0_name"):
        """

        Args:
            df:

        Returns:

        """
        if not df:
            df = self.df_harvest_year

        if not df.empty:
            self.country = df[col].unique()[0].lower().replace(" ", "_")
        else:
            raise ValueError("Dataframe is empty")

    def add_season_information(self, df):
        """
        Add season information to dataframe
        :param df:
        :param method:
        :return:
        """
        grps = df.groupby(["adm1_name", "Season"])

        frames = []
        for key, df_adm1_season in grps:
            if self.method == "fraction_season":
                step = 10

                # Get the number of days in the season
                N = len(df_adm1_season)

                # Create a column called fraction_season in df_adm1_season
                # Values in fraction_season start from 10 and go upto 100, with increments of 10
                # each covering a 10th of the season
                df_adm1_season["fraction_season"] = (
                    np.linspace(10, 100 + step, N + 1) // step * step
                )[:-1]
            elif self.method in ["dekad", "dekad_r"]:
                df_adm1_season[self.method] = df_adm1_season.Doy // 10 + 1
            elif self.method in ["biweekly", "biweekly_r"]:
                df_adm1_season.loc[:, self.method] = df_adm1_season.apply(utils.compute_biweekly_index, axis=1)
            elif self.method in ["monthly", "monthly_r"]:
                df_adm1_season.loc[:, self.method] = df_adm1_season["Month"]

            frames.append(df_adm1_season)

        df = pd.concat(frames)

        return df

    def preprocess_input_df(self, vi_var="ndvi"):
        """

        :return:
        """
        df = pd.read_csv(self.file_path)  # , engine="pyarrow")

        # Do a groupby based on adm1_name and Season, drop all Seasons for
        # which all PHENOLOGICAL_STAGES are not present in the crop_cal column
        # This helps with index calculation later by ensuring that only data from full
        # seasons are used
        # df = df.groupby(["adm1_name", "Season"]).filter(
        #    lambda x: all(i in x["crop_cal"].values for i in PHENOLOGICAL_STAGES)
        # )

        # assign lat and lon value to satisfy icclim
        df["lat"] = 0
        df["lon"] = 0

        # Remove rows where crop_cal is "" or " "
        df = df[df["crop_cal"] != " "]
        df = df[df["crop_cal"] != ""]

        # Convert each element of crop_cal column to float
        df["crop_cal"] = df["crop_cal"].astype(float)

        # Drop all rows where crop_cal is not 1, 2 or 3
        df = df[df["crop_cal"].isin(di.PHENOLOGICAL_STAGES)]

        # Assert that 0 or NaN values are not present in crop_cal column
        assert df["crop_cal"].isnull().sum() == 0
        assert (df["crop_cal"] == 0).sum() == 0

        if "datetime" not in df.columns:
            # Use Year and day of year to get datetime
            df["datetime"] = pd.to_datetime(
                df["year"].astype(str) + df["JD"].astype(str), format="%Y%j"
            )

        # convert datetime column to datetime format
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Compute area proxy by multiplying tot_pix with mean_crop
        df["Area"] = df["tot_pix"] * df["mean_crop"]

        df.loc[:, "snow"] = np.NaN

        df.loc[:, "Harvest Year"] = self.harvest_year

        # rename datetime to time, cpc_tmax to tasmax, cpc_tmin to tasmin
        # cpc_precip to pr, chirps to pr
        df = df.rename(
            columns={
                "original_yield": "yield",
                "datetime": "time",
                "JD": "Doy",
                "cpc_tmax": "tasmax",
                "cpc_tmin": "tasmin",
                "cpc_precip": "pr",
                "chirps": "pr",
                "snow": "snd",
                "esi_4wk": "esi_4wk",
                "region": "adm1_name",
            }
        )

        # Replace NaN values in snd column with 0
        df["snd"] = df["snd"].fillna(0)

        # compute daily mean temperature tas
        df["tg"] = (df["tasmax"] + df["tasmin"]) / 2

        df = df[
            [
                "lat",
                "lon",
                "adm0_name",
                "adm1_name",
                "Harvest Year",
                "Month",
                "Day",
                "Doy",
                "Season",
                "Area",
                "crop_cal",
                "time",
                "tasmax",
                "tasmin",
                "tg",
                "pr",
                "snd",
                vi_var,
                "esi_4wk",
            ]
        ]

        # Loop over each adm1_name and Season combination
        # Divide the entire Season into 10 equal parts, name the column fraction_season
        # and assign the value of the fraction to it, with all the values in each of the 10 parts being the same
        # e.g. if a season has 100 days, then the first 10 days will have a value of 10, the next 10 days will have a
        # value of 20 and so on
        # This is done to ensure that the indices are computed for the entire season
        # and not just for the phenological stages
        if self.method in [
            "fraction_season",
            "dekad",
            "dekad_r",
            "biweekly",
            "biweekly_r",
            "monthly",
            "monthly_r",
        ]:
            df = self.add_season_information(df)

        if "ndvi" in df.columns:
            # Descale the ndvi column by subtracting 50 and dividing by 200
            if df["ndvi"].max() > 1:
                df["ndvi"] = (df["ndvi"] - 50) / 200

        # Exclude all years before 2001
        df = df[df["Season"] >= 2001]

        return df

    def filter_data_for_harvest_year(self):
        """

        Args:
            df:
            harvest_year:

        Returns:

        """
        mask = self.df_country_crop["Season"] == self.harvest_year
        df_filtered = self.df_country_crop[mask]
        df_filtered = df_filtered[df_filtered["time"] <= pd.to_datetime("today")]

        return df_filtered

    def prepare_directories(self):
        """

        Args:

        Returns:

        """
        self.dir_output = utils.create_output_directory(
            self.method, self.admin_zone, self.country, self.crop, self.dir_base
        )

        self.dir_intermediate = (
            self.dir_base
            / "cei"
            / "input"
            / self.method
            / self.admin_zone
            / self.country
        )

        os.makedirs(self.dir_output, exist_ok=True)
        os.makedirs(self.dir_intermediate, exist_ok=True)

    def manage_existing_files(self):
        """

        Args:

        Returns:

        """
        intermediate_file = (
            self.dir_intermediate
            / f"{self.country}_{self.crop}_s{self.season}_{self.harvest_year}.csv"
        )
        cei_file = (
            self.dir_output
            / f"{self.country}_{self.crop}_s{self.season}_{self.harvest_year}.csv"
        )
        current_year = pd.Timestamp.now().year

        if not self.redo:
            mask_year = self.harvest_year < current_year - 1

            if os.path.isfile(cei_file) and mask_year:
                return None

        return intermediate_file

    def process_data_by_region_and_stage(self):
        df_region_and_stage = pd.DataFrame()
        groups = self.df_country_crop.groupby(["adm0_name", "adm1_name"])

        frames_region_and_stage = []
        pbar = tqdm(groups)
        for key, df_group in pbar:
            pbar.set_description(f"Processing {key[0]} {key[1]}")
            pbar.update()

            _frames = self.process_group(df_group, key)
            frames_region_and_stage.append(_frames)

        if len(frames_region_and_stage):
            df_region_and_stage = pd.concat(frames_region_and_stage)

        return df_region_and_stage

    def process_group(self, df_group, key):
        """

        Args:
            df_group:
            df_harvest_year:
            method:
            key:

        Returns:

        """
        df_combine = pd.DataFrame()

        mask = self.df_harvest_year["adm1_name"] == key[1]
        df_harvest_year_region = self.df_harvest_year[mask]

        stages, valid_stages, col = self.determine_stages_and_column(
            df_harvest_year_region
        )

        extended_stages_list = []
        if self.method in ["phenological_stages", "fraction_season", "full_season"]:
            extended_stages_list = stages
        elif self.method in ["dekad_r", "biweekly_r", "monthly_r"]:
            # reverse stages
            stages = stages[::-1]

            # Generate arrays starting from each element in the original array
            for start_index in range(len(stages)):
                for end_index in range(start_index + 1, len(stages) + 1):
                    extended_stages_list.append(stages[start_index:end_index])
        else:
            start_index = 0
            for end_index in range(start_index + 1, len(stages) + 1):
                extended_stages_list.append(stages[start_index:end_index])

        frames_group = []
        for extended_stage in extended_stages_list:
            df_time_period, df_base_period = self.filter_data_for_stage(
                df_group, df_harvest_year_region, col, extended_stage
            )

            for index_name, (index_type, index_details) in di.dict_indices.items():
                processed_data = self.compute_indices_runner(
                    df_harvest_year_region,
                    df_time_period,
                    df_base_period,
                    index_name,
                    index_type,
                    index_details,
                    key,
                    extended_stage,
                )

                if not processed_data.empty:
                    frames_group.append(processed_data)

            # Compute EO indices: NDVI, ESI 4WK
            for eo_var in ["GCVI", "NDVI", "ESI4WK", "H-INDEX"]:
                # Compute EO indices
                df_eo = self.compute_eo_indices(
                    df_time_period,
                    df_harvest_year_region,
                    eo_var,
                    key,
                    extended_stage,
                )
                if not df_eo.empty:
                    frames_group.append(df_eo)

        if len(frames_group):
            df_combine = pd.concat(frames_group)

        return df_combine

    def determine_stages_and_column(self, df):
        """

        Args:
            df:
            method:

        Returns:

        """
        if self.method in ["phenological_stages", "full_season"]:
            col = "crop_cal"
            stages = df[col].unique()
            valid_stages = range(1, 4) if self.method == "phenological_stages" else None
        elif self.method == "fraction_season":
            col = "fraction_season"
            stages = df[col].unique()
            valid_stages = range(10, 110, 10)
        else:
            col = self.method
            stages = df[col].unique()
            if self.method.startswith("biweekly"):
                valid_stages = range(1, 27)
            elif self.method.startswith("dekad"):
                valid_stages = range(1, 38)
            elif self.method.startswith("monthly"):
                valid_stages = range(1, 13)

        return stages, valid_stages, col

    def filter_data_for_stage(
        self, df_all_years, df_harvest_year_region, col, stages
    ):
        """

        Args:
            df_all_years:
            df_harvest_year_region:
            col:
            idx:
            stage:
            stages:
            method:

        Returns:

        """
        if self.method in ["phenological_stages", "fraction_season"]:
            mask = df_harvest_year_region[col].isin([stages])
            df_time_period = df_harvest_year_region[mask]

            mask = df_all_years[col].isin([stages])
            df_base_period = df_all_years[mask]
        elif self.method in [
            "dekad",
            "dekad_r",
            "biweekly",
            "biweekly_r",
            "monthly",
            "monthly_r",
        ]:
            mask = df_harvest_year_region[col].isin(stages)
            df_time_period = df_harvest_year_region[mask]

            mask = df_all_years[col].isin(stages)
            df_base_period = df_all_years[mask]
        elif self.method == "full_season":
            df_time_period = df_harvest_year_region
            df_base_period = df_all_years
        else:
            raise ValueError(f"Unknown method: {self.method}")

        return df_time_period, df_base_period

    def compute_eo_indices(self, df, df_harvest_year_region, var, key, stage):
        """

        Args:
            df:
            df_harvest_year_region:
            var:
            key:
            stage:

        Returns:

        """
        # If stage is not a list then convert it to a list
        # if not isinstance(stage, list):
        #     stage = [stage]

        columns = [
            "Description",
            "CEI",
            "Country",
            "Region",
            "Area",
            "Crop",
            "Season",
            "Method",
            "Stage",
            "Harvest Year",
            "Index",
            "Type",
        ]
        if var == "NDVI":
            dict_eo = di.dict_ndvi
            vars = [var]
        elif var == "GCVI":
            dict_eo = di.dict_gcvi
            vars = [var]
        elif var == "ESI4WK":
            dict_eo = di.dict_esi4wk
            vars = [var]
        elif var == "H-INDEX":
            dict_eo = di.dict_hindex
            vars = list(dict_eo.keys())
        else:
            raise ValueError(f"Invalid var: {var}")

        df_eo = pd.DataFrame()
        frames = []
        # Compute all indices from di.dict_eo
        for iname, (itype, idesc) in dict_eo.items():
            if "NDVI" in iname:
                col_name = 'ndvi'
            elif "ESI4WK" in iname:
                col_name = 'esi_4wk'
            elif "GCVI" in iname:
                col_name = 'gcvi'
            elif "Tmax" in iname:
                col_name = "tasmax"
            elif "Tmin" in iname:
                col_name = "tasmin"
            elif "Tmean" in iname:
                col_name = "tg"
            elif "Precip" in iname:
                col_name = "pr"
            else:
                raise ValueError(f"Invalid index name: {iname}")

            if col_name not in df.columns:
                continue

            # Remove NaNs
            eo_vals = df[col_name].values
            eo_vals = eo_vals[~np.isnan(eo_vals)]

            if len(eo_vals):
                if "MIN" in iname:
                    val = np.nanmin(eo_vals)
                elif "MAX" in iname:
                    val = np.nanmax(eo_vals)
                elif "MEAN" in iname:
                    val = np.nanmean(eo_vals)
                elif "STD" in iname:
                    val = np.nanstd(eo_vals)
                elif "AUC" in iname:
                    val = np.trapz(eo_vals, dx=len(eo_vals))
                elif "H-INDEX" in iname:
                    # Multiply by 10 for h-index to work
                    val = utils.compute_h_index(eo_vals * 10)
                else:
                    raise ValueError(f"Invalid index name: {iname}")

                # Add information to df_eo
                list_df = [
                    idesc,
                    val,
                    key[0].replace("_", " ").title(),
                    key[1].replace("_", " ").title(),
                    df_harvest_year_region["Area"].unique()[0],
                    self.crop.replace("_", " ").title(),
                    self.season,
                    self.method,
                    "_".join(map(str, stage)),
                    self.harvest_year,
                    iname,
                    itype,
                ]
                frames.append(list_df)

            df_eo = pd.DataFrame(frames, columns=columns)

        return df_eo

    def process_row(
        self,
        df,
        df_harvest_year_region,
        stage,
        key,
        index_name,
        index_type,
        index_details,
    ):
        """

        :param df:
        :param df_harvest_year_region:
        :param stage:
        :param key:
        :param index_name:
        :param index_type:
        :param index_details:
        :return:
        """
        # If stage is not a list then convert it to a list
        if not isinstance(stage, list):
            stage = [stage]

        df = df[df["bounds"] == 1]
        # Exclude lat, lon, time, bounds and time_bounds columns
        df = df.drop(columns=["lat", "lon", "time", "bounds", "time_bounds"])

        # Hack: Select the first row and convert it to a dataframe
        df = df.iloc[0].to_frame().T

        df["Country"] = key[0].replace("_", " ").title()
        df["Region"] = key[1].replace("_", " ").title()
        df["Area"] = df_harvest_year_region["Area"].unique()[0]
        df["Crop"] = self.crop.replace("_", " ").title()
        df["Season"] = self.season
        df["Method"] = self.method
        df["Stage"] = "_".join(map(str, stage)) if len(stage) else None
        df["Harvest Year"] = self.harvest_year

        # Rename index_name column to value
        df = df.rename(columns={index_name: "CEI"})

        # Create a column called index and assign index_name to it
        df["Index"] = index_name
        df["Type"] = index_type
        df["Description"] = index_details

        # Rearrange dataframe to move index column upfront
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        return df

    def compute_indices_runner(
        self,
        df_harvest_year_region,
        df_time_period,
        df_base_period,
        index_name,
        index_type,
        index_details,
        key,
        stage,
    ):
        frames = []
        df_frames = pd.DataFrame()
        ds = compute_indices(df_time_period, df_base_period, index_name)

        # If method is False then set stage to None
        istage = None if self.method == "full_season" else "_".join(map(str, stage))

        if ds:
            # convert xarray dataset to dataframe and add additional information
            # such as country, region, crop, season, stage, harvest year
            df_row = ds.to_dataframe().reset_index()
            df_row = self.process_row(
                df_row,
                df_harvest_year_region,
                istage,
                key,
                index_name,
                index_type,
                index_details,
            )
            if not df_row.empty:
                frames.append(df_row)

        if len(frames):
            df_frames = pd.concat(frames)

        # start_period, end_period = utils.compute_time_periods(df_time_period, self.method, self.harvest_year)
        # if self.method.endswith("_r"):
        #     start_period, end_period = end_period, start_period
        #
        # df_frames.loc[:, "Period"] = f"{start_period}_{end_period}"

        return df_frames

    def save(self, df):
        """

        Args:
            frames:

        Returns:

        """
        fname = f"{self.country}_{self.crop}_s{self.season}_{self.harvest_year}.csv"
        df.to_csv(self.dir_output / fname, index=False)


def process(row):
    """

    Args:
        row:
            process_type: Indicates whether data includes Fall info or not
            file_path: Path to the input file
            file_name: Name of the input file
            admin_zone: Administrative zone (admin_1 or admin_2)
            method: Method to be used for computing indices e.g. full_season
            harvest_year: Year of harvest
            redo: Whether to redo the computation or not
    Returns:

    """
    parser, process_type, file_path, file_name, admin_zone, method, harvest_year, vi_var, redo = row

    obj = CEIs(
        parser, process_type, file_path, file_name, admin_zone, method, harvest_year, redo
    )

    # Read input data, convert columns to standardized names
    try:
        obj.df_country_crop = obj.preprocess_input_df(vi_var)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return

    # Filter data for harvest year
    obj.df_harvest_year = obj.filter_data_for_harvest_year()
    if obj.df_harvest_year.empty:
        return

    # Get country, crop and season names
    obj.crop, obj.season = utils.get_crop_season(file_name)
    obj.get_unique_country_name()

    # Create directories to store inermediate and final files
    obj.prepare_directories()

    # Create intermediate file from the input file
    # The intermediate file contains data for the harvest year
    intermediate_file = obj.manage_existing_files()

    if intermediate_file:
        obj.df_harvest_year.to_csv(intermediate_file, index=False)

        # Process data by region and stage and store output in a csv file
        _df = obj.process_data_by_region_and_stage()
        if not _df.empty:
            obj.save(_df)


def validate_index_definitions():
    # Check that there should not be any space in the dicionary keys in di.dict_indices,
    # di.dict_ndvi, di.dict_esi4wk, di.dict_hindex, di.dict_gcvi

    for dict_name in [di.dict_indices, di.dict_ndvi, di.dict_esi4wk, di.dict_hindex, di.dict_gcvi]:
        for key in dict_name.keys():
            if " " in key:
                raise ValueError(f"Space found in {dict_name} key: {key}")
