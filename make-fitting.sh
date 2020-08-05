#!/bin/bash

declare -a scales=("tstep-0.5" "tstep-1.0" "tstep-2.0")
declare -a amps=("0" "1")
declare -a crange=("0" "1")

main_folder="fitting"

mkdir $main_folder
mkdir $main_folder/amp_stats0
mkdir $main_folder/amp_stats1

for s in "${scales[@]}"
do
  mkdir $main_folder/amp_stats0/"$s"
  mkdir $main_folder/amp_stats1/"$s"
done

for j in "${amps[@]}"
do
  for k in "${crange[@]}"
  do
    python tot-fitting.py "$j" 3 "$k"
  done
done

for j in "${amps[@]}"
do
  for k in "${crange[@]}"
  do
    python tot-fitting.py "$j" 5 "$k"
  done
done
