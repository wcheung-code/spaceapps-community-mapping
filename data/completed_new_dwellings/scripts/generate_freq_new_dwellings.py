import sys
import pandas as pd
from time import strptime

def mapping(quarter):
    if quarter == '1':
        return 3
    elif quarter == '2':
        return 6
    elif quarter == '3':
        return 9
    else:
        return 12

if __name__ == "__main__":

    file_name = sys.argv[1]
    raw_df = pd.read_csv(file_name)

    final = []
    for eircode_output, _df in raw_df.groupby('Eircode Output'):
        routing_key, city = tuple(eircode_output.split(': ')) if ": " in eircode_output else ('IE', 'All')
        preprocessed = _df[['Eircode Output', 'Quarter', 'VALUE']]
        preprocessed.loc[:, ['Year', 'Month']] = preprocessed['Quarter'].str.split('Q', expand=True).rename(columns={0:'Year', 1:'Month'})
        
        preprocessed.loc[:, ['Routing Key', 'City']] = preprocessed['Eircode Output'].str.split(': ', expand=True).rename(columns={0:'Routing Key', 1:'City'})
        preprocessed.loc[:, 'Month'] = preprocessed.Month.apply(mapping)
        _final = preprocessed[['Routing Key', 'City', 'Month', 'Year', 'VALUE']].astype({'VALUE': 'float', 'Year': 'int'})
        final.append(_final)

    final = pd.concat(final)
    final.to_csv("./data/completed_new_dwellings/preprocessed/freq-new-dwellings.csv", index=False)