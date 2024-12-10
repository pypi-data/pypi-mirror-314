import numpy as np
import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
import aocs_lab.sun_time as sun_time

if __name__ == "__main__":
    # 太阳矢量与轨道面法线夹角
    beta_angle = np.deg2rad(31)
    sun_time.sun_time(beta_angle, 6900e3)

    beta_angle = np.deg2rad(67)
    sun_time.sun_time(beta_angle, 6900e3)