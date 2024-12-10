from math import sqrt, sin, cos, pi
from . import constants
import numpy as np
from scipy.spatial.transform import Rotation as R

def latitude_to_angular_velocity(latitude):
    # 返回在当地东北天坐标系下的速度分量
    omega_north = constants.EARTH_ROTATION_RATE * cos(latitude)
    omega_up = constants.EARTH_ROTATION_RATE * sin(latitude)

    return [0, omega_north, omega_up]

def orbit_period(semimajor_axis):
    return sqrt( 4*pi**2 * semimajor_axis**3 / constants.GM_EARTH ) # Kepler's Third laws of planetary motion

def orbit_angular_rate(semimajor_axis):
    return 2*pi / orbit_period(semimajor_axis)

# https://en.wikipedia.org/wiki/Latitude#Latitude_on_the_ellipsoid



def orthogonality_error(A: np.array):
    """
    计算矩阵 A 的正交性误差，基于 Frobenius 范数的偏离度计算。
    """
    I = np.eye(A.shape[1])  # 单位矩阵
    error_matrix = A.T @ A - I  # 计算 A^T A 与 I 的差
    frobenius_norm = np.linalg.norm(error_matrix, 'fro')  # Frobenius 范数
    return frobenius_norm

def theta_deg_to_cos_matrix(theta_deg):
    theta_rad = np.deg2rad(theta_deg)
    A = np.cos(theta_rad)    
    return A

def vector_angle(v1, v2):
    dot_product = np.dot(v1, v2)

    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(cos_theta)

    return angle

def unit_vector(vector: list) -> list:
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def sphere_unit_vector(latitude: float, longitude: float):
    """
    计算球坐标系下的单位矢量。
    """

    x = np.cos(latitude) * np.cos(longitude)
    y = np.cos(latitude) * np.sin(longitude)
    z = np.sin(latitude)

    return np.array([x, y, z])

def dcm2quat(A_FG: np.array):
    """
    方向余弦矩阵到四元数的转换。与 MATLAB dcm2quat 定义一致。
    """
    A_GF = A_FG.T
    q_FG = R.from_matrix(A_GF).as_quat(scalar_first=True)

    return q_FG

def quat2dcm(q_FG: list):
    """
    四元数到方向余弦矩阵的转换。与 MATLAB quat2dcm 定义一致。
    """
    A_GF = R.from_quat(q_FG, scalar_first=True).as_matrix()

    return A_GF.T

def rotate_z(rot):
    # 2.164 (Markley 2014)
    return np.array([[ cos(rot),  sin(rot),  0],
                     [-sin(rot),  cos(rot),  0],
                     [        0,         0,  1]])

def rotate_x(rot):
    # 2.164 (Markley 2014)
    return np.array([[ 1,         0,        0],
                     [ 0,  cos(rot),  sin(rot)],
                     [ 0, -sin(rot),  cos(rot)]])


if __name__ == "__main__":
    q = [0.7071, 0.7071, 0, 0]

    A = quat2dcm(q)

    print(A)
    
    print(dcm2quat(A))