import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import r2_score
import statsmodels.api as sm
from pygam import LinearGAM, s, f, te

# Load data
df = pd.read_csv(r'D:\Users\ritvik\projects\GEOGLAM\Output\ml\analysis\August_27_2024\usa.csv')

# Filter Year > 2002 and drop NA values
df = df[df['Year'] > 2002]
df = df.dropna()

# Remove specific 'biweek' columns
pattern = r"biweek(1|2|3|4|5|6|7|8|17|18|19|20|21|22|23|24|25|26)$"
cols_to_remove = [col for col in df.columns if re.search(pattern, col)]
df = df.drop(columns=cols_to_remove)

# Convert 'FIPS' to string to maintain consistency
df['FIPS'] = df['FIPS'].astype(str).str.replace(r'\.0$', '', regex=True)

# Create 'states' variable
df['states'] = df['FIPS'].str.slice(0, 2).astype(int)

# Define Midwest states
MW_states = [17]  # , 18, 19, 20, 26, 27, 29, 31, 38, 39, 46, 55]

# Filter dataframe for Midwest states and Year < 2017
df = df[df['states'].isin(MW_states)]
df = df[df['Year'] < 2020]

# Remove 'states' column
df = df.drop(columns=['states'])

# Fit global trend model using statsmodels OLS
X_global = sm.add_constant(df['Year'])
global_trend_model = sm.OLS(df['yield'], X_global).fit()

# Get predictions
df['global_trend'] = global_trend_model.predict(X_global)

# Calculate yield anomaly
df['yield_anomaly'] = df['yield'] - df['global_trend']

# Define dependent variable and predictors
dependent_variable_name = 'yield_anomaly'
predictors = [col for col in df.columns if 'biweek' in col]

# Set spline and polynomial predictors
spline_predictors = [col for col in predictors if re.match(r'^(esi|pr)', col)]
poly_predictors = [col for col in predictors if re.match(r'^gcvi', col)]
poly_degree = 2

# Initialize the output DataFrame
out_df = pd.DataFrame()

# Get unique years
years = df['Year'].unique()

# Define the group cross-validator
logo = LeaveOneGroupOut()

from functools import reduce
import operator

# Loop over each year for cross-validation
for train_index, test_index in logo.split(df, groups=df['Year']):
    # Split the data
    df_train = df.iloc[train_index].copy()
    df_test = df.iloc[test_index].copy()

    # Ensure 'FIPS' levels in test are present in training
    df_test = df_test[df_test['FIPS'].isin(df_train['FIPS'])].copy()

    # Reset index
    df_train = df_train.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    # Encode 'FIPS' as a categorical variable
    df_train['FIPS'] = df_train['FIPS'].astype('category')
    df_test['FIPS'] = df_test['FIPS'].astype('category')

    # Prepare features and target
    # Spline predictors
    X_train_spline = df_train[spline_predictors]
    X_test_spline = df_test[spline_predictors]

    # Polynomial features
    # Check if there are any polynomial predictors in this fold
    if not df_train[poly_predictors].empty:
        # Fit PolynomialFeatures on df_train[poly_predictors]
        poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
        poly.fit(df_train[poly_predictors])

        # Transform both training and testing data
        X_train_poly = poly.transform(df_train[poly_predictors])
        X_test_poly = poly.transform(df_test[poly_predictors])

        # Get feature names
        poly_feature_names = poly.get_feature_names_out(poly_predictors)

        # Create DataFrames for polynomial features
        X_train_poly = pd.DataFrame(X_train_poly, columns=poly_feature_names, index=df_train.index)
        X_test_poly = pd.DataFrame(X_test_poly, columns=poly_feature_names, index=df_test.index)

        # Combine features
        X_train = pd.concat([X_train_spline.reset_index(drop=True), X_train_poly.reset_index(drop=True)], axis=1)
        X_test = pd.concat([X_test_spline.reset_index(drop=True), X_test_poly.reset_index(drop=True)], axis=1)
    else:
        # If no polynomial predictors, use only spline predictors
        X_train = X_train_spline.reset_index(drop=True)
        X_test = X_test_spline.reset_index(drop=True)
        poly_feature_names = []

    # Convert 'FIPS' to numerical codes
    df_train['FIPS_code'] = df_train['FIPS'].cat.codes
    df_test['FIPS_code'] = df_test['FIPS'].cat.codes

    # Map test 'FIPS_code' to training codes to handle unseen categories
    fips_code_mapping = dict(zip(df_train['FIPS'].cat.categories, df_train['FIPS_code']))
    # Convert 'FIPS' to numerical codes
    df_test['FIPS_code'] = df_test['FIPS'].map(fips_code_mapping)

    # Drop rows with missing 'FIPS_code' in test set
    df_test = df_test.dropna(subset=['FIPS_code'])
    df_test['FIPS_code'] = df_test['FIPS_code'].astype(int)

    # Add 'FIPS_code' to features
    X_train['FIPS_code'] = df_train['FIPS_code'].values
    X_test['FIPS_code'] = df_test['FIPS_code'].values

    # Identify the index of the 'FIPS_code' column
    fips_code_index = X_train.columns.get_loc('FIPS_code')

    # Convert pandas DataFrames to NumPy arrays
    X_train_np = X_train.to_numpy()
    X_test_np = X_test.to_numpy()

    # Target variable
    y_train = df_train[dependent_variable_name]
    y_test = df_test[dependent_variable_name]

    # Define the GAM model
    n_spline_terms = X_train_np.shape[1] - 1  # Subtract 1 for 'FIPS_code'

    # Create spline terms
    spline_terms = [s(i) for i in range(n_spline_terms)]

    # Combine spline terms into a TermList
    if spline_terms:
        spline_term_list = reduce(operator.add, spline_terms)
    else:
        spline_term_list = None  # Handle case with no spline terms

    # Factor term for 'FIPS_code' using its index
    factor_term = f(fips_code_index)

    # Combine all terms into a TermList
    if spline_term_list:
        gam_terms = spline_term_list + factor_term
    else:
        gam_terms = factor_term

    # Initialize the GAM model
    gam = LinearGAM(gam_terms)

    # Fit the model
    gam.gridsearch(X_train_np, y_train)

    # Make predictions
    y_pred = gam.predict(X_test_np)

    # Collect predictions and other relevant information
    pred_df = pd.DataFrame({
        'fit': y_pred,
        'Year': df_test['Year'].values,
        'obs': df_test['yield'].values,
        'yield_anomaly': df_test['yield_anomaly'].values,
        'global_trend': df_test['global_trend'].values,
        'FIPS': df_test['FIPS'].values
    })

    # Append to the output DataFrame
    out_df = pd.concat([out_df, pred_df], ignore_index=True)
    print(pred_df)

# Add 'state' variable to the output DataFrame
out_df['state'] = out_df['FIPS'].str.slice(0, 2).astype(int)

# Convert 'Year' to integer if it's not
out_df['Year'] = out_df['Year'].astype(int)

# Calculate R-squared values for each state and year
r2_by_state_year = out_df.groupby(['Year', 'state']).apply(
    lambda group: pd.Series({'r2': r2_score(group['yield_anomaly'], group['fit'])})
).reset_index()

# Print the R-squared values
print("R-squared by State and Year:")
print(r2_by_state_year)

# Calculate median R-squared value across all years and states
median_r2 = r2_by_state_year['r2'].median()
print(f"Median R-squared across all states and years is: {median_r2:.2f}")
