import pandas as pd

# read csv files
d1 = pd.read_csv('weather.20160201.csv')
d2 = pd.read_csv('weather.20160301.csv')

# concat them in one dataframe
d = pd.concat([d1,d2],ignore_index=True)

# correct datatypes for columns
d.ObservationDate = pd.to_datetime(d.ObservationDate)

# ---------------------
# basic data 'check-up'
# ---------------------

num_records = len(d)

# null values
for el in d.columns:
    num = len( d[d[el].isnull()] )
    type = d[el].dtype
    print('Column "{}", {} type: {}({}%) null values'.format(el,type,num,round(100*num/num_records,1)))

# most frequent (top3) values in columns
NUM_LARGEST = 3
for el in d.columns:
    most_freq = d.groupby(el).size().nlargest(NUM_LARGEST)
    num_not_null = len(d[~d[el].isnull()])
    val_print = []
    for val,count in zip(most_freq.index.values,most_freq.values):
        val_print.append(val)
        val_print.append(round(100*count/num_not_null,1))
    print('Most frequent in column "{}": {}({}%), {}({}%), {}({}%)'.format(el,*val_print))

# investigate null values in 'Country'; can be omitted
# get region names for rows with Country=Null
print(d[d.Country.isnull()].groupby('Region').size())

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

# fix 'Country' for Region='London & South East England' and Region='Northern Ireland'
# Null values in 'Country' for the rest of regions can be fixed in a similar fashion
# comment lines below to not fix
d.loc[(d.Region=='London & South East England') & (d.Country.isnull()),'Country'] = 'ENGLAND'
d.loc[(d.Region=='Northern Ireland') & (d.Country.isnull()),'Country'] = 'NORTHERN IRELAND'

# save df in parquet format
d.to_parquet('weather.2016.parquet')

