# # coding: utf-8
# from lesscode_flask.model.base_model import BaseModel
# from lesscode_flask.utils.helpers import generate_uuid
# from sqlalchemy import Column, DateTime, Integer, JSON, text, Text, String, Float, BigInteger
#
#
# class AuthPermission(BaseModel):
#     __tablename__ = 'lc_auth_permissions'
#     __table_args__ = {'comment': '权限表（用户、角色、应用-资源关系表）'}
#     __bind_key__ = 'auth_db'
#
#     id = Column(String(36), primary_key=True, insert_default=generate_uuid)
#     user_id = Column(String(36), comment='用户id')
#     role_id = Column(String(36), comment='角色id')
#     client_id = Column(String(36), comment='客户端id')
#     type = Column(Integer, comment='0:角色资源，1:客户端资源，2:用户资源')
#     resource_id = Column(String(36), comment='资源id')
#     expires_at = Column(Integer, comment='资源失效时间')
#     validator = Column(JSON, comment='验证数据')
#     create_user_id = Column(String(36), nullable=False, comment='创建人id')
#     create_user_name = Column(String(36), nullable=False, comment='创建人用户名')
#     modify_user_id = Column(String(36), comment='修改人id')
#     modify_user_name = Column(String(36), comment='修改人用户名')
#     create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
#     modify_time = Column(DateTime, comment='修改时间')
