import sys
import pandas as pd
from time import strptime

if __name__ == "__main__":

    file_name = sys.argv[1]
    raw_df = pd.read_csv(file_name)

    for eircode_output, _df in raw_df.groupby('Eircode Output'):
        city = eircode_output.split(': ')[1] if ": " in eircode_output else 'All'
        preprocessed = _df[['Eircode Output', 'Month', 'VALUE', 'Dwelling Status', 'Type of Buyer']]
        preprocessed.loc[:, ['Year', 'Month']] = preprocessed.Month.str.split(' ', expand=True).rename(columns={0:'Year', 1:'Month'})
        preprocessed.loc[:, ['Eircode', 'City']] = preprocessed['Eircode Output'].str.split(': ', expand=True).rename(columns={0:'Eircode', 1:'City'})
        preprocessed.loc[:, 'Month'] = preprocessed.Month.apply(lambda x: strptime(x, '%B').tm_mon)
        final = preprocessed[['Eircode', 'Month', 'Year', 'Dwelling Status', 'Type of Buyer', 'VALUE']].astype({'VALUE': 'float', 'Year': 'int'})
        filename = '-'.join(city.split(" "))
        final.to_csv(f"./data/housing_prices/preprocessed/mean-housing-prices_{filename}.csv")