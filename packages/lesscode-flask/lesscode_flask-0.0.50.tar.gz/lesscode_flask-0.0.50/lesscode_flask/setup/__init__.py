import importlib
import inspect

import uuid

from datetime import datetime

from logging.handlers import TimedRotatingFileHandler

import httpx
import redis
from flask import current_app
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint

from lesscode_flask.db import db
from lesscode_flask.log.access_log_handler import AccessLogHandler
from lesscode_flask.model.user import AnonymousUser, User
from lesscode_flask.service.authentication_service import get_token_user, get_api_user, get_gateway_user
from lesscode_flask.utils.swagger.swagger_template import split_doc
from lesscode_flask.utils.swagger.swagger_util import generate_openapi_spec, replace_symbol, get_params_type, get_sample_data


def setup_logging(app):
    """
    初始化日志配置
    1. 日志等级
        DEBUG : 10
        INFO：20
        WARN：30
        ERROR：40
        CRITICAL：50
    :return:
    """
    import logging
    import sys
    # 日志配置
    # 日志级别
    LOG_LEVEL = app.config.get("LESSCODE_LOG_LEVEL", "DEBUG")
    # 日志格式
    LOG_FORMAT = app.config.get("LESSCODE_LOG_FORMAT",
                                '[%(asctime)s] [%(levelname)s] [%(name)s:%(module)s:%(lineno)d] [%(message)s]')
    # 输出管道
    LOG_STDOUT = app.config.get("LESSCODE_LOG_STDOUT", True)
    # 日志文件备份数量
    LOG_FILE_BACKUPCOUNT = app.config.get("LESSCODE_LOG_FILE_BACKUPCOUNT", 7)
    # 日志文件分割周期
    LOG_FILE_WHEN = app.config.get("LESSCODE_LOG_LOG_FILE_WHEN", "D")
    # 日志文件存储路径
    LOG_FILE_PATH = app.config.get("LESSCODE_LOG_FILE_PATH", 'logs/lesscode.log')
    formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(LOG_LEVEL.upper())
    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout if LOG_STDOUT else sys.stderr)
    console_handler.setFormatter(formatter)
    file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE_PATH, when=LOG_FILE_WHEN,
                                                             backupCount=LOG_FILE_BACKUPCOUNT)

    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)
    logging.addLevelName(100, 'ACCESS')

    LESSCODE_ACCESS_LOG_DB = app.config.get("LESSCODE_ACCESS_LOG_DB", 0)
    if LESSCODE_ACCESS_LOG_DB == 1:
        access_log_handler = AccessLogHandler()
        access_log_handler.level = 100
        logging.getLogger().addHandler(access_log_handler)


def setup_blueprint(app, path=None, pkg_name="handlers"):
    import os
    from flask import Blueprint
    import inspect
    """
    动态注册Handler模块
    遍历项目指定包内的Handler，将包内module引入。
    :param path: 项目内Handler的文件路径
    :param pkg_name: 引入模块前缀
    """
    if path is None:
        # 项目内Handler的文件路径，使用当前工作目录作为根
        path = os.path.join(os.getcwd(), pkg_name)
    # 首先获取当前目录所有文件及文件夹
    dynamic_handler_names = os.listdir(path)
    for handler_name in dynamic_handler_names:
        # 利用os.path.join()方法获取完整路径
        full_file = os.path.join(path, handler_name)
        # 循环判断每个元素是文件夹还是文件
        if os.path.isdir(full_file) and handler_name != "__pycache__":
            # 文件夹递归遍历
            setup_blueprint(app, os.path.join(path, handler_name), ".".join([pkg_name, handler_name]))
        elif os.path.isfile(full_file) and handler_name.lower().endswith("handler.py"):
            # 文件，并且为handler结尾，认为是请求处理器，完成动态装载
            module_path = "{}.{}".format(pkg_name, handler_name.replace(".py", ""))
            module = importlib.import_module(module_path)  # __import__(module_path)
            for name, obj in inspect.getmembers(module):
                # 找到Blueprint 的属性进行注册
                if isinstance(obj, Blueprint):
                    # 如果有配置统一前缀则作为蓝图路径的统一前缀
                    if hasattr(obj, "url_prefix") and app.config.get("ROUTE_PREFIX", ""):
                        obj.url_prefix = f'{app.config.get("ROUTE_PREFIX")}{obj.url_prefix}'
                    # 加载完成后 注册蓝图到应用
                    app.register_blueprint(obj)


