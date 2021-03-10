# -*- coding: utf-8 -*-
"""NaiveBayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fd86AyiC6CfNQSY75kTUVUcx8i9HVSGs
"""

#import os
#os.chdir('/content/drive/My Drive/Code/Ass3/Data')

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.stats import multivariate_normal
from sklearn.metrics import classification_report
import copy 
import math
import csv
import time
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

# Default value
SSE = 0 
phi = -1
pi = 3.141593
dim = 1

def findSample(index):
  lst = df.loc[index]
  lst = lst.to_numpy().tolist()
  lst = lst[:len(lst)-1]
  return lst

def split_data(x,y):
    X_train, X_test, y_train, y_test = train_test_split(
        x, y,stratify = y, test_size=0.2)
    print(len(X_train))
    return  X_train, X_test, y_train, y_test

def findSum(Di):
  lst = [0]*dim
  for ele in Di:
    lst = np.add(lst,ele)
  return lst

def calgaussDist(x,u,covMat):
  x_minus_u = (x-u)* (x-u)
  dist = 1/((pow(2*pi,1/2))*(pow(covMat,1/2)))
  dist = dist * math.exp(-(x_minus_u/(2*covMat)))
  return dist

def testModel(P_Ci_s,Means,CovMat,X_test,y_test):
  Y_out = []
  for i in range(len(X_test)):
    max = 0
    mx_index = 0
    for j in range(len(P_Ci_s)):
      val = 1 #multivariate_normal.pdf(X_test[i], Means[j],CovMat[j])
      for d in range(dim):
        val *= calgaussDist(X_test[i][d], Means[j][d],CovMat[j][d][d]) #multivariate_normal.pdf(X_test[i], Means[j][d],CovMat[j][d][d]) #
      
      temp = val* P_Ci_s[j]
      if temp > max:
        max = temp
        mx_index = j
    Y_out.append(mx_index)
  return Y_out

def NaiveBayesFilter(x,y,k):
  Di_s = {}
  P_Ci_s = []
  Means = []
  CovMat = []
  n = len(x)
  labels = set()
  for sampleIndex in range(n):
    Di_s.setdefault(y[sampleIndex], []).append(x[sampleIndex])
    labels.add(y[sampleIndex])
  for label in labels:
    ni = len(Di_s[label])
    P_Ci_s.append(ni/n)
    ui = findSum(Di_s[label])/ni
    Means.append(ui)
    Zi = np.subtract(Di_s[label],ui)
    mat = ((np.transpose(Zi)).dot(Zi))*(1/ni)
    mat = np.diag(np.diag(mat))
    CovMat.append(mat)
  
  return P_Ci_s,Means,CovMat

def fetchData(filename):
  df = pd.read_csv(filename)
  cols = np.array(df.columns)
  features = cols[:len(df.columns)-1]
  category = cols[len(df.columns)-1:]
  x = df.loc[:,features].values
  y = df.loc[:,category].values
  Y = []
  for i in range(len(y)):
    Y.append(y[i][0])
  return x , Y, df

x, y, df = fetchData('Data/creditcard.csv')
dim = len(df.columns) - 1

X_train, X_test, y_train, y_test = split_data(x,y)

P_Ci_s,Means,CovMat = NaiveBayesFilter(X_train,y_train,k=2)

Y_out = testModel(P_Ci_s,Means,CovMat,X_test,y_test)

print(classification_report(y_test, Y_out))

print(accuracy_score(Y_out,y_test))
