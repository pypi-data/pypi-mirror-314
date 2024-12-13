from lesscode_flask.model.base_model import BaseModel
from lesscode_flask.utils.helpers import generate_uuid
from sqlalchemy import Column, DateTime, JSON, text, String, Integer, Float


class AccessLog(BaseModel):
    __tablename__ = 'lc_access_log'
    __table_args__ = {'comment': '访问日志'}
    __bind_key__ = 'log_db'

    id = Column(String(32), primary_key=True, insert_default=generate_uuid)
    request_id = Column(String(32), comment='请求id')
    display_name = Column(String(64), comment='显示名')
    phone_no = Column(String(255), comment='手机号')
    resource_id = Column(String(32), comment='资源id)')
    resource_label = Column(String(128), comment='菜单显示名(操作)')
    url = Column(String(255), comment='访问地址')
    referrer = Column(String(255), comment='访问来源')
    client_ip = Column(String(255), comment='客户端ip')
    user_agent = Column(String(512), comment='客户端')
    params = Column(JSON)
    duration = Column(Float, comment='请求耗时')
    create_user_id = Column(String(36), nullable=False, comment='创建人id')
    create_user_name = Column(String(36), nullable=False, comment='创建人用户名')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')

