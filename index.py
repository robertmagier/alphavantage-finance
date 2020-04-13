#!/bin/python3
#%%

import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import numpy
from sklearn import linear_model
import pathlib


from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

import lib.prepareData as prep

DATA_DIR = pathlib.Path(__file__).parent.absolute()
dataFileName='data.json'


def _url(func, symbol, interval, apikey):

    query = "https://www.alphavantage.co/query?function={}&symbol={}&interval={}&apikey={}".format(
        func, symbol, interval, apikey
    )
    return query


def downloadStockData(symbol, interval):
    apiUrl = _url("TIME_SERIES_INTRADAY", symbol, interval, "demo")
    results = requests.get(apiUrl)
    input = json.dumps(results.json())
    f = open(os.path.join(DATA_DIR,dataFileName), "w+")
    f.write(input)
    f.close()
    return True


def readStockJsonData():
    f = open(os.path.join(DATA_DIR,dataFileName), "r+")
    output = f.read()
    f.close()
    output = json.loads(output)
    return output


# print(os.getcwd())


exists = os.path.exists(os.path.join(DATA_DIR,'data.json'))
if (exists):
    output = readStockJsonData()
else:
    print('File {} doesn\'t exist. Downloading...'.format(dataFileName))
    downloadStockData("IBM","5min")
    output = readStockJsonData()

df = pd.json_normalize(output)

open_columns = list(filter(lambda name: "open" in name, df.columns))
splitted = open_columns[0].split(' ')[3]
close_columns = list(filter(lambda name: "close" in name, df.columns))
high_columns = list(filter(lambda name: "high" in name, df.columns))
low_columns = list(filter(lambda name: "low" in name, df.columns))

# close_columns
# open_columns
values = pd.DataFrame()
y_open = df.iloc[0, df.columns.isin(open_columns)].to_frame()
y_close = df.iloc[0, df.columns.isin(close_columns)].to_frame()
y_high = df.iloc[0, df.columns.isin(high_columns)].to_frame()
y_low = df.iloc[0, df.columns.isin(low_columns)].to_frame()

values = values.assign(y_open=pd.Series(y_open.iloc[:, 0].map(float)).values)
values = values.assign(y_close=pd.Series(y_close.iloc[:, 0].map(float)).values)
values = values.assign(y_high=pd.Series(y_high.iloc[:, 0].map(float)).values)
values = values.assign(y_low=pd.Series(y_low.iloc[:, 0].map(float)).values)
values = values.assign(x=pd.Series(range(len(values.index))).values)
values = values.assign(time=pd.Series(open_columns).values)

start_value = values.loc[1, ["y_open"]][0]
values["y_diff"] = values["y_close"] - values["y_open"]
values["y_color"] = values["y_close"] - values["y_open"]
values["y_color"] = values["y_color"].map(lambda x: "green" if x > 0 else "red")

values["err_high"] = values.apply(prep.calculateHighError, axis=1)
values["err_low"] = values.apply(prep.calculateLowError, axis=1)
values["high_base"] = values.apply(prep.calculateHighBase, axis=1)
values["low_base"] = values.apply(prep.calculateLowBase, axis=1)
values["legend"] = values.apply(prep.generateLegend,axis=1)
# values['legend'] = pd.to_datetime(values['legend'])

# Calculate linear regression 
reg = linear_model.LinearRegression()
reg.fit(values.loc[:,['x']],values.loc[:,['y_open']])
predicted_linear = reg.predict(values.loc[:,['x']])
values['predicted_linear'] = predicted_linear

# Calculate polynomial regression
model = Pipeline([('poly', PolynomialFeatures(degree=7)),
                  ('linear', LinearRegression(fit_intercept=False))])
model = model.fit(values.loc[:,['x']].values,values.loc[:,['y_open']])

predicted_pol = model.predict(values.loc[:,['x']])
values['predicted_pol'] = predicted_pol

values.sort_values('x',ascending=False,inplace=True)


plt.figure(figsize=(20, 11.25))
plt.xticks(numpy.arange(0, 102, 11),labels=values['legend'][::11])
plt.yticks(numpy.arange(104,111,0.5))
plt.grid()

plt.bar(
    values["x"],
    values["y_diff"],
    bottom=values["y_open"],
    color=values["y_color"],
    width=0.7,
)
plt.plot(values['predicted_linear'],linewidth=2,color='darkblue')
plt.plot(values['predicted_pol'],linewidth=2,color='black')

plt.bar(
    values["x"],
    values["err_high"],
    bottom=values["high_base"],
    color="black",
    width=0.1,
)

plt.bar(
    values["x"],
    values["err_low"],
    bottom=values["low_base"],
    color="black",
    width=0.1,
)
plt.savefig('./plot.png',dpi=600)
plt.show()


# %%
