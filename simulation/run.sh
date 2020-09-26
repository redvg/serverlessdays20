#!/bin/bash


SIMULATION_ID="sim-$1"
NUMBER_OF_DEVICES=$2
NUMBER_OF_SIGNALS_FROM_DEVICE=$3
ENDPOINT=$4
echo "starting simulation $SIMULATION_ID"
python3 simulate.py \
  --simulation_id=$SIMULATION_ID \
  --number_of_devices=$NUMBER_OF_DEVICES \
  --number_of_signals=$NUMBER_OF_SIGNALS_FROM_DEVICE \
  --endpoint=$ENDPOINT
echo "DONE $SIMULATION_ID"
