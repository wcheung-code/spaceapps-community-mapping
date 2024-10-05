# Instructions:

1) Navigate to [https://data.cso.ie/](https://data.cso.ie/).

2) Search `Market-based Household Purchases of Residential Dwellings`

3) Choose the following filters:
![image](https://github.com/user-attachments/assets/731568c8-a612-44c2-a680-c9478a895955)

4) Add downloaded dataset to `data/housing_prices/raw` folder.

5) Run the following from `spaceapps-community-mapping` directory.
```
$ python3 data/housing_prices/scripts/generate_mean_housing_prices.py data/housing_prices/raw/HPM04.20241005T101051.csv
```

6) This will generate all of the mean housing prices in `data/housing_prices/preprocessed` folder.
