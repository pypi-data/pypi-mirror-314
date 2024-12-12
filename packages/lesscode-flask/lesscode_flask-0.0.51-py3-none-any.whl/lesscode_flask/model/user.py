from functools import reduce

from flask_login import AnonymousUserMixin, UserMixin


class PermissionsCheckMixin:
    def has_permission(self, permission):
        return self.has_permissions((permission,))

    def has_permissions(self, permissions):
        has_permissions = reduce(
            lambda a, b: a and b,
            [permission in self.permissions for permission in permissions],
            True,
        )

        return has_permissions


class User(UserMixin, PermissionsCheckMixin):
    """
    在线用户对象类
    """

    def __init__(self, id, username: str = None, display_name: str = None, phone_no: str = None, email: str = None,
                 org_id: str = None, account_status: str = None, permissions=None, roleIds=None, client_id: str = None):
        # '账号id',
        self.id = id
        # 用户名
        self.username = username
        # '显示名',
        self.display_name = display_name
        # 手机号,
        self.phone_no = phone_no
        #  邮箱
        self.email = email
        # 组织机构id',
        self.org_id = org_id
        # '1正常（激活）；2未激活（管理员新增，首次登录需要改密码）； 3锁定（登录错误次数超限，锁定时长可配置）； 4休眠（长期未登录（字段，时长可配置），定时） 5禁用-账号失效；
        self.account_status = account_status
        # 当前用户登录成功的客户端id'
        self.client_id = client_id
        # 权限集合
        self.permissions = permissions
        # 角色集合
        self.roleIds = roleIds

    @staticmethod
    def is_api_user():
        return False

    @staticmethod
    def is_anonymous_user():
        return False

    def __str__(self):
        return (f"User(id={self.id},username={self.username},phone_no={self.phone_no},"
                f"display_name={self.display_name},email={self.email},org_id={self.org_id},"
                f"account_status={self.account_status},permissions={self.permissions})")

    def __repr__(self):
        return (f"User(id={self.id},username={self.username},phone_no={self.phone_no},"
                f"display_name={self.display_name},email={self.email},org_id={self.org_id},"
                f"account_status={self.account_status},permissions={self.permissions})")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "display_name": self.display_name,
            "phone_no": self.phone_no,
            "email": self.email if self.email else "",
            "org_id": self.org_id if self.org_id else "",
            "account_status": self.account_status,
            "permissions": ",".join(self.permissions)
        }


class AnonymousUser(User):
    """
    匿名用户
    """

    def __init__(self, permissions=None):
        super(AnonymousUser, self).__init__("AnonymousUserId", "AnonymousUser", "匿名用户", "-", "-", None, 1,
                                            permissions)

    @staticmethod
    def is_api_user():
        return False

    @staticmethod
    def is_anonymous_user():
        return True


class ApiUser(User):
    def __init__(self, id, username: str = None, display_name: str = None,
                 permissions=None):
        super(ApiUser, self).__init__(id, username, display_name, "-", "-", None, 1, permissions)

    @staticmethod
    def is_api_user():
        return True

    @staticmethod
    def to_obj(_user):
        user = ApiUser(_user.get("id"))
        for key, value in _user.items():
            if isinstance(key, bytes):
                key = key.decode('utf-8')
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            if key == "permissions":
                user.permissions = value.split(",")
            elif key == "org_id":
                user.org_id = value if value else None
            elif key == "account_status":
                user.account_status = int(value)
            else:
                setattr(user, key, value)
        return user
