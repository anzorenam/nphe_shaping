#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

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

pmin=1
tpeaks=[100,110,120,130]
Tstep=1.0
Tmax=255*Tstep
dt=0.2
tend=1000.0
t=np.arange(0,tend,dt)
a0_5d=np.array([-1.4766878,-1.4166647+0.5978596j,-1.2036832+1.2994843j])
a0_3d=np.array([-1.2633573,-1.1490948+0.7864188j])
sigma0=np.exp(1)/np.sqrt(2.0*np.pi)
data=np.loadtxt('pe_stats-b1.dat',comments='#')
Cpar=0
vths=np.array([10.0,20,30,50])
K=np.size(vths)
t0bins=np.arange(0,Tmax,Tstep)
pebins=np.arange(0,150)
for Rpar in [0,1,2]:
  for d in [3,5]:
    fig,ax=plt.subplots(nrows=2,ncols=4)
    for j in range(0,4):
      pe=data[:,0]
      v0=data[:,j+9*Cpar+3*Rpar+1]
      tesT=v0!=0
      pe=pe[tesT]
      v0=v0[tesT]
      M=np.size(v0,0)
      tot=np.zeros([K,M])
      totQ=np.zeros([K,M])
      fwtm=2.0*tpeaks[j]
      if d==3:
        tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(2.9)))
        sigma=tau0*sigma0
        a=(1.0/sigma)*a0_3d
        k0=-1.0*np.real(a[0]*(a[1]*np.conj(a[1])))
        semi_g0=signal.lti([],[a[0],a[1],np.conj(a[1])],k0)
      else:
        tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(15.55)))
        sigma=tau0*sigma0
        a=(1.0/sigma)*a0_5d
        k0=-1.0*np.real(a[0]*(a[1]*np.conj(a[1]))*(a[2]*np.conj(a[2])))
        semi_g0=signal.lti([],[a[0],a[1],np.conj(a[1]),a[2],np.conj(a[2])],k0)
      t,g0=signal.impulse(semi_g0,T=t)
      g0norm=(1.0/np.amax(g0))*g0
      pulse=np.transpose(v0[np.newaxis])*g0norm
      m=0
      ax[1,j].hist(pe,bins=pebins,log=True)
      for vth in vths:
        tot[m,:]=timeovert(pulse,vth,M)
        totQ[m,:]=Tstep*np.digitize(tot[m,:],t0bins)
        tbins,tsat=np.unique(totQ[m,:],return_counts=True)
        phe_th=pmin+tsat[0]-1
        ax[0,j].scatter(pe,totQ[m,:],s=1.0)
        ax[0,j].axis([0.1,140,0,Tmax])
        ax[0,j].set_xscale('log')
        ax[1,j].hist(totQ[m,:],bins=t0bins,log=True,alpha=0.5)
        #print(np.size(tbins),np.amin(tot[m,:]),np.amax(tot[m,:]),tsat,phe_th,vth)
        m+=1
      #plt.savefig('tot_{0}d{1}{2}par.png'.format(d,Cpar,Rpar))
  plt.show()
