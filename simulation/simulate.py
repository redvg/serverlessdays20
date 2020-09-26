#!/usr/bin/env python3


import argparse
import datetime
import os
import time
import json
import random
import requests


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=('Signal simulator'))
    parser.add_argument(
        '--device_id', 
        required=True, 
        help='Device ID',
    )
    parser.add_argument(
        '--number_of_signals',
        type=int,
        default=100,
        help='Number of signals to publish',
    )
    parser.add_argument(
        '--events_per_second',
        type=int,
        default=10,
        help='Number of signals per second',
    )
    parser.add_argument(
        '--token',
        default="qET@23f,fA8~rJ$Fk[@3gV==ZM;?D:T",
        help='Authorization token',
    )
    parser.add_argument(
        '--endpoint', 
        required=True, 
        help='FQDN',
    )
    return parser.parse_args()

def main():
    args = parse_command_line_args()
    device_id = args.device_id
    assert len(device_id) > 0, 'Invalid device id'
    number_of_signals = args.number_of_signals
    assert number_of_signals > 0, 'At least 1 signal expected'
    events_per_second = args.events_per_second
    assert events_per_second > 0, 'Invalid frequency'
    frequency = 1 / events_per_second
    token = args.token
    assert len(token) > 0, 'Invalid token'
    endpoint = args.endpoint
    assert len(endpoint) > 0, 'Invalid URL'

    random.seed(args.device_id)  # A given device ID will always generate the same random data

    initial_temperature = random.randint(-20, 20)
    simulated_temperature = initial_temperature + random.random() * 20

    if random.random() > 0.5:
        temperature_trend = +.1
    else:
        temperature_trend = -.1

    for i in range(1, number_of_signals + 1):
        simulated_temperature = simulated_temperature + temperature_trend * random.normalvariate(0.01,0.005)
        payload = {
            "timestamp": int(time.time()), 
            "device": device_id,
            "temperature": simulated_temperature,
        }
        headers = {"Authorization": "Bearer " + token}
        print('Publishing message {} of {} in {}'.format(i, number_of_signals, device_id))
        r = requests.post(endpoint, json=payload, headers=headers)
        if r.status_code == 200:
            print('ok')
        else:
            print('FAILED')
        # Sends {frequency} events per second
        # time.sleep(frequency)

if __name__ == '__main__':
    main()