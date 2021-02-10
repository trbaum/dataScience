#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:07:01 2020

@author: teddyrosenbaum
"""

import matplotlib.pyplot as  plt
import pandas as pd
import numpy as np
df = pd.read_csv('life-expectancy-years-vs-real-gdp-per-capita-2011us.csv')
df['Real GDP per capita in 2011US$ ($)'] = df['Real GDP per capita in 2011US$ ($)'].fillna(0.0)
df['Life expectancy at birth'] = df['Life expectancy at birth'].fillna(0.0)
df['Code'] = df['Code'].fillna('Na')
l = len(df)

def nContains(dataList,item):
    for i in range(len(dataList)):
        if(dataList[i]  == item):
            return False
    return True

countries = []
for i in range(l):
    if(nContains(countries,df['Entity'][i])):
        countries.append(df['Entity'][i])

def firstIndex(entity):
    for i in range(l):
        if(df['Entity'][i] == entity):
            return i

def lastIndex(entity):
    e = 0;
    for i in range(l):
        if(df['Entity'][i] == entity):
            e = i
    return e

def countryData(entity):
    s = firstIndex(entity)
    e = lastIndex(entity) + 1
    return df[s:e].reset_index(drop=True)

def countryDataYear(entity):
    data = countryData(entity)
    return data.set_index('Year',drop=True)

def makeCountryDic():
    data = {}
    for i in range(len(countries)):
        data.update({countries[i] : countryData(countries[i])})
    return data

def hist2yearsGDP(first,second):
    firstYear = []
    for i in range(l):
        if(df['Year'][i] ==  first and df['Real GDP per capita in 2011US$ ($)'][i] != 0.0 and df['Code'][i] != 'Na'):
            firstYear.append(df['Real GDP per capita in 2011US$ ($)'][i])
    secondYear = []
    for i in range(l):
        if(df['Year'][i] ==  second and df['Real GDP per capita in 2011US$ ($)'][i] != 0.0 and df['Code'][i] != 'Na'):
            secondYear.append(df['Real GDP per capita in 2011US$ ($)'][i])
    plt.hist(firstYear,bins=50,alpha=0.5)
    plt.hist(secondYear,bins=50,alpha=0.5)

def hist2yearsLife(first,second):
    firstYear = []
    for i in range(l):
        if(df['Year'][i] == first and df['Life expectancy at birth'][i] != 0.0 and df['Code'][i] != 'Na'):
            firstYear.append(df['Life expectancy at birth'][i])
    secondYear = []
    for i in range(l):
        if(df['Year'][i] ==  second and df['Life expectancy at birth'][i] != 0.0 and df['Code'][i] != 'Na'):
            secondYear.append(df['Life expectancy at birth'][i])
    plt.hist(firstYear,bins=50,alpha=0.5)
    plt.hist(secondYear,bins=50,alpha=0.5)

def plotCountryDataLifeGDP(country = 'Afghanistan'):
    data = countryData(country)
    for i in range(len(data)):
        if(data['Real GDP per capita in 2011US$ ($)'][i] != 0.0 and data['Life expectancy at birth'][i] != 0.0):
            plt.scatter(data['Real GDP per capita in 2011US$ ($)'][i],data['Life expectancy at birth'][i])
    plt.xlabel('Real GDP per capita in 2011US$ ($)')
    plt.ylabel('Life expectancy at birth')
    return data['Real GDP per capita in 2011US$ ($)'][i],data['Life expectancy at birth'][i]

def plotCountryDataLifeDate(country = 'Afghanistan'):
    data = countryData(country)
    for i in range(len(data)):
        if(data['Life expectancy at birth'][i] != 0.0):
            plt.scatter(data['Year'][i],data['Life expectancy at birth'][i])
    plt.xlabel('Year')
    plt.ylabel('Life expectancy at birth')
    return data['Year'][i],data['Life expectancy at birth'][i]

def plotCountryDataGDPDate(country = 'Afghanistan'):
    data = countryData(country)
    for i in range(len(data)):
        if(data['Real GDP per capita in 2011US$ ($)'][i] != 0.0):
            plt.scatter(data['Year'][i],data['Real GDP per capita in 2011US$ ($)'][i])
    plt.xlabel('Year')
    plt.ylabel('Real GDP per capita in 2011US$ ($)')
    return data['Year'][i],data['Real GDP per capita in 2011US$ ($)'][i]

def exponentialFitYearGDP(country = 'Afghanistan'):
    data = countryData(country)
    ypoints = []
    xpoints = []
    
    for i in range(len(data)):
        if(data['Real GDP per capita in 2011US$ ($)'][i] != 0.0):
            ypoints.append(np.log(data['Real GDP per capita in 2011US$ ($)'][i]))
            xpoints.append(data['Year'][i])
        
    #weights = 1.0/np.log((2020.0-y)/1000.0) talk to dr swift abou weights

    fit = np.polyfit(xpoints,ypoints,1,full=False,cov=True)
    
    cov = fit[1]
    m = fit[0][0]
    merr = np.sqrt(cov[0][0])
    b = fit[0][1]
    berr  = np.sqrt(cov[1][1])
    x = np.array(range(2020-xpoints[0]))
    x = x+xpoints[0]
    y = np.exp(m*x + b)
    
    plt.plot(x,y)
    plt.plot(xpoints,np.exp(ypoints))
    
    return m,merr,b,berr
    


