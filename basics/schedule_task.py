"""
用schedule运行定时任务

1. 定义任务函数
2. 决定定期运行的时间
3. 运行所有待定任务
"""

import logging
import time

import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def job(num=0):
    logging.info(f"execute job({num})")


# 每隔5秒钟运行一次任务，可设定多个任务
schedule.every(5).seconds.do(job, num=0)
schedule.every(5).seconds.do(job, num=1)

# 每隔1分钟运行一次任务
# schedule.every().minute.do(job)

# 每隔1分钟过15秒运行一次任务
# schedule.every().minute.at(":15").do(job)

# 每隔1小时过15分钟运行一次任务
# schedule.every().hour.at(":15").do(job)

# 每天凌晨00:10:00运行一次任务
# schedule.every().day.at("00:10:00").do(job)

# 每周三下午3点运行一次任务
# schedule.every().wednesday.at("15:00:00").do(job)


while True:
    schedule.run_pending()  # 运行所有设定任务
    time.sleep(1)