*ada4891 macro-model

*function:amplifier
*
*revision history:
*rev.2.1 oct 2016-jl
*copyright 2016 by analog devices
*
*refer to http://www.analog.com/analog_root/static/techsupport/designtools/spicemodels/license
*for license statement. use of this model indicates your acceptance
*of the terms and provisions in the license staement.
*
*tested on multsim, simetrix(ngspice), pspice
*
*not modeled: distortion, psrr, overload recovery,
*             shutdown turn on/turn off time
*
*parameters modeled include:
*   vos, ibias, input cm limits and typ output voltge swing over full supply range,
*   open loop gain & phase, slew rate, output current limits, voltage & current noise over temp,
*   capacitive load drive, quiescent and dynamic supply currents.
*
*
*
*node assignments
*                non-inverting input
*                |   inverting input
*                |   |   positive supply
*                |   |   |   negative supply
*                |   |   |   |   output
*                |   |   |   |   |
*                |   |   |   |   |
.subckt ada4891 100 101 102 103 104

***power supplies***
rz1	102	1020	rideal	1e-6
rz2	103	1030	rideal	1e-6
ibias	1020	1030	dc	0.01e-3
dzps	98	1020	diode
iquies	1020	98	dc	4.39e-3
*s1	98	1030	106	113	switch
as1	%v(106)	%gd(98 1030) switch
r1	1020	99	rideal	1e7
r2	99	1030	rideal	1e7
e1	111	110	1020	110	1
e2	110	112	110	1030	1
e3	110	0	99	0	1

***inputs***
*s2	1	100	106	113	switch
as2	%v(106)	%gd(1 100) switch
*s3	9	101	106	113	switch
as3	%v(106)	%gd(9 101) switch
vos	1	2	dc	2.5e-3
ibiasp	110	2	dc	2e-12
ibiasn	110	9	dc	2e-12
rincmp	110	2	rideal	5000e6
rincmn	9	110	rideal	5000e6
cincmp	110	2	2.2e-12
cincmn	9	110	2.2e-12
ios	9	2	1e-15
rindiff	9	2	rideal	10000e3
cindiff	9	2	0.8e-12

***non-inverting input with clamp***
g1	3	110	110	2	0.001
rinp	3	110	rideal	1e3
rx1	40	3	rideal	0.001
dinp	40	41	diode
dinn	42	40	diode
vinp	111	41	dc	1.26
vinn	42	112	dc	0.16

***vnoise***
hvn	6	5	vmeas1	707.10678
vmeas1	20	110	dc	0
vvn	21	110	dc	0.65
dvn	21	20	dvnoisy
hvn1	6	7	vmeas2	707.10678
vmeas2	22	110	dc	0
vvn1	23	110	dc	0.65
dvn1	23	22	dvnoisy

***inoise***
fnin	9	110	vmeas3	0.7071068
vmeas3	51	110	dc	0
vnin	50	110	dc	0.65
dnin	50	51	dinnoisy
fnin1	110	9	vmeas4	0.7071068
vmeas4	53	110	dc	0
vnin1	52	110	dc	0.65
dnin1	52	53	dinnoisy

fnip	2	110	vmeas5	0.7071068
vmeas5	31	110	dc	0
vnip	30	110	dc	0.65
dnip	30	31	dipnoisy
fnip1	110	2	vmeas6	0.7071068
vmeas6	33	110	dc	0
vnip1	32	110	dc	0.65
dnip1	32	33	dipnoisy

***cmrr***
rcmrrp	3	10	rideal	1e12
rcmrrn	10	9	rideal	1e12
g10	11	110	10	110	-8.437e-9
lcmrr	11	12	8e-3
rcmrr	12	110	rideal	1e3
e4	5	3	11	110	1

***power down***
vpd	111	80	dc	2
vpd1	81	0	dc	1.5
rpd	111	106	rideal	1e6
epd	80	113	82	0	1
rdp1	82	0	rideal	1e3
cpd	82	0	1e-10
*s5	81	82	83	113	switch
as5	%v(83)	%gd(81 82) switch
cdp1	83	0	1e-12
rpd2	106	83	1e6

***feedback pin***
*rf	105	104	rideal	0.001

***vfb stage***
g200	200	110	7	9	1
r200	200	110	rideal	250
dzslewp	201	200	dzslewp
dzslewn	201	110	dzslewn

***dominant pole at 8.88 hz***
g210	210	110	200	110	3.378e-6
r210	210	110	rideal	17.92e6
c210	210	110	1e-012

***output voltage clamp-1***
rx2	60	210	rideal	0.001
dzvoutp	61	60	dzvoutp
dzvoutn	60	62	dzvoutn
dvoutp	61	63	diode
dvoutn	64	62	diode
voutp	65	63	dc	5.121
voutn	64	66	dc	5.095
e60	65	110	111	110	1.27
e61	66	110	112	110	1.27

***pole at 500mhz***
g220	220	110	210	110	0.001
r220	220	110	rideal	1000
c220	220	110	0.3183e-12

***pole at 800mhz***
g230	230	110	220	110	0.001
r230	230	110	rideal	1000
c230	230	110	0.1989e-12

***pole at 1200mhz***
g240	240	110	230	110	0.001
r240	240	110	rideal	1000
c240	240	110	0.1326e-12

***pole at 1500mhz***
g245	245	110	240	110	0.001
r245	245	110	rideal	1000
c245	245	110	0.1061e-12

***pole at 1700mhz***
g250	250	110	245	110	0.001
r250	250	110	rideal	1000
c250	250	110	0.0936e-12

***buffer***
g255	255	110	250	110	0.001
r255	255	110	rideal	1000

***buffer***
g260	260	110	255	110	0.001
r260	260	110	rideal	1000

***buffer***
g265	265	110	260	110	0.001
r265	265	110	rideal	1000

***buffer***
g270	270	110	265	110	0.001
r270	270	110	rideal	1000

***buffer***
e280	280	110	270	110	1
r280	280	285	rideal	10

***peak: f=210mhz, zeta=0.7, gain=0.2db***
e290	290	110	285	110	1
r290	290	292	rideal	10
l290	290	291	5.413e-9
c290	291	292	106.103e-12
r291	292	110	rideal	429.314
e295	295	110	292	110	1.0233

***output stage***
g300	300	110	295	110	0.001
r300	300	110	rideal	1000
e301	301	110	300	110	1
rout	302	303	rideal	 36
lout	303	310	 7e-9
cout	310	110	 1.3e-12

***output current limit***
h1	301	304	vsense1	100
vsense1	301	302	dc	0
vioutp	305	304	dc	19.836
vioutn	304	306	dc	30.036
dioutp	307	305	diode
dioutn	306	307	diode
rx3	307	300	rideal	0.001

***output clamp-2***
voutp1	111	73	dc	0.705
voutn1	74	112	dc	0.695
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

*** common models ***
.model	diode	d(bv=100)
.model	switch aswitch(cntl_off=1.495 cntl_on=1.505 r_off=1e6 r_on=0.001 log=true)
.model	dzvoutp	d(bv=4.3)
.model	dzvoutn	d(bv=4.3)
.model	dzslewp	d(bv=50.802)
.model	dzslewn	d(bv=62.643)
.model	dvnoisy	d(is=2.99e-15 kf=1.02e-14)
.model	dinnoisy	d(is=3.81e-19 kf=0.00e0)
.model	dipnoisy	d(is=3.81e-19 kf=0.00e0)
.model	rideal	res(noisy=0)

.ends
