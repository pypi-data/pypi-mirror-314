import numpy as np

import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
from aocs_lab.utils import time
from aocs_lab.influxdb import influxdb2
from aocs_lab.wheel import wheel_data_process

def gen_database(sat_name: str) -> dict:
    database = {}
    database['url'] = "http://172.16.110.211:8086"
    database['token'] = "u0OGUlvv6IGGYSxpoZGZNjenBtE-1ADcdun-W-0oacL66cef5DXPmDwVzj93oP1MRBBCCUOWNFS9yMb77o5OCQ=="
    database['org'] = "gs"
    database['bucket'] = f'piesat02_{sat_name}_database'

    return database

wheel_test = {
    "start_time": '2024-11-28T09:50:00',
    "end_time": '2024-11-28T10:06:00',
    "tm_tag": ['TMKA553', 'TMKA561', 'TMKA569', 'TMKA577']
}

data_list = influxdb2.get_field_value_from_influxdb(
    gen_database('c02'),
    time.beijing_to_utc_time_str(wheel_test['start_time']), 
    time.beijing_to_utc_time_str(wheel_test['end_time']), 
    wheel_test['tm_tag'])

data_array = np.array(data_list)


for i in range(len(wheel_test['tm_tag'])):
    dt = wheel_data_process.calc_slide_time(data_array[:,0], data_array[:,i+1], 5990, 3000)
    print(f"飞轮 {i+1} 惯滑时间为 {dt:.0f} s")

