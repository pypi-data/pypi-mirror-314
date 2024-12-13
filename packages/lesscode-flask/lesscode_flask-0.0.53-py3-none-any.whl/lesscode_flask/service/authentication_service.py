import json
from urllib.parse import unquote

# from lesscode_flask.model.auth_client import AuthClient
# from lesscode_flask.model.auth_permission import AuthPermission
from lesscode_flask.model.user import ApiUser, User, AnonymousUser
# from lesscode_flask.service.auth_client_service import AuthClientService
# from lesscode_flask.service.auth_permission_service import AuthPermissionService
from lesscode_flask.utils.helpers import app_config
from lesscode_flask.utils.redis.redis_helper import RedisHelper


def get_gateway_user(user_json):
    """
    网关传输信息中获取用户信息
    :param apikey:
    :return:
    """
    if user_json:
        user_dict = json.loads(user_json)
        if user_dict and isinstance(user_dict, dict):
            if type(user_dict["roleIds"]) == str:
                user_dict["roleIds"] = json.loads(user_dict["roleIds"])
            user = User(
                id=user_dict["id"],
                username=user_dict["username"],
                display_name=unquote(user_dict["display_name"]),
                phone_no=user_dict["phone_no"],
                permissions=[],
                roleIds=user_dict["roleIds"],
                client_id=user_dict["client_id"]
            )
            return user
    return AnonymousUser()

def get_token_user(token):
    """
    使用API key 获取用户信息
    :param apikey:
    :return:
    """
    token_cache_key = f"oauth2:token:{token}"
    # 优先从缓存中获取
    access_token = RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hgetall(token_cache_key)
    # {
    #     'client_id': 'eYC0lOd1XVBBPpdDntMwFcPg',
    #     'token_type': 'Bearer',
    #     'access_token': 'Rsh1zS9QVzMAefB5G7be04CefK5opjiOCBtBS8BYYi',
    #     'refresh_token': 'la5jb14acszPARoDf1KtH24JjnswSYUsjH4NbsQxOsvpO4Dl',
    #     'scope': 'profile',
    #     'issued_at': 1645614957,
    #     'expires_in': 3600,
    #     'user_id': 21,
    #     'clientId': "",
    #     "grant_type": "",
    #     "is_only_one": "1",
    #     "only_type": "pc"
    # }
    if access_token:
        user_id = access_token.get("user_id")
        clientId = access_token.get("clientId")
        user_cache_key = f"oauth2:client_user_info:client_id:{clientId}:user_id:{user_id}"
        user_dict = RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hgetall(user_cache_key)
        if user_dict:
            user = User(
                id=user_id,
                username=user_dict["username"],
                display_name=user_dict["display_name"],
                phone_no=user_dict["phone_no"],
                permissions=json.loads(user_dict["permissions"]),
                roleIds=json.loads(user_dict["roleIds"]),
                client_id=user_dict["client_id"]
            )
            return user
    return AnonymousUser()


def get_api_user(apikey):
    """
    使用API key 获取用户信息
    :param apikey:
    :return:
    """
    cache_key = f"oauth2:apikey_user_info:{apikey}"
    # 优先从缓存中获取
    user_dict = RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hgetall(cache_key)
    if user_dict:
        user = ApiUser.to_obj(user_dict)
        return user
    # else:
    #     # 库里查询
    #     authClient = AuthClientService().get_one([AuthClient.client_id == apikey])
    #     if authClient:
    #         authPermission = AuthPermissionService().get_items([AuthPermission.client_id == authClient.id])
    #         permissions = [permission.resource_id for permission in authPermission]
    #         user = ApiUser(authClient.id, authClient.client_id, authClient.client_name, permissions)
    #         RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hset(cache_key,
    #                                                                           mapping=user.to_dict(),
    #                                                                           time=authClient.token_expires_in)
    #         return user
    return AnonymousUser()
