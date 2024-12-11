from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
import numpy as np

np.int = np.int32
np.float = np.float64
np.bool = np.bool_

from boruta import BorutaPy
from pygam import LinearGAM, s
import numpy as np
from tqdm import tqdm
from sklearn.metrics import r2_score
import pandas as pd
data = pd.read_csv(r"D:\Users\ritvik\projects\GEOGLAM\Output\ml\analysis\November_03_2024\ukraine\maize\gam\2005\ukraine_maize_2005.csv")

# Drop rows where 'Yield (tn per ha)' is missing
data = data.dropna(subset=['Yield (tn per ha)'])

# Drop columns with missing values
data = data.dropna(axis=1)

# Extract features and target
X = data.drop(columns=['Production (tn)', 'Country', 'Region', 'Crop', 'Yield (tn per ha)', 'Harvest Year'])
y = data['Yield (tn per ha)']
years = data['Harvest Year']

# Step 1: Feature Selection using Boruta
rf = RandomForestRegressor(n_jobs=-1, max_depth=5)
boruta_selector = BorutaPy(rf, n_estimators='auto', random_state=1, verbose=True)
boruta_selector.fit(X.values, y.values)

# Select features marked as important by Boruta
selected_features = X.columns[boruta_selector.support_].tolist()
X_selected = X[selected_features]

# Step 2: Perform Year-based Temporal Validation
year_splits = sorted(data['Harvest Year'].unique())  # Unique years sorted for ordered splitting
results = []
gam_predictions = []

for i in range(len(year_splits) - 1):
    # Define the training and testing periods
    train_years = year_splits[:i + 1]
    test_year = year_splits[i + 1]
    print(test_year)
    # Split data based on years
    X_train = X_selected[years.isin(train_years)]
    y_train = y[years.isin(train_years)]
    X_test = X_selected[years == test_year]
    y_test = y[years == test_year]

    # Step 3: Fit the spline regression model (GAM) on all selected features
    gam = LinearGAM(terms='auto').fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = gam.predict(X_test)
    gam_predictions.append((test_year, y_pred))

    # Evaluate model performance for each split
    rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    # also compute r2 and mape
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    results.append({'Year': test_year, 'RMSE': rmse, 'R2': r2, 'MAPE': mape})

# create dataframe
results = pd.DataFrame(results)

# Display RMSE results by test year for each temporal validation fold
print(results)

breakpoint()
