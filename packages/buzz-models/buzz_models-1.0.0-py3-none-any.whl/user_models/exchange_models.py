from sqlmodel import SQLModel, Field, func
from typing import Optional
from datetime import datetime


class BoBaseUserExchangeInfos(SQLModel, table=True):
    __tablename__ = "bo_base_user_exchange_infos"

    # 主键ID
    id: int = Field(primary_key=True, index=True, description="主键ID")
    # 用户ID
    user_id: int = Field(..., description="用户ID")
    # 用户名
    user_name: str = Field(..., max_length=255, description="用户名")
    # 交易所绑定的服务器ip
    bind_ip: str = Field(..., max_length=255, description="交易所绑定的服务器ip")
    # 交易所绑定的服务器端口
    bind_port: int = Field(..., description="交易所绑定的服务器端口")
    # 交易所类型
    exchange_type: str = Field(..., max_length=255, description="交易所类型")
    # 交易所备注名称
    exchange_name: str = Field(..., max_length=255, description="交易所备注名称")
    # 交易所API密钥
    exchange_api_key: str = Field(..., max_length=255, description="交易所API密钥")
    # 交易所API密钥
    exchange_api_secret: str = Field(..., max_length=255, description="交易所API密钥")
    # 交易所API口令（如果有）
    exchange_api_passphrase: Optional[str] = Field(default=None, max_length=255, description="交易所API口令（如果有）")
    # 是否是主账号
    is_main: bool = Field(default=False, description="是否是主账号")
    # 创建日期
    create_date: datetime = Field(default_factory=datetime.now, description="创建日期")
    # 更新日期
    update_date: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now()}, description="更新日期")

    def to_dict(self):
        result = {}
        # 获取实例的所有字段
        for column in self.__table__.columns:
            value = self.__dict__.get(column.name, None)  # 直接从 __dict__ 获取属性值
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
