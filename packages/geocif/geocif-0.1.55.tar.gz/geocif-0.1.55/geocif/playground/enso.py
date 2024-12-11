import os
import pandas as pd
import numpy as np
import requests
from io import StringIO

class SSTIndexExtractor:
    def __init__(self, save_path='SST_index.csv',
                 working_dir=r'.'):
        self.save_path = save_path
        os.chdir(working_dir)
        self.combined_data = pd.DataFrame()

    def fetch_data_from_url(self, url):
        """Fetches data from a URL and returns it as a StringIO object."""
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        return StringIO(response.text)

    def process_time_series_data(self, url, variable, missing_value=-999.00):
        """Generalized method to process time series data in year-based format."""
        raw_data = self.fetch_data_from_url(url).getvalue().splitlines()
        data = []

        for line in raw_data[1:]:  # Skip the first line with start and end years
            fields = line.split()
            if len(fields) == 13:  # Ensure each line has a year + 12 monthly values
                year = int(fields[0])
                monthly_values = [
                    float(value) if float(value) != missing_value else np.nan for value in fields[1:]
                ]
                # Generate monthly dates for the given year
                for month, value in enumerate(monthly_values, start=1):
                    date = pd.Timestamp(year=year, month=month, day=1)
                    data.append((date, value))

        # Create DataFrame with dates as index
        df = pd.DataFrame(data, columns=['Date', variable]).set_index('Date')
        self.add_to_combined_data(df, variable)

    def add_to_combined_data(self, data, variable):
        """Adds a new SST index to the combined DataFrame."""
        if self.combined_data.empty:
            self.combined_data = data
        else:
            self.combined_data = self.combined_data.join(data, how='outer')

    def process_meiv2(self):
        """Processes and adds MEI.v2 index to combined data."""
        url = 'https://www.psl.noaa.gov/enso/mei/data/meiv2.data'
        self.process_time_series_data(url, 'MEI')

    def process_nina34(self):
        """Processes and adds Nino Anom 3.4 index to combined data."""
        url = 'https://psl.noaa.gov/data/correlation/nina34.anom.data'  # Updated URL
        self.process_time_series_data(url, 'NINA34')

    def process_iod(self):
        """Processes and adds IOD index to combined data."""
        url = 'https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data'
        self.process_time_series_data(url, 'IOD')

    def save_combined_data(self):
        """Saves the combined DataFrame to the Excel file."""
        self.combined_data.to_csv(self.save_path)

    def run_all(self):
        """Executes all processing functions and saves combined data."""
        self.process_meiv2()
        self.process_nina34()
        self.process_iod()
        self.save_combined_data()
        print(self.combined_data)

# Example usage:
extractor = SSTIndexExtractor()
extractor.run_all()
