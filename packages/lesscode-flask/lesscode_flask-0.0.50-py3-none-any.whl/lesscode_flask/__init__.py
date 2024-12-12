__version__ = '0.0.50'

import functools
import logging
import traceback

from flask import Blueprint
from lesscode_flask.utils.decorator.cache import deal_cache


class SQ_Blueprint(Blueprint):
    def __init__(self, name: str, url_prefix: str, **kwargs):
        if not kwargs.get("import_name"):
            kwargs["import_name"] = __name__
        super().__init__(name=name, url_prefix=url_prefix, **kwargs)

    def decorator_handler(self, title: str, url: str = None, cache_enalbe: bool = False, cache_ex: int = 3600 * 10,
                          content_type: str = "json", methods=['POST']):
        options = {"methods": methods}

        def decorator(func):
            path = url if url else "/{}".format(func.__name__)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 如果开启了缓存开关
                if cache_enalbe:
                    # 尝试从缓存中获取数据
                    try:
                        data = deal_cache(func, cache_ex, "", *args, **kwargs)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        data = func(*args, **kwargs)
                    return data
                # 如果没有开启缓存，或者缓存未命中，则执行原始函数
                data = func(*args, **kwargs)
                return data

            wrapper._title = title
            wrapper._request_type = content_type
            # 添加 URL 规则到 Flask 路由
            self.add_url_rule(path, None, wrapper, **options)
            return wrapper

        return decorator

    def post_route(self, title: str, url: str = None, cache_enalbe: bool = False, cache_ex: int = 3600 * 10,
                   content_type: str = "json", methods=['POST']):
        decorator = self.decorator_handler(title, url, cache_enalbe, cache_ex, content_type, methods)
        return decorator

    def get_route(self, title: str, url: str = None, cache_enalbe: bool = False, cache_ex: int = 3600 * 10,
                  content_type: str = "json", methods=['GET']):
        decorator = self.decorator_handler(title, url, cache_enalbe, cache_ex, content_type, methods)
        return decorator