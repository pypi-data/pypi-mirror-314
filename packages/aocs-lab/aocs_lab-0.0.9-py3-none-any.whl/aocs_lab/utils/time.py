from datetime import datetime, timedelta

def beijing_to_utc_time_str(beijing_time_str: str):
    # 将字符串转换为 datetime 对象
    beijing_time = datetime.strptime(beijing_time_str, '%Y-%m-%dT%H:%M:%S')

    # 北京时间转为 UTC 时间，减去8小时
    utc_time = beijing_time - timedelta(hours=8)

    # 转换为字符串表示
    utc_time_str = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return utc_time_str