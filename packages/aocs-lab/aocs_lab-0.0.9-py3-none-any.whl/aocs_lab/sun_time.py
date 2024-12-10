import numpy as np
from .utils import lib as lib
from .utils import constants as constants

# 计算太阳矢量在轨道系的某个平面的照射情况
def sun_time(beta_angle, semimajor_axis):
    # 地球矢量
    v_earth = np.array([0, 0, 1])

    # 太阳矢量与地球矢量夹角阈值（太阳升起）
    theta = np.arcsin(constants.EARTH_EQUATORIAL_RADIUS/semimajor_axis)

    # 圆锥矢量遍历
    earth_sun_angle = np.array([])
    phi_line = np.linspace(0, 2*np.pi, 1000)

    for phi in phi_line:
        y = np.cos(np.pi-beta_angle)
        xz = np.sin(np.pi-beta_angle)
        v_sun = np.array([xz*np.sin(phi), y, xz*np.cos(phi)])

        angle = lib.vector_angle(v_sun, v_earth)
        earth_sun_angle = np.append(earth_sun_angle, angle)

    shadow_segment = np.where(earth_sun_angle < theta)
    sun_segment = np.where(earth_sun_angle >= theta)

    # 有效时间计算
    valid_segment_len = sun_segment[0].__len__()
    valid_segment_time = valid_segment_len / phi_line.__len__() * lib.orbit_period(semimajor_axis)

    print("轨道周期 (s):", lib.orbit_period(semimajor_axis))
    print("阳照区时长 (s):", valid_segment_time)


if __name__ == "__main__":
    # 太阳矢量与轨道面法线夹角
    beta_angle = np.deg2rad(31)
    sun_time(beta_angle, 6900e3)

    beta_angle = np.deg2rad(67)
    sun_time(beta_angle, 6900e3)