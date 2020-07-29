#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

data=np.loadtxt('pe_stats.dat')
x=data[:,0]
y=data[:,1:]
pebins=np.arange(0,200)
fig,ax=plt.subplots(nrows=1,ncols=1)
for k in range(0,26):
  ax.scatter(x,y[:,k])
  msphe,sphe0,r,p,std=stats.linregress(x,y[:,k])
  sphe=y[x==1.0,k]
  print(np.mean(sphe)-2.0*np.std(sphe),np.mean(sphe)+2.0*np.std(sphe))
  print(1.0*msphe+sphe0,(200.0*msphe+sphe0)<2000)
plt.show()
