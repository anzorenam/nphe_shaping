* ada4807 spice macro-model

* function: amplifier
*
* revision history:
* rev. 4.0 dec 2014 -tc
* copyright 2014 by analog devices
*
* refer to http://www.analog.com/analog_root/static/techsupport/designtools/spicemodels/license
* for license statement. use of this model indicates your acceptance
* of the terms and provisions in the license staement.
*
* tested in multisim, simetrix(ngspice), psice
*
* not modeled: distortion, psrr, overload recovery, bias current at high vcm,
*                       disable turn on/turn off time, change in noise for high vcm,
*
* parameters modeled include:
*   vos, ibias, input cm limits and typ output voltge swing over full supply range, cmrr,
*   open loop gain & phase, slew rate, output current limits, voltage & current noise over temp,
*   capacitive load drive, quiescent and dynamic supply currents,
*   disable pin functionality, single supply & offset supply functionality.
*
* node assignments
*                             non-inverting input
*                              |     inverting input
*                              |      |      positive supply
*                              |      |      |      negative supply
*                              |      |      |      |      output
*                              |      |      |      |      |      disable bar
*                              |      |      |      |      |      |
.subckt ada4807 100 101 102 103 104 106

***power supplies***
ibias	102	103	dc	2.4e-6
dzps	98	102	diode
iquies	102	98	dc	0.9976e-3
*s1	98	103	106	113	switch
as1	%v(106)	%gd(98 103) switch
r1	102	99	rideal	1e7
r2	99	103	rideal	1e7
e1	111	110	102	110	1
e2	110	112	110	103	1
e3	110	0	99	0	1

***inputs***
*s2	1	100	106	113	switch
as2	%v(106)	%gd(1 100) switch
*s3	9	101	106	113	switch
as3	%v(106)	%gd(9 101) switch

vos	1	2	dc	20e-6
ibiasp	110	2	dc	-1.2e-6
ibiasn	110	9	dc	-1.2e-6
rincmp	110	2	rideal	45e6
rincmn	9	110	rideal	45e6
cincmp	110	2	4.5e-12
cincmn	9	110	4.5e-12
ios	9	2	dc	1e-7
rindiff	9	2	rideal	35e3
cindiff	9	2	0.4e-012

***non-inverting input with clamp***
g1	3	110	110	2	0.001
rinp	3	110	rideal	1e3
rx1	40	3	rideal	0.001
dinp	40	41	diode
dinn	42	40	diode
vinp	111	41	dc	0.35
vinn	42	112	dc	0.35

***vnoise***
hvn	6	5	vmeas1	707.1067812
vmeas1	20	110	dc	0
vvn	21	110	dc	0.65
dvn	21	20	dvnoisy
hvn1	6	7	vmeas2	707.1067812
vmeas2	22	110	dc	0
vvn1	23	110	dc	0.65
dvn1	23	22	dvnoisy

***inoise***
fnin	9	110	vmeas3	0.70710678
vmeas3	51	110	dc	0
vnin	50	110	dc	0.65
dnin	50	51	dinnoisy
fnin1	110	9	vmeas4	0.70710678
vmeas4	53	110	dc	0
vnin1	52	110	dc	0.65
dnin1	52	53	dinnoisy

fnip	2	110	vmeas5	0.70710678
vmeas5	31	110	dc	0
vnip	30	110	dc	0.65
dnip	30	31	dipnoisy
fnip1	110	2	vmeas6	0.70710678
vmeas6	33	110	dc	0
vnip1	32	110	dc	0.65
dnip1	32	33	dipnoisy

***cmrr***
rcmrrp	3	10	rideal	1e12
rcmrrn	10	9	rideal	1e12
g10	11	110	10	110	0.565e-9
lcmrr	11	12	15.9e-3
rcmrr	12	110	rideal	1e3
e4	5	3	11	110	1

***power down***
vpd	0	85	dc	1.055
vpd1	81	0	dc	0.3
rpd	111	106	rideal	1.6e9
epd	80	113	82	0	1
rdp1	82	0	rideal	1e3
cpd	82	0	1e-10
*s5	81	82	106	113	switch
as5	%v(106)	%gd(81 82) switch
epd1	111	80	83	0	1
dzpd	0	83	dpd
rpd2	84	83	rideal	1e6
epd2	84	85	111	112             1

