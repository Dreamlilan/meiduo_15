#coding:utf8
# 用于保存celery的配置信息
# 中间人 使用 redis的14号库
broker_url = "redis://127.0.0.1/14"

# 结果保存到 redis的15号库
result_backend = "redis://127.0.0.1/15"