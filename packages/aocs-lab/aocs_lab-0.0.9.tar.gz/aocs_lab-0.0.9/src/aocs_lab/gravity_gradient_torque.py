import numpy as np
from .utils import lib as lib
from .utils import constants as constants


def gen_sphere_unit_vector_list():
    n = []
    for lat in range(-90, 90, 5):
        for lon in range(0, 360, 5):
            n.append(lib.sphere_unit_vector(np.deg2rad(lat), np.deg2rad(lon)))

    return n

def calc_gravity_gradient_torque(I: np.ndarray, r: float, n: list)-> np.ndarray:
    """
    计算重力梯度力矩。
    I: 本体系惯量矩阵
    r: 质心到地心的距离
    n: 引力方向在本体系的表示（单位矢量）
    """
    
    # 确保 I 是 3x3 矩阵
    assert I.shape == (3, 3), "I must be a 3x3 matrix"

    # 单位化
    n = lib.unit_vector(n)

    # 计算重力梯度力矩
    torque = (3 * constants.GM_EARTH / r**3) * np.cross(n, I@n)

    return torque

def get_max_torque(I, r: float) -> float:
    n_list = gen_sphere_unit_vector_list()
    L_list = []
    for n in n_list:
        L_list.append(calc_gravity_gradient_torque(I, 6900e3, n))

    max_torque = max(L_list, key=np.linalg.norm)

    return np.linalg.norm(max_torque)

# 用于测试
# 在 src 目录下执行以下命令
# py -m aocs_lab.gravity_gradient_torque
if __name__ == '__main__':
    I = np.array([[89, 19, -7], 
                  [19, 341, 2], 
                  [-7, 2, 294]])
    
    r = 6900e3

    max_torque = get_max_torque(I, r)

    print(max_torque)