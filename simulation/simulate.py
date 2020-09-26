#!/usr/bin/env python3


import argparse
import datetime
import os
import time
import json
import random
import requests
import asyncio
import aiohttp


def _parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=('Signal simulator'))
    parser.add_argument(
        '--simulation_id',
        required=True, 
        help='Simulation ID',
    )
    parser.add_argument(
        '--number_of_devices',
        type=int,
        default=3, 
        help='Number of devices in operation',
    )
    parser.add_argument(
        '--number_of_signals',
        type=int,
        default=100,
        help='Number of signals to publish',
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

def make_request(endpoint, payload, headers):
    return requests.post(endpoint, json=json.dumps(payload), headers=headers)

async def _run_one(device_id, number_of_signals, token, endpoint):
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
        loop = asyncio.get_event_loop()
        f = loop.run_in_executor(None, make_request, endpoint, payload, headers)
        r = await f
        print(r.reason)

async def main():
    args = _parse_command_line_args()
    simulation_id = args.simulation_id
    assert len(simulation_id) > 0, 'Invalid ID'
    number_of_devices = args.number_of_devices
    assert number_of_devices > 0, 'At least 1 device expected'
    number_of_signals = args.number_of_signals
    assert number_of_signals > 0, 'At least 1 signal expected'
    token = args.token
    assert len(token) > 0, 'Invalid token'
    endpoint = args.endpoint
    assert len(endpoint) > 0, 'Invalid URL'

    tasks = []
    for each in range(0, number_of_devices):
        tasks.append(_run_one("{}-device-{}".format(simulation_id, str(each+1)), number_of_signals, token, endpoint))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())