#!/bin/bash


SIMULATION_ID="sim-$1"
NUMBER_OF_DEVICES=$2
NUMBER_OF_SIGNALS_FROM_DEVICE=$3
URL=$4
echo 'starting simulation ' $SIMULATION_ID
for (( i=1; i<=$NUMBER_OF_DEVICES; i++ ))
do
  DEVICE_ID="$SIMULATION_ID-device-$i-$(date +%s000)"
  echo "starting device $DEVICE_ID with $NUMBER_OF_SIGNALS_FROM_DEVICE signals"
  python3 simulate.py \
    --device_id=$DEVICE_ID \
    --number_of_signals=$NUMBER_OF_SIGNALS_FROM_DEVICE \
    --url=$URL
  echo "DONE device $DEVICE_ID"
done