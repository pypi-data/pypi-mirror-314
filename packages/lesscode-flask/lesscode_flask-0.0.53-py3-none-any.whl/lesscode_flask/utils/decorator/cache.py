import copy
import datetime
import functools
import inspect
import json
import logging
import sys
import traceback

from threading import Thread

# 装饰器
from lesscode_utils.json_utils import JSONEncoder

from lesscode_flask.utils.helpers import app_config
from lesscode_flask.utils.redis.redis_helper import RedisHelper


def Cache(ex=3600 * 12, cache_key=None):
    def cache_func(func):
        # 默认key生成方法：str(item)
        @functools.wraps(func)
        def cache_wrapper(*args, **params):
            try:
                data = deal_cache(func, ex, cache_key, *args, **params)
            except Exception as e:
                logging.error(traceback.format_exc())
                data = func(*args, **params)
            return data

        return cache_wrapper

    return cache_func


def deal_cache(func, ex, cache_key, *args, **params):
    # 获取缓存查询key
    signature = inspect.signature(func)
    params = dict(sorted(params.items(), key=lambda x: x[0]))
    func_name = str(func).split(" ")[1]
    if not cache_key:
        cache_key = format_insert_key(signature, func_name, args, params)
    logging.info("redis_key:{}".format(cache_key))
    value = query_cache(cache_key, params, ex, func=func, args=args)
    if value is not False:
        data = value
    else:
        start = datetime.datetime.now()
        logging.info("[组件：{}]数据开始计算！".format(func_name))
        # copy_params = copy.deepcopy(params)
        # data = func(*args, **copy_params)
        data = func(*args, **params)
        # 插入缓存表
        insert_cache(data, ex, cache_key)
        logging.info("[组件：{}]数据缓存已刷新！用时{}".format(func_name, datetime.datetime.now() - start))

    return data


def get_redis_conn_name():
    try:
        conn_name = app_config.get("REDIS_CACHE_KEY", "redis")
    except:
        raise Exception("Redis connection is missing")
    return conn_name


def query_cache(cache_key, params=None, ex=3600 * 12, func=None, args=None, conn_name=None):
    if conn_name is None:
        conn_name = get_redis_conn_name()

    if app_config.get("CACHE_ENABLE"):
        ttl = RedisHelper(conn_name).get_connection().ttl(cache_key)

        if ttl and ex >= 900 and 0 < ttl <= ex - 900:
            Thread(target=request_interface, kwargs={
                "func": func,
                "params": params,
                "args": args,
                "ex": ex,
                "cache_key": cache_key
            }).start()
        data = RedisHelper(conn_name).sync_get(cache_key)
        if data:
            value = json.loads(data)
            return value
        else:
            logging.info("str_select_key为".format(cache_key))
            return False
    return False


def request_interface(func, params, args, ex, cache_key):
    # copy_params = copy.deepcopy(params)
    data = func(*args, **params)
    insert_cache(data, ex, cache_key)


def format_insert_key(signature, func_name, args, params):
    _args = []
    param_keys = list(signature.parameters.keys())
    if param_keys and args:
        if param_keys[0] == "self":
            _args = copy.deepcopy(args[1:])
        else:
            _args = copy.deepcopy(args)
    if isinstance(_args, tuple):
        _args = list(_args)
    for k in params:
        if k != "self":
            _args.append(json.dumps(params[k]))
    str_insert_key = "&".join([str(x) for x in _args])
    str_insert_key = app_config.get("ROUTE_PREFIX") + "#" + func_name + "#" + str_insert_key
    return str_insert_key


def insert_cache(data, ex, cache_key, conn_name=None):
    # 大于512kb不缓存
    if sys.getsizeof(data) <= 512 * 1024:
        if conn_name is None:
            conn_name = get_redis_conn_name()
        if app_config.get("CACHE_ENABLE"):
            try:
                RedisHelper(conn_name).sync_set(cache_key, JSONEncoder().encode(data), ex=ex)
            except:
                logging.error(traceback.format_exc())
