import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib import rcParams

# 灵知 05 发射时间线绘制

# 阳照区开始
sun_start = [
    datetime(2024, 12, 15, 3,16,50),
    datetime(2024, 12, 15, 4,52,11),
    datetime(2024, 12, 15, 6,27,32),
    datetime(2024, 12, 15, 8,2,54)
]

# 阳照区结束
sun_end = [
    datetime(2024, 12, 15, 4,18,46),
    datetime(2024, 12, 15, 5,54,7),
    datetime(2024, 12, 15, 7,29,28),
    datetime(2024, 12, 15, 9,4,49)
]

# 升交点时间
anode_time = [
    datetime(2024, 12, 15, 3,53,50),
    datetime(2024, 12, 15, 5,29,20),
    datetime(2024, 12, 15, 7,4,40),
    datetime(2024, 12, 15, 8,40,0)
]

# 卫星事件点
offset = timedelta(seconds = 250) # 上电到阻尼三阶段最长时间
dates = [
    datetime(2024, 12, 15, 2, 50, 47),
    datetime(2024, 12, 15, 3, 4, 51), # C01 星箭分离
    datetime(2024, 12, 15, 3, 4, 52), # C02 星箭分离
    datetime(2024, 12, 15, 3, 5, 26), # C04 星箭分离
    datetime(2024, 12, 15, 3, 5, 56), # C03 星箭分离
    datetime(2024, 12, 15, 3, 5, 56) + offset,
    sun_start[0] + timedelta(seconds = 960),# 对日搜索+机动最长时间
]

# 过站时间线
station_time = [
    {
        "name": "新加坡+马来",
        "task": "确认星箭分离\n进阻尼三阶段\n帆板解锁",
        "time": 
        [
            datetime.fromisoformat("2024-12-15 03:04:51"),
            datetime.fromisoformat("2024-12-15 03:10:56"),
        ]
    },
    {
        "name": "阿根廷站",
        "task": "确认对日四阶段（自旋对日）\nSAR 天线展开",
        "time": 
        [
            datetime(2024, 12, 15, 3, 34, 32),
            datetime(2024, 12, 15, 3, 44, 48)
        ]
    },
    {
        "name": "中西部地面站",
        "task": "星敏接入\n转约束对日",
        "time": 
        [
            datetime(2024, 12, 15, 4, 23, 34),
            datetime(2024, 12, 15, 4, 37, 59)
        ]
    },
    {
        "name": "阿根廷站",
        "task": "星敏对准、校时、组合开启",
        "time": 
        [
            datetime(2024, 12, 15, 5, 10, 4),
            datetime(2024, 12, 15, 5, 15, 58)
        ]
    },
    {
        "name": "中西部地面站\n一星一站跟踪",
        "task": "陀螺温补，零位设置",
        "time": 
        [
            datetime(2024, 12, 15, 5, 59, 16),
            datetime(2024, 12, 15, 6, 10, 7)
        ]
    },
    {
        "name": "阿塞拜疆",
        "time": 
        [
            datetime(2024, 12, 15, 7, 35, 27),
            datetime(2024, 12, 15, 7, 45, 2)
        ]
    },
    {
        "name": "南非",
        "time": 
        [
            datetime(2024, 12, 15, 7, 56, 45),
            datetime(2024, 12, 15, 8, 5, 42)
        ]
    }
]






def plot_time_line_of_station(ax, dates: datetime, station_name: str, task: str, color="red", linewidth=5):
    # 绘制时间线
    ax.hlines(y=-0.1, xmin=min(dates), xmax=max(dates), color=color, linewidth=linewidth, zorder=3)
    # 添加站点标签
    ax.text(dates[0], -0.4, dates[0].strftime("%H:%M:%S"), ha="right", va="bottom", fontsize=10, rotation=45)
    ax.text(dates[1], -0.4, dates[1].strftime("%H:%M:%S"), ha="right", va="bottom", fontsize=10, rotation=45)
    dt = dates[1] - dates[0]
    minutes, seconds = divmod(dt.seconds, 60)
    ax.text(dates[0], -0.6,  f'{station_name}\n{minutes}m{seconds}s', ha="left", va="bottom", fontsize=10)
    ax.text(dates[0], -0.8,  f'{task}', ha="left", va="bottom", fontsize=10, color="red")





if __name__ == "__main__":
    # 全局设置字体为 SimHei
    rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

    # 创建图形
    fig, ax = plt.subplots(figsize=(20, 5))

    # 绘制卫星时间线
    ax.hlines(y=0, xmin=min(dates), xmax=max(dates), color="gray", linewidth=1.5)
    ax.scatter(dates, [0] * len(dates), color="blue", zorder=2)

    ax.text(dates[0], 0.2, 
            f"发射\n{dates[0].strftime("%H:%M:%S")}", 
            ha="left", va="bottom", fontsize=10, rotation=45)
    ax.text(dates[1], 0.2, 
            f"四星依次分离\n{dates[1].strftime("%H:%M:%S")} ~ {dates[4].strftime("%H:%M:%S")}", 
            ha="left", va="bottom", fontsize=10, rotation=45)
    ax.text(dates[5], 0.2, 
            f"进阻尼三阶段最晚时间\n{dates[5].strftime("%H:%M:%S")}", 
            ha="left", va="bottom", fontsize=10, rotation=45)
    ax.text(dates[6], 0.2, 
            f"进对日四阶段最晚时间\n{dates[6].strftime("%H:%M:%S")}", 
            ha="left", va="bottom", fontsize=10, rotation=45)

    # 绘制过站时间线
    for i in range(len(station_time)-2):
        plot_time_line_of_station(ax, station_time[i]["time"], station_time[i]["name"], station_time[i]["task"])

    # 阳照区绘制
    for i in range(2):
        ax.axvspan(sun_start[i], sun_end[i], 
                color="yellow", alpha=0.5, zorder=1, ymin=0, ymax=0.5)  # 矩形块
        ax.text(sun_start[i], -0.95, 
                f'阳照区时间\n{sun_start[i].strftime("%H:%M:%S")} ~ {sun_end[i].strftime("%H:%M:%S")}', 
                ha="left", va="bottom", fontsize=10)

    # 圈次绘制
    for i in range(2):
        ax.axvspan(anode_time[i], anode_time[i+1], 
                color="lightblue", alpha=0.5, zorder=1, ymin=0.5, ymax=1)  # 矩形块
        ax.text(anode_time[i], 0.8, 
                f'升交点时间\n{anode_time[i].strftime("%H:%M:%S")}\n圈次计数: {i+1}', 
                ha="left", va="bottom", fontsize=10)

    # 美化时间线
    ax.set_ylim(-1, 1)
    ax.set_yticks([])  # 隐藏 y 轴刻度
    ax.grid(visible=False)  # 不显示网格线
    plt.tight_layout()

    # 显示图形
    plt.savefig("timeline_highres.png", dpi=300, bbox_inches="tight")  # 设置分辨率和边框
    # plt.show()



