import sys
import pandas as pd
from time import strptime

if __name__ == "__main__":

    file_name = sys.argv[1]
    raw_df = pd.read_csv(file_name)

final = []
for eircode_output, _df in raw_df.groupby('Eircode Output'):
    routing_key, city = tuple(eircode_output.split(': ')) if ": " in eircode_output else ('IE', 'All')
    preprocessed = _df[['Eircode Output', 'Month', 'VALUE', 'Dwelling Status', 'Type of Buyer']]
    preprocessed.loc[:, ['Year', 'Month']] = preprocessed.Month.str.split(' ', expand=True).rename(columns={0:'Year', 1:'Month'})
    preprocessed.loc[:, ['Routing Key', 'City']] = preprocessed['Eircode Output'].str.split(': ', expand=True).rename(columns={0:'Routing Key', 1:'City'})
    preprocessed.loc[:, 'Month'] = preprocessed.Month.apply(lambda x: strptime(x, '%B').tm_mon)
    _final = preprocessed[['Routing Key', 'City', 'Month', 'Year', 'Dwelling Status', 'Type of Buyer', 'VALUE']].astype({'VALUE': 'float', 'Year': 'int'})
    final.append(_final)

final = pd.concat(final)
final.to_csv("./data/housing_prices/preprocessed/mean-housing-prices.csv", index=False)