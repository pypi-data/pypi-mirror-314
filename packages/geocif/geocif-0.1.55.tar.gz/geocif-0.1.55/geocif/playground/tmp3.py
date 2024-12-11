import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Part 1: Read and Process Crop Yield Data
# Replace 'crop_yield_data.csv' with your actual crop yield data file
# Ensure your data has at least 'Year' and 'Yield' columns

# For demonstration purposes, let's create a sample dataset
crop_data = {
    'Year': list(range(1980, 2021)),
    'Yield': [91.0, 105.0, 113.0, 81.0, 106.0, 118.0, 119.0, 119.0, 84.6, 116.0,
              118.5, 108.6, 131.4, 100.7, 138.6, 113.5, 127.1, 126.7, 134.4, 133.8,
              136.9, 138.2, 129.3, 142.2, 160.3, 147.9, 149.1, 150.7, 153.9, 164.7,
              152.8, 147.2, 123.1, 158.1, 171.0, 168.4, 174.6, 176.6, 176.4, 167.8, 172.0]
}

crop_yield = pd.DataFrame(crop_data)

# Compute yield anomaly
crop_yield['Yield_Anomaly'] = crop_yield['Yield'] - crop_yield['Yield'].mean()

# Part 2: Read and Process Climate Indices Data

# Read ENSO (Nino 3.4 Index) data

enso_url = 'https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices'
enso_data = pd.read_csv(enso_url, delim_whitespace=True)
enso_data['Year'] = enso_data['YR']
enso_data = enso_data.groupby('Year')['ANOM'].mean().reset_index()
enso_data.rename(columns={'ANOM': 'ENSO'}, inplace=True)

# Read PDO data
pdo_url = 'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.pdo.dat'
pdo_data = pd.read_csv(pdo_url, skiprows=1)
pdo_data['Date'] = pd.to_datetime(pdo_data['Date'])
pdo_data['Year'] = pdo_data['Date'].dt.year
pdo_data = pdo_data.groupby('Year')['Value'].mean().reset_index()
pdo_data.rename(columns={'Value': 'PDO'}, inplace=True)

# Read NAO data
nao_url = 'https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii.table'
nao_data = pd.read_csv(nao_url, delim_whitespace=True)
nao_data = nao_data.melt(id_vars='YEAR', var_name='Month', value_name='NAO')
nao_data['Year'] = nao_data['YEAR']
nao_data = nao_data.groupby('Year')['NAO'].mean().reset_index()

# Read AO data
# ao_url = 'https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/AO_index_Monthly.txt'
# ao_data = pd.read_csv(ao_url, skiprows=1, delim_whitespace=True, names=['YEAR','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'])
# ao_data['Year'] = ao_data['YEAR']
# ao_data['AO'] = ao_data[['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']].mean(axis=1)
# ao_data = ao_data[['Year', 'AO']]

# Part 3: Merge All Data

# Merge crop yield data with climate indices
merged_data = crop_yield.copy()

# Merge with ENSO data
merged_data = pd.merge(merged_data, enso_data, on='Year', how='left')

# Merge with PDO data
merged_data = pd.merge(merged_data, pdo_data, on='Year', how='left')

# Merge with NAO data
merged_data = pd.merge(merged_data, nao_data[['Year', 'NAO']], on='Year', how='left')

# # Merge with AO data
# merged_data = pd.merge(merged_data, ao_data, on='Year', how='left')

# Handle missing data (if any)
merged_data.dropna(inplace=True)

# Part 4: Multivariate Regression Analysis

# Define predictor variables and response variable
X = merged_data[['ENSO', 'PDO', 'NAO', 'AO']]
y = merged_data['Yield_Anomaly']

# Fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Print regression coefficients
coefficients = pd.DataFrame({'Variable': X.columns, 'Coefficient': model.coef_})
print('Regression Coefficients:')
print(coefficients)
print(f'Intercept: {model.intercept_:.2f}')

# Predict yield anomalies
merged_data['Predicted_Yield_Anomaly'] = model.predict(X)

# Calculate R-squared
r2 = r2_score(y, merged_data['Predicted_Yield_Anomaly'])
print(f'R-squared: {r2:.2f}')

# Part 5: Visualization

# Plot Actual vs Predicted Yield Anomalies
plt.figure(figsize=(10,6))
plt.plot(merged_data['Year'], merged_data['Yield_Anomaly'], label='Actual Yield Anomaly', marker='o')
plt.plot(merged_data['Year'], merged_data['Predicted_Yield_Anomaly'], label='Predicted Yield Anomaly', marker='x')
plt.xlabel('Year')
plt.ylabel('Yield Anomaly (bushels per acre)')
plt.title('Actual vs Predicted Crop Yield Anomalies')
plt.legend()
plt.grid(True)
plt.show()

# Plot Residuals
merged_data['Residuals'] = merged_data['Yield_Anomaly'] - merged_data['Predicted_Yield_Anomaly']
plt.figure(figsize=(10,6))
plt.bar(merged_data['Year'], merged_data['Residuals'])
plt.xlabel('Year')
plt.ylabel('Residuals (bushels per acre)')
plt.title('Residuals of the Yield Prediction Model')
plt.grid(True)
plt.show()
