# -*- coding: utf-8 -*-
"""medal_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yZhKwY1JuttGOeat7ZemOZSelgmeaFHD
"""

import pandas as pd;
teams = pd.read_csv("/content/teams.csv")
print(teams)

teams = teams[["team", "country","year","athletes","age","prev_medals","medals"]]
print(teams)

# teams.corr()["medals"]
import seaborn as sns
sns.lmplot(x="athletes",y="medals",data=teams,fit_reg=True,ci=None)

sns.lmplot(x="age",y="medals",data=teams,fit_reg=True,ci=None)

teams.plot.hist(y="medals")

#data cleaning
teams[teams.isnull().any(axis=1)]

teams = teams.dropna()
print(teams)

train  = teams[teams["year"]<2012].copy()
test = teams[teams["year"]>=2012].copy()

train.shape

test.shape

#Training Model
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
predictors = ["athletes","prev_medals"]
target = "medals"
reg.fit(train[predictors],train["medals"])
LinearRegression()
predictions = reg.predict(test[predictors])
print(predictions)

test["predictions"] = predictions
test.loc[test["predictions"]<0,"predictions"] = 0
test["predictions"] = test["predictions"].round()
print(test)

#mean absolute error
from sklearn.metrics import mean_absolute_error
error = mean_absolute_error(test["medals"],test["predictions"])
print(error)

teams.describe()["medals"]

test[test["team"]== "USA"]

test[test["team"]== "IND"]

errors  = (test["medals"] - test["predictions"]).abs()
print(errors)

error_by_team = errors.groupby(test["team"]).mean()
print(error_by_team)

medals_by_team = test["medals"].groupby(test["team"]).mean()
print(medals_by_team)

error_ratio  = error_by_team/medals_by_team
print(error_ratio)

error_ratio[~pd.isnull(error_ratio)]

import numpy as np
error_ratio  = error_ratio[np.isfinite(error_ratio)]
print(error_ratio)

error_ratio.plot.hist()

error_ratio.sort_values()