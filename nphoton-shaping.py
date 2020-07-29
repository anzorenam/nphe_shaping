#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import numpy as np
import scipy.stats as stats
import scipy.signal as signal
import numpy.random as rnd
import scipy.fftpack as fftp
import ROOT
import root_numpy as rnp
import time
import datetime
import os

t1=time.time()
home=os.environ['HOME']
dir='nphe_shaping'
name='{0}/{1}/scibar_photons-s15.csv'.format(home,dir)
f=open(name,'r')

dt=0.2
Fs=1.0/dt
tend=1000.0
M=50000
Nz=50000
R=5000
ntime=np.arange(dt,100.0,dt)
N=np.size(ntime)
p=np.zeros([M,N])
n0,pnum,t0=np.array(f.readline().split()[0:3],dtype=np.float)
iphe=np.zeros([M,R])
nphe=np.zeros(M,dtype=np.uint16)
alpha=2.0
t=np.arange(0,tend,dt)
tconv=np.arange(0,2.0*tend-dt,dt)
Qpmt,sqpmt=0.938888,0.146729
mtau,stau=0.377159,0.0157205
tfun='TMath::Landau(x,{0},{1},1)'.format(mtau,stau)
taud=ROOT.TF1('tau0',tfun,0.1,2.0)
Vsat=2500.0
cf=['100p','200p','400p']
rf=['3k','6k','12k']

tpeaks=[75,100,150]
Gains=[1.0]
mpar=np.size(cf)*np.size(rf)*np.size(tpeaks)*np.size(Gains)

plot=True
j=0
jphoton=0
for line in f:
  p[j,jphoton]=t0
  nphe[j]=jphoton+1
  k=np.fromstring(line,dtype=np.float,count=4,sep=' ')
  nevent=k[0]
  t0=k[2]
  if n0!=nevent:
    n0=nevent
    ptimes=p[j,p[j,:]!=0]
    if np.all(ptimes<200.0):
      rnd_tau=rnp.random_sample(taud,jphoton+1)
      q=stats.norm.rvs(loc=Qpmt,scale=sqpmt,size=jphoton+1)
      k=q/(2.0*rnd_tau)
      tnorm=(t-np.transpose(ptimes[np.newaxis]))/np.transpose(rnd_tau[np.newaxis])
      u=t>np.transpose(ptimes[np.newaxis])
      izero=np.transpose(k[np.newaxis])*np.power(tnorm,alpha)*np.exp(-1.0*tnorm)*u
      iphe[j,:]=np.sum(izero,axis=0)
    j+=1
    jphoton=0
  else:
    jphoton+=1

test=np.logical_and(nphe!=0,np.sum(p!=0,axis=1)>=1.0)
nphe=nphe[test]
p=p[test]
iphe=iphe[test,:]
Mevent=np.size(iphe,0)
pe_stats=np.zeros([Mevent,mpar+1])
pe_stats[:,0]=nphe
print(Mevent)
print(np.amin(nphe),np.amax(nphe))

elem=199
pe=np.arange(0,elem)
pe_hist,bi=np.histogram(nphe,bins=np.arange(0,elem+1))
pe=bi[np.nonzero(pe_hist)]
Npe=np.size(pe)

kpar=0
sigma0=np.exp(1)/np.sqrt(2.0*np.pi)
Nhalf=int(Nz/2)
a0=np.array([-1.4766878,-1.4166647+0.5978596j,-1.2036832+1.2994843j])
for c in cf:
  for r in rf:
    i_freq=fftp.fft(iphe,2*R-1,axis=1)
    name='{0}/{1}/electronics-sim/trans_{2}{3}.dat'.format(home,dir,c,r)
    zl_freq=np.loadtxt(name,usecols=(1,3),skiprows=2)
    zl_full=np.zeros((Nz,2))
    zl_full[0:Nhalf+1,0]=zl_freq[:,0]
    zl_full[0:Nhalf+1,1]=zl_freq[:,1]
    zl_full[Nhalf+1:Nz,0]=np.flip(zl_freq[1:Nhalf,0],0)
    zl_full[Nhalf+1:Nz,1]=-1.0*np.flip(zl_freq[1:Nhalf,1],0)
    zl_time=np.real(fftp.ifft(zl_full[:,0]+1j*zl_full[:,1]))[:R]
    z_conv=fftp.fft(zl_time,2*R-1)
    vint=i_freq*z_conv
    for tp in tpeaks:
      fwtm=2.0*tp
      tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(15.55)))
      sigma=tau0*sigma0
      a=(1.0/sigma)*a0
      k0=np.real((a[1]*np.conj(a[1]))*(a[2]*np.conj(a[2])))
      semi_g0=signal.lti([],[a[1],np.conj(a[1]),a[2],np.conj(a[2])],k0)
      t,g0=signal.impulse(semi_g0,T=t)
      gfreq=fftp.fft(g0,2*R-1)
      vgauss=np.real(fftp.ifft(gfreq*vint,axis=1))[:,:R]
      for Gv in Gains:
        kpar+=1
        pe_stats[:,kpar]=np.amax(Gv*vgauss,axis=1)

nout='{0}/{1}/pe_stats.dat'.format(home,dir)
np.savetxt(nout,pe_stats)
t2=time.time()
dtime=datetime.timedelta(seconds=(t2-t1))
print('Tiempo total {0:1.2f} seg.'.format(dtime.total_seconds()))
