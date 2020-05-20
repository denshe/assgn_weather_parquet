import pandas as pd

d = pd.read_parquet('weather.2016.parquet')
print(d.loc[d.ScreenTemperature.idxmax()][['ObservationDate','ScreenTemperature','Region']])

