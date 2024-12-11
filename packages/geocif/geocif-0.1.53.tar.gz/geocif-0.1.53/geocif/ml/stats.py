import os
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_yld_prd(df, name_crop, cntr, region, calendar_year, region_column="ADM1_NAME"):
    """
    Example input: ('United States of America', 'Wyoming', 2000)
    Example output: 1.614
    Args:
        df:
        cntr:
        region:
        calendar_year:

    Returns:

    """
    # Get yield and production for country for specific year
    val = np.NaN

    # df.columns.values: [u'ADM0_NAME', u'ADM1_NAME', u'ADM2_NAME', u'str_ID', u'num_ID', 1990 ... 2015]
    if calendar_year in df.columns:
        # Find if country and region exists in calendar
        # mask_adm1 = (df['ADM1_NAME'].str.lower() == reg.lower())

        # if not df['ADM1_NAME'].isnull().all():
        #    df_tmp = df.loc[mask_adm1]

        df_tmp = df.copy()
        if name_crop == "rice":
            if cntr == "Viet nam":
                df_tmp = df.loc[df.Season == "Spring Paddy"]
            elif cntr == "Thailand":
                df_tmp = df.loc[df.Season == "Major Season"]
            elif cntr == "China":
                df_tmp = df.loc[df.Season == "Single-cropping and Middle-season Rice"]
            elif cntr == "India":
                df_tmp = df.loc[df.Season == "Kharif"]
        elif name_crop == "maize" and cntr in [
            "Austria",
            "Belgium",
            "Bulgaria",
            "Croatia",
            "Czech  Republic",
            "Denmark",
            "Germany",
            "Greece",
            "Hungary",
            "Italy",
            "Lithuania",
            "Luxembourg",
            "Netherlands",
            "Poland",
            "Portugal",
            "Romania",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden",
            "United Kingdom",
        ]:
            df_tmp = df.loc[df.Season == "Grain Maize and Corn-cob-mix"]
        elif name_crop == "maize" and cntr in ["France"]:
            df_tmp = df.loc[df.Season == "Green Maize"]

        if not df_tmp.empty:
            if cntr != "Vietnam":
                mask_tmp_country = (
                    df_tmp["ADM0_NAME"].str.lower() == cntr.replace("_", " ").lower()
                )
            else:
                mask_tmp_country = df_tmp["ADM0_NAME"].str.lower() == "viet nam"
            if region:
                mask_tmp_adm1 = df_tmp[region_column].str.lower() == region.lower()
            else:
                # ADM1_NAME column should be NaN to get country level stats
                mask_tmp_adm1 = df_tmp[region_column].isnull()

            # CM_Season should be 1 for the Main season
            # TODO: Make this user specified
            mask_cm_season = df_tmp["CM_Season"] == 1
            val = df_tmp.loc[mask_tmp_country & mask_tmp_adm1 & mask_cm_season][calendar_year]

            try:
                if val.isnull().all():
                    val = np.NaN
                else:
                    val = val.values[0]
            except:
                breakpoint()

        else:
            # The values[-1] is a hack to accommodate multiple types of green maize
            vals = df[calendar_year]
            val = vals.values[-1] if not vals.empty else np.NaN

    # Replace yield/production value of 0 with NaN
    val = np.NaN if val == 0.0 else val

    return val


def add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone):
    """

    Args:
        dir_stats:
        df:
        stats:
        method:
        admin_zone:

    Returns:

    """
    # Create empty columns for all the ag statistics
    for stat in stats:
        df.loc[:, stat] = np.NaN

    # Fill in the ag statistics columns with data when available
    # Compute national scale statistics
    crop = df["Crop"].unique()[0]
    # Change crop to lower case and replace space by _
    crop = crop.lower().replace(" ", "_")
    season = df["Season"].unique()[0]

    # Read in the area stats for the crop and season
    stat_file = dir_stats / f"{crop}_{season}.xlsx"

    for stat in stats:
        if os.path.isfile(stat_file):
            df_stat = pd.read_excel(stat_file, sheet_name=stat)
        else:
            continue

        # Loop over each Country, Region, harvest year combination and add the area
        grp = df.groupby(["Country", "Region", "Harvest Year"], dropna=False)
        for key, group in tqdm(grp, desc=f"Adding {stat} {method}", leave=False):
            country, region, year = key

            df_adm0 = pd.DataFrame()
            if not df_stat.empty:
                tmp = df_stat["ADM0_NAME"].str.lower()
                if country != "vietnam":  # Hack alert
                    mask_country = tmp == country.replace("_", " ").lower()
                else:
                    mask_country = tmp == "viet nam"
                df_adm0 = df_stat.loc[mask_country]

            if df_adm0.empty:
                continue

            # Get the statistic for the country and year
            region_column = "ADM2_NAME" if admin_zone == "admin_2" else "ADM1_NAME"
            val = get_yld_prd(
                df_adm0,
                crop,  # maize
                cntr=country,  # Brazil
                region=region,  # Mato Grasso
                calendar_year=year,
                region_column=region_column,
            )

            # Add the statistic to the dataframe
            df.loc[group.index, stat] = val

    return df


