# coding:utf8
"""
Celery

1. 任务
    1.任务的文件名 必须是 tasks  因为我们的Celery实例对象会自动检测任务,检测任务的文件 必须是 tasks
    2.我们的任务必须经过 Celery的实例对象的 task装饰器 装饰 才可以被celery调用执行

2. broker
3. worker



"""

from libs.yuntongxun.sms import CCP
from celery_tasks.main import app


@app.task
def send_sms_code(mobile, sms_code):
    CCP().send_template_sms(mobile, [sms_code, 5], 1)
