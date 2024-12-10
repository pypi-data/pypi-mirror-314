import numpy as np

import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.lib as lib

# 上海厂房坐标 31.021018°N 121.393126°E
# 太原坐标 38.8°N 111.6°E， 厂房偏转角度 asin(37.1/58.7)

if __name__ == "__main__":
    # 坐标定义，当地东北天L，厂房东北天F，卫星本体系B
    omega_L = lib.latitude_to_angular_velocity(np.deg2rad(38.8))
    A_FL = lib.rotate_z(np.asin(37.1/58.7))  # 当地东北天 到 厂房东北天坐标系
    A_BF = lib.rotate_z(np.deg2rad(180))     # 卫星xyz对应西南天，相对厂房西北天旋转180deg
  
    omega_B = A_BF @ A_FL @ omega_L
    omega_B_deg = np.rad2deg(omega_B)

    print(f'卫星本体系理论角速度')
    print(f'x: {omega_B_deg[0]:10.6f} deg/s')
    print(f'y: {omega_B_deg[1]:10.6f} deg/s')
    print(f'z: {omega_B_deg[2]:10.6f} deg/s')