***feedback pin***
*rf	105	104	rideal	0.001

***vfb stage***
g200	200	110	7	9	1
r200	200	110	rideal	250
dzslewp	201	110	dzslewp
dzslewn	201	200	dzslewn

***1st pole***
g210	210	110	200	110	4.9046e-6
r210	210	110	rideal	2.8937e9
c210	210	110	1e-012

***output voltage clamp-1***
rx2	60	210	rideal	0.001
dzvoutp	61	60	dzvoutp
dzvoutn	60	62	dzvoutn
dvoutp	61	63	diode
dvoutn	64	62	diode
voutp	65	63	dc	5.1355
voutn	64	66	dc	5.1355
e60	65	110	111	110	2.71
e61	66	110	112	110	2.71

*** 11 frequency stages ***
g220	220	110	210	110	0.001
r220	220	110	rideal	1000
c220	220	221	0.87448e-12
r221	221	110	rideal	13e3

g230	230	110	220	110	0.001
r230	230	110	rideal	1000
c230	230	110	0.46132e-12

g240	240	110	230	110	0.001
r240	240	110	rideal	1000
c240	240	110	0.05895e-12

g245	245	110	240	110	0.001
r245	245	110	rideal	1000
c245	245	110	0.02842e-12

g250	250	110	245	110	0.001
r250	250	110	rideal	1000
c250	250	110	0.02842e-12

g255	255	110	250	110	0.001
r255	255	110	rideal	1000
c255	255	110	0.02842e-12

g260	260	110	255	110	0.001
r260	260	110	rideal	1000
c260	260	110	0.02842e-12

g265	265	110	260	110	0.001
r265	265	110	rideal	1000
c265	265	110	0.02842e-12

g270	270	110	265	110	0.001
r270	270	110	rideal	1000
c270	270	110	0.02842e-12

e280	280	110	270	110	1
r280	280	285	rideal	10
l280	285	281	7.67e-9
c280	281	282	637.06e-12
r281	282	110	rideal	12.2

e290	290	110	285	110	1
r290	290	292	rideal	10
l290	290	291	4.91e-9
c290	291	292	70.74e-12
r291	292	110	rideal	168.77
e295	295	110	292	110	1.0593

***output stage***
g300	300	110	295	110	0.001
r300	300	110	rideal	1000
e301	301	110	300	110	1
rout	301	302	rideal	114
lout	302	310	24e-009
cout	310	110	0.4e-012

***output current limit***
vioutp	71	310	dc	8.35
vioutn	310	72	dc	7.782
dioutp	70	71	diode
dioutn	72	70	diode
rx3	70	300	rideal	0.001

***output clamp-2***
voutp1	111	73	dc	0.815
voutn1	74	112	dc	0.815
dvoutp1	75	73	diode
dvoutn1	74	75	diode
rx4	75	310	rideal	0.001

***supply currents***
fiovcc	314	110	vmeas8	1
vmeas8	310	311	dc	0
r314	110	314	rideal	1e9
dzovcc	110	314	diode
dovcc	102	314	diode
rx5	311	312	rideal	0.001
fiovee	315	110	vmeas9	1
vmeas9	312	313	dc	0
r315	315	110	rideal	1e9
dzovee	315	110	diode
dovee	315	103	diode

***output switch***
*s4	104	313	106	113	switch
as4	%v(106)	%gd(104 313) switch

*** common models***
.model	diode	d(bv=100)
.model	switch aswitch(cntl_off=0.299 cntl_on=0.301 r_off=1e6 r_on=0.001 log=true)
.model	dzvoutp	d(bv=4.3)
.model	dzvoutn	d(bv=4.3)
.model	dzslewp	d(bv=66.5)
.model	dzslewn d(bv=76.1)
.model	dpd     d(bv=3.416)
.model	dvnoisy	d(is=3.66e-016 kf=8.03e-018)
.model	dinnoisy	d(is=1.83e-017 kf=6.64e-016)
.model	dipnoisy	d(is=1.83e-017 kf=6.64e-016)
.model	rideal	res(noisy)
*
.ends
