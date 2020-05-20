# Converting and quering weather data in parquet format

### Prerequisites:
* Python 3.6
* pipenv
* sqlite3 (to query parquet by SQL)
    * [libparquet.so library](https://github.com/cldellow/sqlite-parquet-vtable) (to read parquet in sqlite3)

### Files:
File | Description
--- | ---
Pipfile | Specifies python libraries
Pipfile.lock | pipenv environment locked
convert2parquet.py | reads weather data from CSV file, concats, prints data quality checks, applies some fixes, converts to parquet format and saves to 'weather.2016.parquet'
**weather.2016.parquet** | parquet file with weather data; **size: 1.1 MB**; output of 'convert2parquet.py'
query_parquet.py | to query parquet file in pandas
query_parquet.sqlite | commands to SQL-query parquet file in SQLite3 

### Usage:
#### Concatenation, data checks, convertation to parquet
```
pipenv install
pipenv sync
pipenv shell
python convert2parquet.py
```

```
Output of convert2parquet.py
============================
# Column "ObservationDate" converted to datetime type

# Checks for null values through all the columns
Column "ForecastSiteCode", int64 type: 0(0.0%) null values
Column "ObservationTime", int64 type: 0(0.0%) null values
Column "ObservationDate", datetime64[ns] type: 0(0.0%) null values
Column "WindDirection", int64 type: 0(0.0%) null values
Column "WindSpeed", int64 type: 0(0.0%) null values
Column "WindGust", float64 type: 151411(77.8%) null values
Column "Visibility", float64 type: 26493(13.6%) null values
Column "ScreenTemperature", float64 type: 0(0.0%) null values
Column "Pressure", float64 type: 14820(7.6%) null values
Column "SignificantWeatherCode", int64 type: 0(0.0%) null values
Column "SiteName", object type: 0(0.0%) null values
Column "Latitude", float64 type: 0(0.0%) null values
Column "Longitude", float64 type: 0(0.0%) null values
Column "Region", object type: 0(0.0%) null values
Column "Country", object type: 27760(14.3%) null values

# Checks for most frequent values through all the columns
Most frequent in column "ForecastSiteCode": 3266(0.7%), 3749(0.7%), 3853(0.7%)
Most frequent in column "ObservationTime": 22(4.3%), 18(4.2%), 21(4.2%)
Most frequent in column "ObservationDate": 2016-03-16T00:00:00.000000000(1.8%), 2016-02-25T00:00:00.000000000(1.7%), 2016-03-12T00:00:00.000000000(1.7%)
Most frequent in column "WindDirection": 12(12.2%), 11(10.2%), 10(8.5%)
Most frequent in column "WindSpeed": 8(7.2%), 6(6.9%), 7(6.5%)
Most frequent in column "WindGust": 29.0(9.6%), 31.0(8.3%), 30.0(7.8%)
Most frequent in column "Visibility": 30000.0(8.8%), 50000.0(8.1%), 35000.0(6.5%)
Most frequent in column "ScreenTemperature": -99.0(1.6%), 5.7(1.3%), 5.3(1.3%)
Most frequent in column "Pressure": 1016.0(3.5%), 1017.0(2.8%), 1015.0(2.8%)
Most frequent in column "SignificantWeatherCode": 8(26.6%), 7(21.2%), -99(12.5%)
Most frequent in column "SiteName": LINTON ON OUSE (3266)(0.7%), MIDDLE WALLOP (3749)(0.7%), YEOVILTON (3853)(0.7%)
Most frequent in column "Latitude": 57.206(1.5%), 55.05(1.5%), 51.15(1.4%)
Most frequent in column "Longitude": -1.25(1.5%), -2.64(0.7%), -1.57(0.7%)
Most frequent in column "Region": London & South East England(12.4%), South West England(12.2%), Wales(10.1%)
Most frequent in column "Country": ENGLAND(60.2%), SCOTLAND(24.5%), WALES(11.0%)

# Investigating on null values in 'Country' column: values of 'Region' when 'Country'=null
Region
East Midlands                  1436
Grampian                       2827
Highland & Eilean Siar         4170
London & South East England    2775
North East England             2828
North West England             4093
Northern Ireland               5705
Orkney & Shetland              1424
Wales                          1267
Yorkshire & Humber             1235
dtype: int64

# fixing null values in 'Country' for Region='London & South East England' and Region='Northern Ireland'

# lastly, dataframe converted to parquet and saved as 'weather.2016.parquet'
```
Among the other issues found in the data is the value -99.0 in "ScreenTemperature" (most frequent value in this column). As "ScreenTemperature" columns contains degrees in Celsius, it seems '-99.0' represents the cases when a temperature value is not available for an observation (i.e., null value).

#### Querying parquet by pandas
```
pipenv install
pipenv sync
pipenv shell
python query_parquet.py
```
Outputs the answer to the question:\
    *ObservationDate:* 2016-03-17 00:00:00\
    *ScreenTemperature:* **15.8**\
    *Region:* Highland & Eilean Siar
    
#### Querying parquet by SQL (via SQLite3)
Commands are as follows (also see 'query_parquet.sqlite'):\
```
$ sqlite3
sqlite> -- load library to read parquet files
sqlite> .load ./libparquet
sqlite> CREATE VIRTUAL TABLE weather USING parquet('weather.2016.parquet');
sqlite> select ScreenTemperature,DATETIME(ROUND(ObservationDate / 1000), 'unixepoch'),Region from weath where ScreenTemperature = (select max(ScreenTemperature) from weather);
```
Output: **15.8** | 2016-03-17 00:00:00 | Highland & Eilean Siar
