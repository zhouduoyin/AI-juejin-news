"""
用户模块 Pydantic Schema
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    """用户注册请求体"""
    username: str
    password: str


class UserInfoBase(BaseModel):
    """用户基础信息（公开资料）"""
    model_config = ConfigDict(
        from_attributes=True,   # 允许从 ORM 对象属性取值
        populate_by_name=True,  # 允许同时使用字段名和别名
    )

    nickname: Optional[str] = Field(default=None, description="昵称")
    avatar: Optional[str] = Field(default=None, description="头像URL")
    gender: Optional[str] = Field(default=None, description="性别")
    bio: Optional[str] = Field(default=None, description="个人简介")


class UserUpdateRequest(BaseModel):
    """用户资料更新请求体——所有字段可选，只更新传入的字段"""
    nickname: Optional[str] = Field(default=None, description="昵称")
    avatar: Optional[str] = Field(default=None, description="头像URL")
    gender: Optional[str] = Field(default=None, description="性别")
    bio: Optional[str] = Field(default=None, description="个人简介")


class ChangePasswordRequest(BaseModel):
    """修改密码请求体"""
    model_config = ConfigDict(populate_by_name=True)

    old_password: str = Field(..., min_length=1, alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=1, alias="newPassword", description="新密码")


class UserInfoResponse(UserInfoBase):
    """用户信息响应（基础信息 + 标识字段）"""
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")


class UserAuthResponse(BaseModel):
    """用户认证响应（含令牌和用户信息）"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    token: str = Field(..., description="访问令牌")
    user_info: UserInfoResponse = Field(..., alias="userInfo", description="用户信息")
