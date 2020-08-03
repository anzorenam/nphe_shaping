#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import numpy as np
import scipy.stats as stats
import numpy.random as rnd
import scipy.fftpack as fftp
import ROOT
import root_numpy as rnp
import time
import datetime
import argparse
import os

parser=argparse.ArgumentParser()
parser.add_argument('amp', help='select amp',type=int)
parser.add_argument('nfile', help='select file',type=int)
args=parser.parse_args()
amp=args.amp
nfile=args.nfile

t1=time.time()
home=os.environ['HOME']
dir='nphe_shaping'
name='{0}/{1}/scibar_photons-s{2}.csv'.format(home,dir,nfile)
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
mpar=np.size(cf)*np.size(rf)

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
Nhalf=int(Nz/2)
i_freq=fftp.fft(iphe,2*R-1,axis=1)
for c in cf:
  for r in rf:
    name='{0}/{1}/electronics-sim/trans-{2}_{3}{4}.dat'.format(home,dir,amp,c,r)
    zl_freq=np.loadtxt(name,usecols=(1,3),skiprows=2)
    zl_full=np.zeros((Nz,2))
    zl_full[0:Nhalf+1,0]=zl_freq[:,0]
    zl_full[0:Nhalf+1,1]=zl_freq[:,1]
    zl_full[Nhalf+1:Nz,0]=np.flip(zl_freq[1:Nhalf,0],0)
    zl_full[Nhalf+1:Nz,1]=-1.0*np.flip(zl_freq[1:Nhalf,1],0)
    zl_time=np.real(fftp.ifft(zl_full[:,0]+1j*zl_full[:,1]))[:R]
    z_conv=fftp.fft(zl_time,2*R-1)
    vint=np.real(fftp.ifft(i_freq*z_conv,axis=1))[:,:R]
    kpar+=1
    pe_stats[:,kpar]=np.amax(vint,axis=1)

nout='{0}/{1}/pe_stats-b{0}{1}.dat'.format(home,dir,amp,nfile)
np.savetxt(nout,pe_stats)
t2=time.time()
dtime=datetime.timedelta(seconds=(t2-t1))
print('Tiempo total {0:1.2f} seg.'.format(dtime.total_seconds()))
