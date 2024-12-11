import os

# Set R_HOME environment variable before importing rpy2
os.environ["R_HOME"] = f"{os.environ['CONDA_PREFIX']}\Lib\R"

import rpy2.robjects.packages as rpackages

# Install 'ggplot2' if it's not already installed
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)  # Choose the first CRAN mirror


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pygam import LinearGAM, s
import statsmodels.api as sm
from patsy import dmatrix
from rpy2.robjects import pandas2ri, r
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


# Activate the automatic conversion between pandas DataFrame and R data.frame
pandas2ri.activate()

# Create synthetic data to simulate an agricultural context
np.random.seed(42)
n = 100
temperature = np.linspace(10, 30, n)  # Temperature range from 10°C to 30°C
yield_anomaly = 5 * np.sin(temperature / 2) + np.random.normal(0, 1, size=n)  # Simulated yield anomaly
data = pd.DataFrame({'Temperature': temperature, 'Yield_Anomaly': yield_anomaly})

# Prepare a grid for prediction
temperature_grid = np.linspace(10, 30, 200)

# 1. Cubic Spline using statsmodels
# Create a cubic spline basis with patsy
cubic_spline_basis = dmatrix("bs(Temperature, degree=3, df=6, include_intercept=True) - 1",
                             data, return_type='dataframe')

# Fit the model using OLS
model_cubic_statsmodels = sm.OLS(data['Yield_Anomaly'], cubic_spline_basis).fit()

# Predict on the temperature grid
cubic_spline_grid_basis = dmatrix("bs(temperature_grid, degree=3, df=6, include_intercept=True) - 1",
                                  {"temperature_grid": temperature_grid}, return_type='dataframe')
cubic_statsmodels_preds = model_cubic_statsmodels.predict(cubic_spline_grid_basis)

# 2. Cubic Spline using pygam
# Fit a Generalized Additive Model (GAM) with a cubic spline
gam = LinearGAM(s(0, n_splines=10, spline_order=3)).fit(data['Temperature'], data['Yield_Anomaly'])

# Predict on the temperature grid
gam_preds = gam.predict(temperature_grid)

# 3. R Integration with rpy2 for mgcv
# Import necessary R packages
importr('mgcv')

# Convert Python DataFrame to R DataFrame
r_data = pandas2ri.py2rpy(data)

# R script to fit a cubic spline using mgcv and predict on the grid
r_code = '''
library(mgcv)
temperature_grid <- seq(10, 30, length.out = 200)
gam_model <- gam(Yield_Anomaly ~ s(Temperature, bs = "cs"), data = data)
predictions <- predict(gam_model, newdata = data.frame(Temperature = temperature_grid))
list(temperature_grid = temperature_grid, predictions = predictions)
'''

# Execute the R code
robjects.globalenv['data'] = r_data
r_result = robjects.r(r_code)
r_temperature_grid = np.array(r_result[0])
r_predictions = np.array(r_result[1])

# Plotting all three models together
plt.figure(figsize=(10, 6))

# Plot original data
plt.scatter(data['Temperature'], data['Yield_Anomaly'], color='gray', alpha=0.5, label='Data')

# Plot statsmodels prediction
plt.plot(temperature_grid, cubic_statsmodels_preds, label='Cubic Spline (statsmodels)', color='blue')

# Plot pygam prediction
plt.plot(temperature_grid, gam_preds, label='Cubic Spline (pygam)', color='green')

# Plot mgcv prediction from R
plt.plot(r_temperature_grid, r_predictions, label='Cubic Spline (mgcv, R)', color='red')

# Customize the plot
plt.title('Cubic Splines for Yield Prediction (Temperature vs Yield Anomaly)')
plt.xlabel('Temperature (°C)')
plt.ylabel('Yield Anomaly')
plt.legend()
plt.show()
