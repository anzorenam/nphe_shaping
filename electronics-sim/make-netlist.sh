#!/bin/bash

declare -a tpeaks=("75" "100" "125" "150" "175")
declare -a degree=("3" "5")
declare -a Cfed=("100p" "200p" "400p")
declare -a Rfed=("3k" "6k" "12k")

Cin="100p"
Rin="100k"

for k in "${tpeaks[@]}"
do
  for d in "${degree[@]}"
  do
    for i in "${Cfed[@]}"
    do
      for j in "${Rfed[@]}"
      do
        python netlist.py 0 "$k" "$d" "$i" "$j" "$Cin" "$Rin"
        ngspice -o sim.log -b preamp-a0.cir > tem.txt
      done
    done
  done
done

rm sim.log
rm tem.txt

for k in "${tpeaks[@]}"
do
  for d in "${degree[@]}"
  do
    for i in "${Cfed[@]}"
    do
      for j in "${Rfed[@]}"
      do
        python netlist.py 1 "$k" "$d" "$i" "$j" "$Cin" "$Rin"
        ngspice -o sim.log -b preamp-a1.cir > tem.txt
      done
    done
  done
done

rm sim.log
rm tem.txt
