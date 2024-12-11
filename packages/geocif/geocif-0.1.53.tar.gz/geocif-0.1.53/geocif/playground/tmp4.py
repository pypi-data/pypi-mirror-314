# Instructions for installing required packages:
# 1. Install R: You need R installed on your system. You can download it from https://cran.r-project.org/.
# 2. Install Python packages:
#    - rpy2: `pip install rpy2`
#    - pandas: `pip install pandas`
#    - numpy: `pip install numpy`
#    - joblib: `pip install joblib`
#    - tqdm: `pip install tqdm`
#    - catboost: `pip install catboost`
#    - matplotlib: `pip install matplotlib`
# 3. Install R packages:
#    - Open R console and run:
#      `install.packages("mgcv")`
#      `install.packages("stats")`

import os

# Set R_HOME environment variable before importing rpy2
os.environ["R_HOME"] = f"{os.environ['CONDA_PREFIX']}\Lib\R"

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd
import numpy as np
import random
import re
from joblib import Parallel, delayed
from tqdm import tqdm
from catboost import CatBoostRegressor, Pool
import matplotlib.pyplot as plt


def setup_environment():
    """Set up environment and activate pandas-to-R dataframe conversion."""
    pandas2ri.activate()


def import_r_packages():
    """Import necessary R packages."""
    stats = importr('stats')
    mgcv = importr('mgcv')
    return stats, mgcv


def read_and_clean_data(filepath):
    """Read CSV data and perform initial cleaning."""
    df = pd.read_csv(filepath)
    df = df[df['Year'] > 2002].dropna()
    return df


def fit_county_level_trend_model(df, stats):
    """Fit county-level trend model and compute yield anomaly."""
    trend_models = {}
    for fips in tqdm(df['FIPS'].unique(), desc="Fitting County-Level Trend Model"):
        county_data = df[df['FIPS'] == fips]
        trend_model = stats.lm('yield ~ Year', data=pandas2ri.py2rpy(county_data))
        trend_models[fips] = trend_model
        df.loc[df['FIPS'] == fips, 'county_trend'] = np.array(stats.predict(trend_model))
    df['yield_anomaly'] = df.apply(
        lambda row: row['yield'] - row['county_trend'] if pd.notna(row['county_trend']) else np.nan, axis=1)

    return df


def remove_columns(df):
    """Remove specific biweek columns based on regex pattern."""
    cols_to_remove = [col for col in df.columns if
                      re.search(r'biweek(1|2|3|4|5|6|7|8|17|18|19|20|21|22|23|24|25|26)$', col)]
    return df.drop(columns=cols_to_remove)


