import json
import numpy as np
import os, sys
from scipy.spatial.transform import Rotation as R

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
from aocs_lab.utils import lib

def theta_measure_to_quat(
        theta_deg_LB_measure: list[list], 
        A_LS_measure: list[list],  
        q_BS_design: list):   
                
    # theta_deg_LB_measure 棱镜到机械系精测矩阵
    # A_LS_measure 棱镜到星敏测量系矩阵
    # q_BS_design 安装四元数设计值
    z_S = np.array([0,0,1])

    # 计算星敏设计值
    A_SB_design = R.from_quat(q_BS_design, scalar_first=True).as_matrix() # 该转换函数与 matlab 的 quat2dcm 相反，需要格外注意
    z_B_design = A_SB_design.T @ z_S

    # 计算星敏测量值
    A_LB_measure = lib.theta_deg_to_cos_matrix(theta_deg_LB_measure)
    A_SB_measure = np.array(A_LS_measure).T @ A_LB_measure
    z_B_measure = A_SB_measure.T @ z_S
    q_BS_mesaure = R.from_matrix(A_SB_measure).as_quat(scalar_first=True)

    # 测量值与设计值相对关系
    A_SmSd = A_SB_measure @ A_SB_design.T
    rotvec_SmSd = R.from_matrix(A_SmSd).as_rotvec(degrees=True)
    rotvec_SmSd_norm_deg = np.linalg.norm(rotvec_SmSd)

    light_axis_err_deg = np.rad2deg(lib.vector_angle(z_B_measure, z_B_design))

    if lib.orthogonality_error(A_LB_measure) > 1e-5:
        raise(f"精测矩阵正交性误差: {lib.orthogonality_error(A_LB_measure):.3e}", )

    return q_BS_mesaure, light_axis_err_deg, rotvec_SmSd_norm_deg


def sar_data_process():
    with open('./piesat2_BC.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_file_SAR = open('output_SAR.txt', 'w', encoding="utf-8")

    SAR_list = data['sat_type_C']['SAR_list']
    q_BS_design = data['sat_type_C']['SAR_q_BS_design']

    for sat_index, SAR_position in enumerate(SAR_list):
        # A_SB S:SAR 天线坐标系，B:卫星本体系
        A_SB = lib.theta_deg_to_cos_matrix(SAR_position['SAR_theta_matrix_SB_deg'])
        print(f'精测矩阵正交性误差 {lib.orthogonality_error(A_SB)}')
        if lib.orthogonality_error(A_SB) > 1e-5:
            raise(f"精测矩阵正交性误差: {lib.orthogonality_error(A_SB):.3e}")

        A_BS = A_SB.T
        q_BS = lib.dcm2quat(A_BS)

        rotvec_BS = R.from_matrix(A_BS).as_rotvec(degrees=True)
        rotvec_BS_norm_deg = np.linalg.norm(rotvec_BS)

        print(f"卫星编号 C0{sat_index+1}:", file=output_file_SAR)
        # print(f"    精测矫正后安装四元数:", file=output_file_SAR)
        # [print(f"      {x:13.10f}", file=output_file_SAR) for x in q_BS]
        # print(f"    z轴安装偏差: {light_axis_err:.3f} deg", file=output_file_SAR)
        # print(f"    安装偏差(欧拉转角): {rotvec_BS_norm_deg:.3f} deg", file=output_file_SAR)
        print(f"set_sar_install_quat(\n{q_BS[0]:.13f},\n{q_BS[1]:.13f},\n{q_BS[2]:.13f},\n{q_BS[3]:.13f});\n", file=output_file_SAR)


if __name__ == "__main__":
    with open('./piesat2_BC.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_file = open('output_star_tracker.txt', 'w', encoding="utf-8")

    sat_list = data['sat_type_C']['sat_list']
    q_BS_design_list = data['sat_type_C']['q_BS_design']

    for sat_index, star_trackers_of_one_sat in enumerate(sat_list):
        print(f"卫星编号 C0{sat_index+1}:", file=output_file)
        for star_tracker_index, (star_tracker, q_BS_design) in enumerate(zip(star_trackers_of_one_sat, q_BS_design_list)):
            q_BS, light_axis_err, rotvec_norm_deg = theta_measure_to_quat(
                star_tracker['theta_matrix_LB_deg'], 
                star_tracker['A_LS'], 
                q_BS_design)

            if star_tracker_index == 0:
                name = 'A'
            elif star_tracker_index == 1:
                name = 'B'
            else:
                raise(f"星敏编号错误: {star_tracker_index}")
            print(f"  // 星敏 {name}:", file=output_file)
            # print(f"    精测矫正后安装四元数:", file=output_file)
            # [print(f"      {x:13.10f}", file=output_file) for x in q_BS]
            # print(f"    光轴安装偏差: {light_axis_err:.3f} deg", file=output_file)
            # print(f"    星敏安装偏差(欧拉转角): {rotvec_norm_deg:.3f} deg", file=output_file)

            print(f"GsStaSetPosQuat(\nGS_CID_{name},\n{q_BS[0]},\n{q_BS[1]},\n{q_BS[2]},\n{q_BS[3]});\n", file=output_file)

    sar_data_process()



