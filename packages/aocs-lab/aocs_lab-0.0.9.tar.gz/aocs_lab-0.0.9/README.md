# 姿轨控工具箱

## 使用说明

安装 (使用清华源)

`pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple aocs-lab`

升级到最新版

`pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade aocs-lab`

使用示例

```py
import aocs_lab.sun_time as st
import numpy as np

if __name__ == "__main__":
    # 太阳矢量与轨道面法线夹角 31 deg
    beta_angle = np.deg2rad(31)
    st.sun_time(beta_angle, 6900e3)
```

## 功能简介

当前功能

1. 回归圈数分析
2. SAR 天线受照分析
3. 偏置对日分析
4. 星敏布局分析
5. 光照阴影分析
6. 对日转对地过程的能源情况
7. 阳照区时间分析
8. F10.7 分析
9. 衰减率计算
10. 等效迎风面面积
11. 星敏失效时间分析
12. 飞轮惯滑时间计算
13. Python 驱动 STK
14. 星敏精测数据处理


### 回归圈数分析

![alt text](https://i.postimg.cc/rwys18wF/image.png)

### SAR 天线受照分析

![alt text](https://i.postimg.cc/8c8sMMjq/07b726e3-adbe-4110-91e6-374c52536e0c.png)

### 偏置对日分析

![alt text](https://i.postimg.cc/vHtDx1MN/beb2cc20-1e08-4764-8d2d-fa639751145d.png)

### 星敏布局分析

![alt text](https://i.postimg.cc/GpHpfqDW/image-1.png)

### 阳照区时间分析

![alt text](https://i.postimg.cc/XNFr3HP3/b2d38290-2901-4392-83c5-190958959a8d.png)

### F10.7 分析

![alt text](https://i.postimg.cc/j5nLDZdH/3cce67ab-0b2e-469f-a6e5-ee13b9b8874d.png)

### 等效迎风面面积

![alt text](https://i.postimg.cc/sDrv2PFW/977604f2-567a-492a-a0db-02f48094ef5b.png)

### 星敏失效时间分析

![alt text](https://i.postimg.cc/hv9vrvmh/589514ff-5b7a-4dbf-8748-22a92947639c.png)