#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.signal as signal

sns.set(rc={"figure.figsize":(8,4)})
sns.set_context('paper',font_scale=1.0,rc={'lines.linewidth':1.0})
sns.set_style('ticks')
mat.rc('text',usetex=True)
mat.rcParams['text.latex.preamble']=[r'\usepackage[utf8]{inputenc}',r'\usepackage[T1]{fontenc}',r'\usepackage[spanish]{babel}',r'\usepackage{amsmath,amsfonts,amssymb}',r'\usepackage{siunitx}']

plot=False
degree=3
if degree==3:
  tp=180.0
  fwtm=2.0*tp
  sigma0=np.exp(1)/np.sqrt(2.0*np.pi)
  tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(2.9)))
  sigma=tau0*sigma0
  a=(1.0/sigma)*np.array([-1.2633573,-1.1490948+0.7864188j])
  k0=-1.0*np.real(a[0]*(a[1]*np.conj(a[1])))
  C11=56
  H1=1.0
  trash,c1,s1=np.poly((a[1],np.conj(a[1])))
  w01=np.sqrt(s1)
  alpha1=c1/w01
  k1=(1.0e-3)*w01*C11
  m1=0.25*np.power(alpha1,2.0)+(H1-1.0)
  C21=m1*C11
  R11=2.0/(alpha1*k1)
  R21=alpha1/(2.0*m1*k1)
  f01=1e3*w01/(2.0*np.pi)
  e1=100.0*np.absolute(w01-1.0e3*np.sqrt(1.0/(1960.0*1870.0*C11*39.0)))/w01
  print('Etapa uno: C2= {0}pF,R1= {1}ohms,R2= {2}ohms'.format(C21,R11,R21))
  print('Porcentaje error etapa 1: {0}%'.format(e1))
  print('Ancho de banda mínimo por etapa: {0}MHz'.format(1.0*f01))
elif degree==5:
  C11=56.0
  C12=56.0
  H1=2.5
  H2=2.5
  trash,c1,s1=np.poly((a[1],np.conj(a[1])))
  trash,c2,s2=np.poly((a[2],np.conj(a[2])))
  w01=np.sqrt(s1)
  w02=np.sqrt(s2)
  alpha1=c1/w01
  alpha2=c2/w02
  k1=(1.0e-3)*w01*C11
  k2=(1.0e-3)*w02*C12
  m1=0.25*np.power(alpha1,2.0)+(H1-1.0)
  m2=0.25*np.power(alpha2,2.0)+(H2-1.0)
  C21=m1*C11
  C22=m2*C12
  R11=2.0/(alpha1*k1)
  R12=2.0/(alpha2*k2)
  R21=alpha1/(2.0*m1*k1)
  R22=alpha2/(2.0*m2*k2)
  f01=1e3*w01/(2.0*np.pi)
  f02=1e3*w02/(2.0*np.pi)
  e1=100.0*np.absolute(w01-1.0e3*np.sqrt(1.0/(665.0*243.0*C11*130.0)))/w01
  e2=100.0*np.absolute(w02-1.0e3*np.sqrt(1.0/(787.0*182.0*C12*110.0)))/w02
  #print 'Etapa uno: C2= {0}pF,R1= {1}ohms,R2= {2}ohms'.format(C21,R11,R21)
  #print 'Porcentaje error etapa 1: {0}%'.format(e1)
  #print 'Etapa dos: C2={0}pF,R1={1}ohms,R2={2}ohms'.format(C22,R12,R22)
  #print 'Porcentaje error etapa 2: {0}%'.format(e2)
  #print 'Ancho de banda mínimo por etapa: {0}MHz {1}MHz'.format(3.52*f01,3.52*f02)

Cf=33.0
Rf=18.0
tint=Cf*Rf
Cdiff=Cf
td=1.0/(-1.0*np.real(a[0])-1.0/tint)
Rdiff=1.0e3*(td/Cdiff)
e0=100.0*(td)*np.absolute(1.0/td-1.0/(3.48*Cf))
print('Diferenciador: Rdiff= {0}ohms'.format(Rdiff))
print('Porcentaje error diff: {0}%'.format(e0))

if plot==True:
  Tstep=0.1
  t=np.arange(0,1500.0,Tstep)
  semi_g0=signal.lti([],[a[0],a[1],np.conj(a[1]),a[2],np.conj(a[2])],k0)
  t,g0=signal.impulse(semi_g0,T=t)
  w,mag,p=semi_g0.bode()
  c=sns.color_palette(sns.cubehelix_palette(8,start=.25,rot=-.75,reverse=True))
  fig,ax=plt.subplots(nrows=1,ncols=1)
  ax.plot(t,g0)
  #ax.semilogx(w/(2.0*np.pi),mag)
  plt.ylabel(r'$\text{Amplitud} \left[\si{\milli\volt}\right]$')
  plt.xlabel(r'$\text{Tiempo} \left[\si{\nano\second}\right]$',x=0.9,ha='right')
  #plt.ylim(0.01,1.0)
  #plt.xlim(0,10)
  plt.show()
