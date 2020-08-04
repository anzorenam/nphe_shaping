#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import argparse
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('amp', help='select amp',type=int)
parser.add_argument('tp', help='peaking time',type=int)
parser.add_argument('degree', help='filter order',type=int)
parser.add_argument('cf', help='feedback C',type=str)
parser.add_argument('rf', help='feedback R',type=str)
parser.add_argument('ci', help='input C',type=str)
parser.add_argument('ri', help='input R',type=str)
args=parser.parse_args()

amp=args.amp
tp=args.tp
degree=args.degree
cf=args.cf
rf=args.rf
ci=args.ci
ri=args.ri
jin='10mA'

Cfeed=np.float(cf[:-1])
Rfeed=np.float(rf[:-1])
tint=Cfeed*Rfeed
Cdiff=Cfeed

fwtm=2.0*tp
sigma0=np.exp(1)/np.sqrt(2.0*np.pi)
if degree==5:
  tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(15.55)))
  sigma=tau0*sigma0
  a0=(1.0/sigma)*(1.4766878)
else:
  tau0=fwtm/(2.0*sigma0*np.sqrt(2.0*np.log(2.9)))
  sigma=tau0*sigma0
  a0=(1.0/sigma)*(1.2633573)
td=1.0/(a0-1.0/tint)
Rdiff=np.round(1.0e3*(td/Cdiff))

fnet=open('preamp-temp{0}.net'.format(amp),'r')
fout=open('preamp-a{0}.cir'.format(amp),'w')
ndata='trans-{0}_tp{1}d{2}-{3}{4}.dat'.format(amp,tp,degree,cf,rf)
Cnet=fnet.readlines()
Cnet.insert(2,'.param cfed={0}\n'.format(cf))
Cnet.insert(3,'.param rfed={0}\n'.format(rf))
Cnet.insert(4,'.param cin={0}\n'.format(ci))
Cnet.insert(5,'.param rin={0}\n'.format(ri))
Cnet.insert(6,'.param rdiff={0}\n'.format(Rdiff))
Cnet.insert(9,'is vin 0 dc 0 ac {0}\n'.format(jin))
if amp==0:
  Cnet.insert(26,'echo transimpedance > {0}\n'.format(ndata))
  Cnet.insert(30,'wrdata {0} v(onoise_total)\n'.format(ndata))
  Cnet.insert(32,'wrdata {0} real(vout)/{1} imag(vout)/{1}\n'.format(ndata,jin))
  Cnet.insert(34,'wrdata {0} real(vout)/{1} imag(vout)/{1}\n'.format(ndata,jin))
else:
  Cnet.insert(27,'echo transimpedance > {0}\n'.format(ndata))
  Cnet.insert(31,'wrdata {0} v(onoise_total)\n'.format(ndata))
  Cnet.insert(33,'wrdata {0} real(vout)/{1} imag(vout)/{1}\n'.format(ndata,jin))
  Cnet.insert(35,'wrdata {0} real(vout)/{1} imag(vout)/{1}\n'.format(ndata,jin))

for elem in Cnet:
  fout.write(elem)
fnet.close()
fout.close()
