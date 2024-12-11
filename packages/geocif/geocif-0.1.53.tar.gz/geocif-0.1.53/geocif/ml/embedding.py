from collections import Counter

import numpy as np
import pandas as pd
from scipy.stats import pearsonr as pearsonr


def extract_regions(X, y, regions=[]):
    """
    Extract data of specific regions
    :param X: pd.DataFrame, input data
    :param y: pd.Series, target data
    :param regions: list, list of regions to extract
    """
    X, y = X.copy(), y.copy()

    indexes = X[X["Region"].isin(regions)].index
    X = X.loc[indexes, :].reset_index(drop=True)
    y = y.loc[indexes].reset_index(drop=True)

    return X, y


def _compute_correlations(X, y):
    feature_correlations = {}

    for feature in X.columns:
        # Ignore columns that are object or categorical type
        if X[feature].dtypes.name in ["object", "category"]:
            continue

        f_series = X[feature]

        # Ignore NaN values in either y and f_series
        mask = ~np.isnan(y) | ~np.isnan(f_series)
        y = y[mask]
        f_series = f_series[mask]

        if np.std(f_series) == 0 or np.std(y) == 0:
            feature_correlations[feature] = np.nan
        else:
            try:
                r = pearsonr(y, f_series)[0]
                feature_correlations[feature] = round(r, 3)
            except:
                feature_correlations[feature] = np.nan

    return feature_correlations


def find_most_common_top_feature(top_feature_by_region):
    """
    Find the most common top feature and number of occurences
    :param top_feature_by_region: dict, top feature by region
    """
    # Extract the first position values from the tuples
    values_first_position = [value[0][0] for value in top_feature_by_region.values()]

    # Count occurrences of each value and average value of the top feature
    counter = Counter(values_first_position)

    # Return the counter which contains the most
    # common top feature(s) and number of occurences
    return counter


def get_top_correlated_features(inputs, targets):
    """
    Get most correlated features for each region
    :param inputs: pd.DataFrame, input data
    :param targets: pd.Series, target data
    :param type: str, Find top feature by correlation (top), or compute all feature correlations (all)
    """
    feature_by_region = {}

    for region_id in inputs["Region"].unique():
        X, y = extract_regions(inputs, targets, regions=[region_id])

        feature_correlations = _compute_correlations(X, y)

        # Exclude any nan values
        feature_correlations = {
            k: v for k, v in feature_correlations.items() if not np.isnan(v)
        }

        if not feature_correlations:
            continue

        # Sorts the items of feature_correlations, a dictionary mapping features to their
        # correlation values, by the absolute value of the correlation in descending order,
        # resulting in a list of tuples with the feature and its corresponding correlation value
        sorted_corr_features = sorted(
            feature_correlations.items(), key=lambda x: abs(x[1]), reverse=True
        )

        top_feature, top_corr = sorted_corr_features[0]
        feature_by_region[region_id] = ([top_feature], [top_corr])

    counter = find_most_common_top_feature(feature_by_region)

    return feature_by_region, counter


def get_all_features_correlation(inputs, targets, method):
    """
    Get the top correlated features for each region
    :param inputs: pd.DataFrame, input data
    :param targets: pd.Series, target data
    :param method: str, method to use to find the top correlated features
    """
    frames = []
    for region_id in inputs["Region"].unique():
        X, y = extract_regions(inputs, targets, regions=[region_id])

        feature_correlations = _compute_correlations(X, y)

        # Exclude any nan values
        feature_correlations = {
            k: v for k, v in feature_correlations.items() if not np.isnan(v)
        }

        if not feature_correlations:
            continue

        split_keys = []
        for key in feature_correlations.keys():
            parts = key.split(" ")
            cei = parts[0]
            time_period = " ".join(parts[1:])

            split_keys.append([cei, time_period])

        # split_keys = [key.rsplit("_", 1) for key in feature_correlations.keys()]
        values = list(feature_correlations.values())

        # Creating a DataFrame
        df = pd.DataFrame(split_keys, columns=["Metric", method])
        df["Value"] = values

        # If you want to pivot the DataFrame so each metric becomes a column name and include the year as a separate column
        df_pivoted = df.pivot_table(
            index=method, columns="Metric", values="Value", aggfunc="first"
        ).reset_index()
        df_pivoted["Region"] = region_id
        # Move the 'Region' column to the front
        cols = df_pivoted.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df_pivoted = df_pivoted[cols]

        frames.append(df_pivoted)

    if len(frames):
        feature_by_region = pd.concat(frames)
    else:
        feature_by_region = pd.DataFrame()

    return feature_by_region
