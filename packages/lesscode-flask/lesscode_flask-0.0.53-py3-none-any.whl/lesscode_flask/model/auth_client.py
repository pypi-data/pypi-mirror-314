# # coding: utf-8
# from lesscode_flask.model.base_model import BaseModel, JSONEncodedDict, DatetimeEncodedString
# from lesscode_flask.utils.helpers import generate_uuid
# from sqlalchemy import Column, DateTime, Integer, JSON, text, Text, String, Float, BigInteger
#
#
# class AuthClient(BaseModel):
#     __tablename__ = 'lc_auth_client'
#     __table_args__ = {'comment': '客户端信息表'}
#     __bind_key__ = 'auth_db'
#
#     id = Column(String(36), primary_key=True, comment='主键', insert_default=generate_uuid)
#     client_name = Column(String(255), comment='系统名称')
#     app_key = Column(String(64), nullable=False, unique=True, comment='用于唯一标识每一个客户端')
#     secret_key = Column(String(256), comment='用于指定客户端(client)的访问密匙')
#     scope = Column(String(256), comment='指定客户端申请的权限范围,可选值包括read,write,trust')
#     authorized_grant_types = Column(String(256),
#                                     comment='指定客户端支持的grant_type,可选值包括authorization_code,password,refresh_token,implicit,client_credentials, 若支持多个grant_type用逗号(,)分隔')
#     redirect_uris = Column(String(256), comment='客户端的重定向uri,可为空, 当grant_type为authorization_code或implicit时')
#     logout_redirect_uri = Column(String(255), comment='客户端登出重定向uri')
#     access_token_validity = Column(Integer,
#                                    comment='设定客户端的access_token的有效时间值(单位:秒),可选, 若不设定值则使用默认的有效时间值(60 * 60 * 12, 12小时)')
#     refresh_token_validity = Column(Integer,
#                                     comment='设定客户端的refresh_token的有效时间值(单位:秒),可选, 若不设定值则使用默认的有效时间值(60 * 60 * 24 * 30, 30天)')
#     autoapprove = Column(String(256), comment='设置用户是否自动approval操作, 默认值为 false, 可选值包括 true,false, read,write')
#     response_types = Column(String(255))
#     serial_index = Column(Float(11, True), comment='排序字段')
#     client_id_issued_at = Column(BigInteger)
#     client_secret_expires_at = Column(BigInteger)
#     token_expires_in = Column(Integer, default=3600)
#     description = Column(String(255), comment='描述')
#     is_enable = Column(Integer, nullable=False, default=1, comment='1:可用，0:禁用')
#     is_deleted = Column(Integer, nullable=False, default=0, comment='1:删除，0:未删除')
#     create_user_id = Column(String(36), nullable=False, comment='创建人id')
#     create_user_name = Column(String(36), nullable=False, comment='创建人用户名')
#     modify_user_id = Column(String(36), comment='修改人id')
#     modify_user_name = Column(String(36), comment='修改人用户名')
#     create_time = Column(DatetimeEncodedString(), server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
#     modify_time = Column(DatetimeEncodedString(), comment='修改时间')
#     service_export = Column(String(255), comment='服务出口,例如：https://chanyeos.com')
#     is_only_one = Column(Integer, default=1, comment='1：互踢，0：不互踢')
#     metadata_ = Column('metadata', JSONEncodedDict())
