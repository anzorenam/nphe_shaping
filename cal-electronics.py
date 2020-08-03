#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns

sns.set(rc={"figure.figsize":(8,4)})
sns.set_context('paper',font_scale=1.5,rc={'lines.linewidth':1.5})
sns.set_style('ticks')
mat.rc('text',usetex=True)
mat.rcParams['text.latex.preamble']=[r'\usepackage[utf8]{inputenc}',r'\usepackage[T1]{fontenc}',r'\usepackage[spanish]{babel}',r'\usepackage[scaled]{helvet}',r'\renewcommand\familydefault{\sfdefault}',r'\usepackage{amsmath,amsfonts,amssymb}',r'\usepackage{siunitx}']

print=False
c0=sns.diverging_palette(255,133,l=60,n=15,center="dark")
sns.set_palette(c0)
fig,ax=plt.subplots(nrows=1,ncols=2,sharex=False,sharey=True)
for j in range(0,2):
  data=np.loadtxt('pe_stats-b{0}.dat'.format(j),comments='#')
  x=data[:,0]
  y=data[:,1:]
  pebins=np.arange(0,200)
  for k in range(0,27):
    z=(1.0/1000.0)*y[:,k]
    test=z!=0
    ax[j].scatter(x[test],z[test],s=1.0,rasterized=True)
    msphe,sphe0,r,p,std=stats.linregress(x,y[:,k])
    sphe=y[x==1.0,k]
    if print==True:
      print('b{0}'.format(j))
      print(np.mean(sphe)-2.0*np.std(sphe),np.mean(sphe)+2.0*np.std(sphe))
      print(1.0*msphe+sphe0,(200.0*msphe+sphe0)<3500)
  ax[j].axhline(y=4.7,ls=':',color='black')
  ax[j].axhline(y=2.4,ls=':',color='black')
  ax[j].set_xlabel(r'Photoelectrons',x=0.9,horizontalalignment='right')
  ax[j].set_ylabel(r'Amplitude $[\si{\volt}]$')
ax[0].axis([0,140,0,7])
ax[1].axis([0,140,0,7])
plt.tight_layout(pad=1.0)
plt.savefig('phe-cal.pdf')
plt.show()
