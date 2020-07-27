#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import argparse

parser=argparse.ArgumentParser()
parser.add_argument('cf', help='feedback C',type=str)
parser.add_argument('rf', help='feedback R',type=str)
parser.add_argument('ci', help='input C',type=str)
parser.add_argument('ri', help='input R',type=str)
args=parser.parse_args()

cf=args.cf
rf=args.rf
ci=args.ci
ri=args.ri
jin='10mA'

fnet=open('preamp-template.net','r')
fout=open('preamp.cir','w')
ndata='trans_{0}{1}.dat'.format(cf,rf)
Cnet=fnet.readlines()
Cnet.insert(2,'.param cfed={0}\n'.format(cf))
Cnet.insert(3,'.param rfed={0}\n'.format(rf))
Cnet.insert(4,'.param cin={0}\n'.format(ci))
Cnet.insert(5,'.param rin={0}\n'.format(ri))
Cnet.insert(8,'is vin 0 dc 0 ac {0}\n'.format(jin))
Cnet.insert(25,'echo transimpedance > {0}\n'.format(ndata))
Cnet.insert(29,'wrdata {0} v(onoise_total)\n'.format(ndata))
Cnet.insert(31,'wrdata {0} real(vout)/{1} imag(vout)/{1}\n'.format(ndata,jin))
Cnet.insert(33,'wrdata {0} real(vout)/{1} imag(vout)/{1}\n'.format(ndata,jin))

for elem in Cnet:
  fout.write(elem)
fnet.close()
fout.close()
