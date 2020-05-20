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
weather.2016.parquet | parquet file with weather data; output of convert2parquet.py
query_parquet.py | to query parquet file in pandas
query_parquet.sqlite | commands to SQL-query parquet file in SQLite3 
