# -*- coding: utf-8 -*-
# 解决MonkeyPatchWarning
import os

from gevent import monkey  # 导入补丁模块

monkey.patch_all()  # 创建补丁
from funcy import iteritems
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def __init__(self, app):
        self.app = app
        cpu_count = os.cpu_count()
        if cpu_count is None:
            cpu_count = 5
        options = {
            'bind': f"0.0.0.0:{app.config.get('PORT', 5002)}",  # 绑定地址和端口
            'workers': cpu_count*2+1,  # 指定 workers 数量
            'accesslog': "-",  # 输出到标准输出，取消gunicorn接管日志输出
            'worker_class': 'gevent',  # worker 运行方式
            'timeout': 300
        }
        self.options = options
        super(Application, self).__init__()
        self.application = None
        # self.logger = logging  # 自定义一直输出，如果项目中已经使用了其他的日志框架，而不想让gunicorn接管日志输出，需要将日志框架的对象指定给这里

    def load_config(self):
        config = {key: value for key, value in iteritems(self.options)
                  if key in self.cfg.settings and value is not None}
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.app