def filter_midwest_states(df):
    """Filter for Midwest states and years before 2017."""
    df['states'] = df['FIPS'].apply(lambda x: int(float(x)) // 1000)
    MW_states = [17, 18]  #, 19, 20, 26, 27, 29, 31, 38, 39, 46, 55]
    df = df[df['states'].isin(MW_states) & (df['Year'] < 2017)]
    return df.drop(columns=['states'])


def construct_formula(df):
    """Construct model formula with spline and polynomial terms."""
    predictors = [col for col in df.columns if re.search(r'biweek', col)]
    spline_predictors = [pred for pred in predictors if re.search(r'^esi|^pr', pred)]
    poly_predictors = [pred for pred in predictors if re.search(r'^gcvi', pred)]

    spline_terms = ' + '.join([f's({pred}, bs = "cr", k = 3)' for pred in spline_predictors])
    poly_terms = ' + '.join([f'poly({pred}, degree = 2)' for pred in poly_predictors])

    all_terms = ' + '.join([spline_terms, poly_terms])
    formula_str = f'yield_anomaly ~ {all_terms}'
    random_effects = ' + s(FIPS, bs = "re")'
    formula_str_gamm = formula_str + random_effects
    return ro.r('as.formula')(formula_str), ro.r('as.formula')(formula_str_gamm)


def train_and_predict_r_gam(year, df, formula, mgcv):
    """Train GAM R model for a specific year and make predictions."""
    df_train = df[df['Year'] != year].copy()
    df_test = df[df['Year'] == year].copy()

    df_train['FIPS'] = pd.Categorical(df_train['FIPS'].astype(str))
    df_test['FIPS'] = pd.Categorical(df_test['FIPS'].astype(str))
    df_test = df_test[df_test['FIPS'].isin(df_train['FIPS'])]

    df_train = df_train.dropna(axis=1, how='all')
    df_test = df_test.loc[:, df_test.columns.isin(df_train.columns)]

    try:
        model = mgcv.bam(formula, data=pandas2ri.py2rpy(df_train))
        predicted = mgcv.predict_gam(model, pandas2ri.py2rpy(df_test), se=True)
    except Exception as e:
        print(f"Error fitting or predicting for Year {year} with GAM: {e}")
        return pd.DataFrame(columns=['fit', 'se.fit', 'Year', 'obs', 'yield_anomaly', 'county_trend', 'FIPS', 'model'])

    pred_df = pd.DataFrame({'fit': np.array(predicted[0]), 'se.fit': np.array(predicted[1])})
    pred_df['Year'] = year
    pred_df['obs'] = df_test['yield'].values
    pred_df['yield_anomaly'] = df_test['yield_anomaly'].values
    pred_df['county_trend'] = df_test['county_trend'].values
    pred_df['FIPS'] = df_test['FIPS'].values
    pred_df['model'] = 'GAM'

    return pred_df


def train_and_predict_r_gamm(year, df, formula, mgcv):
    """Train GAMM R model for a specific year and make predictions."""
    df_train = df[df['Year'] != year].copy()
    df_test = df[df['Year'] == year].copy()

    df_train['FIPS'] = pd.Categorical(df_train['FIPS'].astype(str))
    df_test['FIPS'] = pd.Categorical(df_test['FIPS'].astype(str))
    df_test = df_test[df_test['FIPS'].isin(df_train['FIPS'])]

    df_train = df_train.dropna(axis=1, how='all')
    df_test = df_test.loc[:, df_test.columns.isin(df_train.columns)]

    try:
        model = mgcv.gamm(formula, random=ro.r('list(FIPS = ~1)'), data=pandas2ri.py2rpy(df_train))
        predicted = mgcv.predict_gam(model.rx2('gam'), pandas2ri.py2rpy(df_test), se=True)
    except Exception as e:
        print(f"Error fitting or predicting for Year {year} with GAMM: {e}")
        return pd.DataFrame(columns=['fit', 'se.fit', 'Year', 'obs', 'yield_anomaly', 'county_trend', 'FIPS', 'model'])

    pred_df = pd.DataFrame({'fit': np.array(predicted[0]), 'se.fit': np.array(predicted[1])})
    pred_df['Year'] = year
    pred_df['obs'] = df_test['yield'].values
    pred_df['yield_anomaly'] = df_test['yield_anomaly'].values
    pred_df['county_trend'] = df_test['county_trend'].values
    pred_df['FIPS'] = df_test['FIPS'].values
    pred_df['model'] = 'GAMM'

    return pred_df


def train_and_predict_catboost(year, df, feature_importances=[]):
    """Train CatBoost model for a specific year and make predictions."""
    df_train = df[df['Year'] != year].copy()
    df_test = df[df['Year'] == year].copy()

    df_train['FIPS'] = pd.Categorical(df_train['FIPS'].astype(str))
    df_test['FIPS'] = pd.Categorical(df_test['FIPS'].astype(str))
    df_test = df_test[df_test['FIPS'].isin(df_train['FIPS'])]

    df_train = df_train.dropna(axis=1, how='all')
    df_test = df_test.loc[:, df_test.columns.isin(df_train.columns)]

    features = [col for col in df_train.columns if col not in ['yield', 'yield_anomaly', 'county_trend', 'Year', 'FIPS']]
    X_train = df_train[features]
    y_train = df_train['yield_anomaly']
    X_test = df_test[features]

    try:
        model = CatBoostRegressor(iterations=2000, depth=6, learning_rate=0.1, loss_function='RMSE', verbose=0, random_state=42)
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
        feature_importances.append(model.get_feature_importance())
    except Exception as e:
        print(f"Error fitting or predicting for Year {year} with CatBoost: {e}")
        return pd.DataFrame(columns=['fit', 'Year', 'obs', 'yield_anomaly', 'county_trend', 'FIPS', 'model'])

    pred_df = pd.DataFrame({'fit': predicted})
    pred_df['Year'] = year
    pred_df['obs'] = df_test['yield'].values
    pred_df['yield_anomaly'] = df_test['yield_anomaly'].values
    pred_df['county_trend'] = df_test['county_trend'].values
    pred_df['FIPS'] = df_test['FIPS'].values
    pred_df['model'] = 'CatBoost'

    return pred_df

def calculate_metrics(out_df):
    """Calculate MAPE, MSE, and R-squared by year and create a summary dataframe."""
    # Convert from yield anomaly back to original yield at the FIPS level
    out_df['predicted_yield'] = out_df.apply(lambda row: row['fit'] + row['county_trend'] if pd.notna(row['county_trend']) else np.nan, axis=1)
    out_df['actual_yield'] = out_df.apply(lambda row: row['yield_anomaly'] + row['county_trend'] if pd.notna(row['county_trend']) else np.nan, axis=1)

    metrics = []
    for (year, model), group in out_df.groupby(['Year', 'model']):
        mape = np.mean(np.abs((group['actual_yield'] - group['predicted_yield']) / group['actual_yield'])) * 100
        mse = np.mean((group['actual_yield'] - group['predicted_yield']) ** 2)
        r_squared = np.corrcoef(group['predicted_yield'], group['actual_yield'])[0, 1] ** 2
        fips_code = group['FIPS'].unique()[0]
        state_name = f"State_{fips_code}"  # Placeholder for state name, replace with actual mapping if available
        metrics.append({'Year': year, 'Model': model, 'State': state_name, 'FIPS': fips_code, 'MAPE': mape, 'MSE': mse, 'R-squared': r_squared})
    metrics_df = pd.DataFrame(metrics)
    print(metrics_df)
    return metrics_df

def plot_model_performance(metrics_df):
    """Produce plots comparing model performance by year and state."""
    plt.figure(figsize=(12, 8))
    for metric in ['MAPE', 'MSE', 'R-squared']:
        plt.clf()
        for model in metrics_df['Model'].unique():
            subset = metrics_df[metrics_df['Model'] == model]
            plt.plot(subset['Year'], subset[metric], label=f'{model} - {metric}')
        plt.xlabel('Year')
        plt.ylabel(metric)
        plt.title(f'Model Comparison by Year - {metric}')
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    setup_environment()
    stats, mgcv = import_r_packages()

    df = read_and_clean_data(r'D:\Users\ritvik\projects\GEOGLAM\Output\ml\analysis\August_27_2024\usa.csv')
    df = fit_county_level_trend_model(df, stats)
    df = remove_columns(df)
    df = filter_midwest_states(df)
    df['FIPS'] = df['FIPS'].astype(str)

    formula_gam, formula_gamm = construct_formula(df)
    years = np.sort(df['Year'].unique())

    # Train R models (GAM and GAMM) and CatBoost model
    gam_results = [train_and_predict_r_gam(year, df, formula_gam, mgcv) for year in tqdm(years, desc="Training GAM Model")]
    gamm_results = [train_and_predict_r_gamm(year, df, formula_gamm, mgcv) for year in tqdm(years, desc="Training GAMM Model")]
    catboost_models = []
    feature_importances = []
    # catboost_results = []
    # for year in tqdm(years, desc="Training CatBoost Model"):
    #     result = train_and_predict_catboost(year, df, feature_importances)
    #     catboost_results.append(result)

    # Plot feature importance for CatBoost model (averaged over all iterations)
    # if feature_importances:
    #     avg_feature_importance = np.mean(feature_importances, axis=0)
    #     plt.figure(figsize=(10, 8))
    #     plt.barh(df.columns[df.columns.isin(features)], avg_feature_importance, align='center')
    #     plt.xlabel('Feature Importance')
    #     plt.title('Average CatBoost Feature Importance')
    #     plt.gca().invert_yaxis()
    #     plt.show()

    # Combine results
    out_df = pd.concat(gam_results + gamm_results, ignore_index=True)

    # Calculate metrics and plot model performance
    metrics_df = calculate_metrics(out_df)
    plot_model_performance(metrics_df)
    print(metrics_df)
    # Save results to a CSV file in long format
    out_df.to_csv(r'D:\Users\ritvik\projects\GEOGLAM\Output\ml\analysis\model_results_long_format.csv', index=False)

if __name__ == "__main__":
    main()
