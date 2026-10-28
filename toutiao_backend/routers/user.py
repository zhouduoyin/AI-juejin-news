"""
用户模块路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.user import get_user_by_username, create_user, authenticate_user, update_user, change_password
from crud.user_token import upsert_user_token
from schemas.user import UserRequest, UserInfoResponse, UserAuthResponse, UserUpdateRequest, ChangePasswordRequest
from utils.response import success_response
from utils.exception import raise_conflict, raise_bad_request
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(req: UserRequest, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    existing = await get_user_by_username(db, req.username)
    if existing:
        raise_conflict("用户名已存在")

    user = await create_user(db, user_data=req)
    token = await upsert_user_token(db, user_id=user.id)

    user_info = UserInfoResponse.model_validate(user)
    auth_data = UserAuthResponse.model_validate({"token": token, "userInfo": user_info})

    return success_response(message="注册成功", data=auth_data)


@router.post("/login")
async def login(req: UserRequest, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    user = await authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = await upsert_user_token(db, user_id=user.id)

    user_info = UserInfoResponse.model_validate(user)
    auth_data = UserAuthResponse.model_validate({"token": token, "userInfo": user_info})

    return success_response(message="登录成功", data=auth_data)


@router.get("/info")
async def get_user_info(current_user=Depends(get_current_user)):
    """获取当前登录用户信息"""
    return success_response(message="查询成功", data=UserInfoResponse.model_validate(current_user))


@router.put("/update")
async def update_user_info(
    req: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """修改用户个人资料——仅更新传入的字段"""
    user = await update_user(db, user=current_user, update_data=req)
    return success_response(message="更新成功", data=UserInfoResponse.model_validate(user))


@router.put("/password")
async def change_password_endpoint(
    req: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """修改密码——需提供旧密码验证"""
    ok = await change_password(db, user=current_user, old_password=req.old_password, new_password=req.new_password)
    if not ok:
        raise_bad_request("旧密码错误")
    return success_response(message="密码修改成功")