def add_statistics(
    dir_stats,
    df,
    country,
    crop,
    admin_zone,
    stats,
    method,
    target_col="Yield (tn per ha)",
):
    """

    Args:
        df:
        country:
        crop:
        admin_zone:
        stats:
        method:
        target_col:

    Returns:

    """
    # First check if country and crop are in the admin_crop_production.csv file
    if country == "Afghanistan":
        fn = "afghanistan.csv"
    elif country == "Illinois":
        fn = "illinois.csv"
    else:
        fn = "adm_crop_production.csv"
    df_fewsnet = pd.read_csv(dir_stats / fn, low_memory=False)
    # HACK
    if country == "Afghanistan":
        df_fewsnet.loc[:, "product"] = (
            df_fewsnet["season_name"] + " " + df_fewsnet["product"]
        )
    # Check if country and crop exist in the fewsnet database
    mask = (df_fewsnet["country"] == country) & (df_fewsnet["product"] == crop)

    if mask.sum() == 0 or country == "Zambia":
        df = add_GEOGLAM_statistics(dir_stats, df, stats, method, admin_zone)
    else:
        group_by = ["Region", "Harvest Year"]

        groups = df.groupby(group_by)

        # Define processing for each group
        def process_group(group, region, harvest_year):
            mask = (df["Region"] == region) & (df["Harvest Year"] == harvest_year)

            mask_region = df_fewsnet[admin_zone] == region
            mask_yield = (
                df_fewsnet["crop_production_system"].isin(
                    [
                        "none",
                        "Small-scale (PS)",
                        "Commercial (PS)",
                        "All (PS)",
                        "irrigated",
                        "rainfed",
                    ]
                )
                & (df_fewsnet["harvest_year"] == harvest_year)
                & (df_fewsnet["product"] == crop)
                & df_fewsnet["season_name"].isin(
                    [
                        "Main",
                        "Meher",
                        "Main harvest",
                        "Annual",
                        "Summer",
                        "Spring",
                        "Winter",
                    ]
                )
                & (df_fewsnet["indicator"].isin(["yield", "area", "production"]))
            )

            # Fetching values for each indicator
            yield_value = df_fewsnet.loc[
                mask_yield & mask_region & (df_fewsnet["indicator"] == "yield"), "value"
            ]
            area_value = df_fewsnet.loc[
                mask_yield & mask_region & (df_fewsnet["indicator"] == "area"), "value"
            ]
            prod_value = df_fewsnet.loc[
                mask_yield & mask_region & (df_fewsnet["indicator"] == "production"),
                "value",
            ]

            # Replace any inf or 0 values by NaN
            yield_value = yield_value.replace([0, np.inf, -np.inf], np.nan)
            area_value = area_value.replace([0, np.inf, -np.inf], np.nan)
            prod_value = prod_value.replace([0, np.inf, -np.inf], np.nan)

            if not yield_value.empty:
                group.loc[:, target_col] = yield_value.values[0]
                group.loc[:, "Area (ha)"] = area_value.values[0]
                group.loc[:, "Production (tn)"] = prod_value.values[0]

            return group

        # Process each group with a progress bar
        results = []
        for (region, harvest_year), group in tqdm(
            groups, total=len(groups), desc="Processing statistics", leave=False
        ):
            processed_group = process_group(group.copy(), region, harvest_year)
            results.append(processed_group)

        df = pd.concat(results)

    # Add columns for obj.stats_cols
    for col in ["Area"]:
        df.loc[:, col] = np.nan

    return df
