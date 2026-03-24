import time
from datetime import datetime


def get_date_separate():
    time_formate = time.localtime()
    year = time_formate.tm_year
    mon = time_formate.tm_mon
    day = time_formate.tm_mday
    return year, mon, day

def get_datetime():
    now = datetime.now()

    # 格式化时间，保留年月日时分秒
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time

def get_date():
    now = datetime.now()

    # 格式化时间，保留年月日
    formatted_time = now.strftime("%Y-%m-%d")

    return formatted_time

if __name__ == '__main__':
    print(get_datetime())