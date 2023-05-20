from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from sqlalchemy import select

from app.user.models import User
from app.user.services import UserService
from core.exceptions import CustomException, UnauthorizedException, \
    ForbiddenException, NotFoundException
from core.db import session


def is_privileged_or_admin(func):
    async def wrapper(*args, **kwargs):
        if await UserService().get_user_rating(kwargs["user_id"]) >= 1000 or await UserService().is_admin(
                kwargs["user_id"]):
            return await func(*args, **kwargs)
        raise ForbiddenException

    return wrapper


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False
        return await UserService().is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception


class IsOwnerDependency(SecurityBase):
    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request, id: int):
        if request.user.id is None:
            raise UnauthorizedException

        user = await session.scalar(select(User).where(User.id == request.user.id))
        obj = await session.scalar(select(self.obj).where(self.obj.id == id))
        if not obj or not user:
            raise NotFoundException
        attr = getattr(obj, self.attr)
        if isinstance(attr, int) and not (user.id == attr) or \
                isinstance(attr, list) and user not in getattr(obj, self.attr, []):
            raise ForbiddenException
