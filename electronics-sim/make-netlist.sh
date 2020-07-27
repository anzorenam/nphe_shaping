#!/bin/bash

declare -a Cfed=("100p" "200p" "400p")
declare -a Rfed=("3k" "6k" "12k")

Cin="100p"
Rin="100k"
for i in "${Cfed[@]}"
do
  for j in "${Rfed[@]}"
  do
    python netlist.py "$i" "$j" "$Cin" "$Rin"
    ngspice -o sim.log -b preamp.cir > tem.txt
  done
done

rm sim.log
rm tem.txt