def setup_query_runner():
    """
    注入数据查询执行器
    :return:
    """
    from redash.query_runner import import_query_runners
    from redash import settings as redash_settings
    import_query_runners(redash_settings.QUERY_RUNNERS)


def setup_sql_alchemy(app):
    """
    配置SQLAlchemy
    :param app:
    :return:
    """
    if app.config.get("SQLALCHEMY_BINDS"):  # 确保配置SQLALCHEMY_BINDS才注册SQLAlchemy
        db.init_app(app)


def setup_login_manager(app):
    login_manager = LoginManager(app)
    setattr(app, "login_manager", login_manager)

    @login_manager.request_loader
    def request_loader(request):
        # 使用token访问的用户
        if app.config.get("GATEWAY_USER_ENABLE"):
            user_json = request.headers.get("User", "")
            if user_json:
                return get_gateway_user(user_json)
        # 使用token访问的用户
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            return get_token_user(token)
        apikey = request.headers.get("API-Key")
        if apikey:
            # 使用AK访问的接口用户
            return get_api_user(apikey)
        # 无任何用户信息返回 匿名用户
        return AnonymousUser()


def setup_swagger(app):
    """
    配置Swagger
    :param app:
    :return:
    """
    SWAGGER_URL = app.config.get("SWAGGER_URL", "")  # 访问 Swagger UI 的 URL
    # API_URL = 'http://127.0.0.1:5001/static/swagger.json'  # Swagger 规范的路径（本地 JSON 文件）
    API_URL = app.config.get("SWAGGER_API_URL", "")  # 接口
    # 创建 Swagger UI 蓝图
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI 访问路径
        app.config.get("OUTSIDE_SCREEN_IP") + API_URL,  # Swagger 文件路径
        config={  # Swagger UI 配置参数
            'app_name': "Flask-Swagger-UI 示例"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route(API_URL, methods=['GET'])
    def swagger_spec():
        from lesscode_flask import __version__
        swag = generate_openapi_spec(app)
        swag['info']['title'] = app.config.get("SWAGGER_NAME", "")
        swag['info']['description'] = app.config.get("SWAGGER_DESCRIPTION", "")
        swag['info']['version'] = app.config.get("SWAGGER_VERSION", __version__)
        return swag


def setup_redis(app):
    redis_conn_list = app.config.get("DATA_SOURCE", [])

    for r in redis_conn_list:
        if r.get("type") == "redis":
            conn = redis.Redis(host=r.get("host"), port=r.get("port"), db=r.get("db"), password=r.get("password"),
                               decode_responses=True)
            if not hasattr(current_app, "redis_conn_dict"):
                current_app.redis_conn_dict = {}
            if getattr(current_app, "redis_conn_dict").get(r.get("conn_name")):
                raise Exception("Connection {} is repetitive".format(r.get("conn_name")))
            else:
                redis_conn_dict = getattr(current_app, "redis_conn_dict")
                redis_conn_dict.update({
                    r.get("conn_name"): conn
                })
                setattr(current_app, "redis_conn_dict", redis_conn_dict)


def setup_resource_register(app):
    def extract_get_parameters(rule, view_func, param_desc_dict=None):
        if param_desc_dict is None:
            param_desc_dict = {}
        parameters = []
        # 提取查询参数和表单参数
        sig = inspect.signature(view_func)
        for arg, param in sig.parameters.items():
            if arg not in rule.arguments:
                param_info = {
                    "name": arg,
                    "in": "query",
                    "type": "string",
                    "description": param_desc_dict[arg] if param_desc_dict.get(arg) else f"Path parameter {arg}",
                }
                if param.default is inspect.Parameter.empty:
                    param_info["required"] = True
                    param_info["example"] = get_sample_data(param.annotation.__name__)
                else:
                    param_info["required"] = False
                    param_info["default"] = param.default
                    param_info["example"] = param.default
                parameters.append(param_info)
        return parameters

    def extract_post_body(view_func, not_allow_list=None, param_desc_dict=None):
        if param_desc_dict is None:
            param_desc_dict = {}
        param_list = []
        # 提取查询参数和表单参数
        sig = inspect.signature(view_func)

        required = []
        for arg, param in sig.parameters.items():
            param_info = {
                "name": param.name,
                "type": get_params_type(param),
                "description": param_desc_dict[arg] if param_desc_dict.get(arg) else f"Path parameter {arg}",
                "in": "body"
            }
            # 如果默认值是空，则是必填参数
            if param.default is inspect.Parameter.empty:
                if (not_allow_list and arg not in not_allow_list) or not not_allow_list:
                    required.append(arg)

                param_info["example"] = get_sample_data(param.annotation.__name__)
                param_info["required"] = True
            else:
                param_info["default"] = param.default
                param_info["required"] = False
                if param.default is not None:
                    param_info["example"] = param.default
                else:
                    param_info["example"] = get_sample_data(param.annotation.__name__)
            # 如果参数类型是FileStorage 则swagger中format为binary 显示导入文件
            if param.annotation.__name__ == "FileStorage":
                param_info["format"] = "binary"
            if (not_allow_list and arg not in not_allow_list) or not not_allow_list:
                param_list.append(param_info)

        return param_list

    def extract_path_parameters(rule, param_desc_dict=None):
        if param_desc_dict is None:
            param_desc_dict = {}
        param_list = []
        # 提取路径参数
        for arg in rule.arguments:
            param_list.append({
                "name": arg,
                "in": "path",
                "required": True,
                "description": param_desc_dict[arg] if param_desc_dict.get(arg) else f"Path parameter {arg}",
                "example": "",
                "default": "",
                "type": "string"
            })
        return param_list

    def package_resource(label, symbol, access, type, method="", url="", description="", param_list: list = None):
        """

        :param label: 展示中文名称
        :param symbol: 标识符号
        :param access: 访问权限2：需要权限 1：需要登录 0：游客
        :param type:菜单类型 0：功能分组  1：页面 2：接口 3：前端控件 4：接口池接口
        :param method:post、get
        :param url:接口地址
        :param description:接口描述
        :return:
        """
        resource = {
            "client_id": current_app.config.get("CLIENT_ID", ""),
            "label": label,
            "symbol": symbol,
            "access": access,
            "type": type,
            "method": method,
            "serial_index": 0,
            "url": url,
            "description": description,
            "is_enable": 1,
            "is_deleted": 0,
            "create_user_id": "-",
            "create_user_name": "-",
            "create_time": str(datetime.now())
        }
        return resource

    if current_app.config.get("REGISTER_ENABLE", False) and current_app.config.get("REGISTER_SERVER"):
        resource_list = []
        url_rules_dict = {}
        for blueprint_name, blueprint in app.blueprints.items():
            if blueprint.url_prefix not in ["/swagger-ui"]:
                url_rules_dict[blueprint_name] = []
                # 遍历全局 URL 规则
                for rule in app.url_map.iter_rules():
                    # 筛选出属于当前蓝图的规则
                    if rule.endpoint.startswith(f"{blueprint_name}."):
                        url_rules_dict[blueprint_name].append(rule)

        for parent_resource in url_rules_dict:
            symbol = uuid.uuid1().hex
            resource = package_resource(label=parent_resource, symbol=symbol, access=0, type=0)
            resource["children"] = []

            for child_resource in url_rules_dict[parent_resource]:
                view_func = app.view_functions[child_resource.endpoint]
                if view_func.__doc__:

                    description = view_func.__doc__.strip().splitlines()[
                        0] if view_func.__doc__.strip().splitlines() else None
                else:
                    description = ""

                method = list(child_resource.methods - {'HEAD', 'OPTIONS'})[0]
                inter_desc, param_desc_dict, return_desc = split_doc(child_resource, app)
                if method == "POST":
                    path = replace_symbol(child_resource.rule)
                    if "{" in path and "}" in path:
                        path_params = extract_path_parameters(child_resource, param_desc_dict)
                        param_list = extract_post_body(view_func,
                                                       not_allow_list=[param["name"] for param in path_params],
                                                       param_desc_dict=param_desc_dict)
                        param_list = param_list + param_list
                    else:
                        param_list = extract_post_body(view_func, param_desc_dict=param_desc_dict)
                elif method == "GET":
                    param_list = extract_path_parameters(child_resource, param_desc_dict) + extract_get_parameters(
                        child_resource, view_func, param_desc_dict)
                else:
                    param_list = []
                resource["children"].append(
                    package_resource(label="", symbol=child_resource.rule, access=1, type=2, url=child_resource.rule,
                                     description=description, param_list=param_list))
            resource_list.append(resource)
        with httpx.Client(**{"timeout": None}) as session:
            try:
                res = session.request("post", url=current_app.config.get(
                    "REGISTER_SERVER") + "/icp/authResource/resource_register", json={
                    "resource_list": resource_list
                })
                return res
            except Exception as e:
                raise e
