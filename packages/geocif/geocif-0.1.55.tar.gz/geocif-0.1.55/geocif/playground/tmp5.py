import pandas as pd
import matplotlib.pyplot as plt

# DataFrame to store performance impacts
impact_df = pd.DataFrame(columns=['Test_Year', 'Region', 'Performance_Impact'])

# Baseline Scenario: Calculate baseline RMSE for each test year
baseline_performance = {}
for test_year in years:
    train_data = data[data['year'] != test_year]
    test_data = data[data['year'] == test_year]
    baseline_rmse = evaluate_model(train_data, test_data)
    baseline_performance[test_year] = baseline_rmse
    print(f"Baseline RMSE for test year {test_year}: {baseline_rmse}")

# Regional Inclusion Scenario: Calculate impact for each region in each test year
for test_year in years:
    test_data = data[data['year'] == test_year]
    train_data_base = data[data['year'] != test_year]
    performance_impact = {}

    for region in regions:
        # Add test year data for the specified region to the training set
        region_data = test_data[test_data['region'] == region]
        train_data_with_region = pd.concat([train_data_base, region_data], ignore_index=True)

        # Evaluate model performance with region data included
        rmse_with_region = evaluate_model(train_data_with_region, test_data[test_data['region'] != region])
        baseline_rmse = baseline_performance[test_year]
        impact = baseline_rmse - rmse_with_region  # Improvement when including this region

        # Store impact data in DataFrame
        impact_df = impact_df.append({
            'Test_Year': test_year,
            'Region': region,
            'Performance_Impact': impact
        }, ignore_index=True)

# Convert Performance_Impact to numeric for calculations
impact_df['Performance_Impact'] = pd.to_numeric(impact_df['Performance_Impact'])

# Plotting relative impact for each region
for test_year in years:
    yearly_impact = impact_df[impact_df['Test_Year'] == test_year]
    yearly_impact = yearly_impact.sort_values(by='Performance_Impact', ascending=False)

    # Bar plot for the test year, showing the relative impact of each region
    plt.figure(figsize=(10, 6))
    plt.bar(yearly_impact['Region'], yearly_impact['Performance_Impact'])
    plt.title(f'Relative Impact of Each Region on Model Performance (Test Year: {test_year})')
    plt.xlabel('Region')
    plt.ylabel('Performance Improvement (RMSE Reduction)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
