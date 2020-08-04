#!/bin/bash

declare -a amps=("0" "1")
declare -a degree=("3" "5")

date
for j in "${amps[@]}"
do
  for k in "${degree[@]}"
  do
    python nphoton-shaping.py "$j" "$k" 0 &
    python nphoton-shaping.py "$j" "$k" 1 &
    wait
  done
done

for j in "${amps[@]}"
do
  for k in "${degree[@]}"
  do
    python nphoton-shaping.py "$j" "$k" 2 &
    python nphoton-shaping.py "$j" "$k" 3 &
    wait
  done
done

date
