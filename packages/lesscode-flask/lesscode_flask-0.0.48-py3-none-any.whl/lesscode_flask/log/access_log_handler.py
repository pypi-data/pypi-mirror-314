from logging import Handler

from flask import request, copy_current_request_context
from flask_login import current_user
import threading
from lesscode_flask.model.access_log import AccessLog

from lesscode_flask.service.access_log_service import AccessLogService
from lesscode_flask.utils.helpers import app_config
from lesscode_flask.utils.redis.redis_helper import RedisHelper


class AccessLogHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def emit(self, record):
        # 客户端IP
        referrer = request.referrer
        client_ip = request.remote_addr
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        params = {}
        args = request.args
        if args:
            params["args"] = args
        form = request.form
        if form:
            params["form"] = form
        if request.mimetype == 'application/json' and request.json is not None:
            params["json"] = request.json

        request_id = request.headers.get('Request-Id')
        if request_id is None:
            request_id = request.request_id
        user_agent_string = request.headers.get('user-agent')
        url = request.path
        url_info_key = f"upms:url_info:{url}"

        resource_id = "-"
        resource_label = "-"
        url_info = RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hgetall(url_info_key)
        if url_info:
            resource_id = url_info.get("id", "-")
            resource_label = url_info.get("label", "-")

        access_log = AccessLog(request_id=request_id, display_name=current_user.display_name,
                               phone_no=current_user.phone_no,
                               resource_id=resource_id,
                               resource_label=resource_label, url=url, referrer=referrer, client_ip=client_ip,
                               user_agent=user_agent_string,
                               params=params, duration=record.message)

        @copy_current_request_context
        def thread_function(access_log):
            # 在这个函数内部，应用上下文将会被正确传递
            AccessLogService.add_item(access_log)

        # 创建并启动线程
        thread = threading.Thread(target=thread_function, args=[access_log])
        thread.start()
