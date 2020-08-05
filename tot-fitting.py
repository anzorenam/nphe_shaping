#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
mat.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import argparse
import os

def timeovert(x,vth,M):
  t0=np.zeros(M)
  tf=np.zeros(M)
  for j in range(0,M):
    try:
      t0[j]=np.nonzero(x[j,:]>vth)[0][0]
      tf[j]=np.nonzero(x[j,:]>vth)[0][-1]
    except IndexError:
      t0[j]=0
      tf[j]=0
  tover=(0.1)*(tf-t0)
  return tover

parser=argparse.ArgumentParser()
parser.add_argument('amp', help='select amp',type=int)
parser.add_argument('degree', help='filter order',type=int)
parser.add_argument('crange', help='capacitance range',type=int)
args=parser.parse_args()
amp=args.amp
degree=args.degree
crange=args.crange

home=os.environ['HOME']
dir='nphe_shaping'
nin='pe_stats/pe_stats-a{0}_d{1}c{2}'.format(amp,degree,crange)
name='{0}/{1}/{2}.dat'.format(home,dir,nin)

dt=0.2
tend=1000.0
t=np.arange(0,tend,dt)
tpeaks=[75,100,125,150,175]
a0_5d=np.array([-1.4766878,-1.4166647+0.5978596j,-1.2036832+1.2994843j])
a0_3d=np.array([-1.2633573,-1.1490948+0.7864188j])
sigma0=np.exp(1)/np.sqrt(2.0*np.pi)
data=np.loadtxt(name,comments='#')
vths=np.array([10,20,30,50])
K=np.size(vths)
pebins=np.arange(0,200)

for scale in [0.5,1.0,1.25]:
  Tstep=scale
  Tmax=255*Tstep
  t0bins=np.arange(0,Tmax,Tstep)
  dout='{0}/{1}/fitting/amp_stats{2}/tstep-{3}'.format(home,dir,amp,scale)
  for Cpar in [0,1,2]:
    for Rpar in [0,1,2]:
      fig,ax=plt.subplots(nrows=2,ncols=5)
      fig.set_size_inches(12,7)
      for Tpar in [0,1,2,3,4]:
        pe=data[:,0]
        v0=data[:,9*Tpar+3*Cpar+Rpar+1]
        tesT=v0!=0
        pe=pe[tesT]
        v0=v0[tesT]
        M=np.size(v0,0)
        tot=np.zeros([K,M])
        totQ=np.zeros([K,M])
        fwtm=2.0*tpeaks[Tpar]
        if degree==3:
          tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(2.9)))
          sigma=tau0*sigma0
          a=(1.0/sigma)*a0_3d
          k0=np.real((a[1]*np.conj(a[1])))
          semi_g0=signal.lti([],[a[1],np.conj(a[1])],k0)
        else:
          tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(15.55)))
          sigma=tau0*sigma0
          a=(1.0/sigma)*a0_5d
          k0=-1.0*np.real((a[1]*np.conj(a[1]))*(a[2]*np.conj(a[2])))
          semi_g0=signal.lti([],[a[1],np.conj(a[1]),a[2],np.conj(a[2])],k0)
        t,g0=signal.impulse(semi_g0,T=t)
        g0norm=(1.0/np.amax(g0))*g0
        pulse=np.transpose(v0[np.newaxis])*g0norm
        m=0
        ax[1,Tpar].hist(pe,bins=pebins,log=True)
        for vth in vths:
          tot[m,:]=timeovert(pulse,vth,M)
          totQ[m,:]=Tstep*np.digitize(tot[m,:],t0bins)
          tbins,tsat=np.unique(totQ[m,:],return_counts=True)
          ax[0,Tpar].scatter(pe,totQ[m,:],s=1.0)
          ax[0,Tpar].axis([0.9,200,0,Tmax])
          ax[0,Tpar].set_xscale('log')
          ax[1,Tpar].hist(totQ[m,:],bins=t0bins,log=True,alpha=0.5)
          m+=1
      plt.savefig('{0}/tot_d{1}c{2}-{3}{4}par.png'.format(dout,degree,crange,Cpar,Rpar),dpi=100)
