from typing import Optional, List

from sqlalchemy import or_, select, update

from app.user.models import User
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException, NotFoundException,
)
from core.utils.password_hasher import Hasher
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique().all()

    async def get_user_or_404(
            self,
            user_id: int,
    ) -> User:

        result = await session.execute(select(User).where(User.id == user_id))
        instance = result.scalar()
        if not instance:
            raise NotFoundException
        return instance

    @Transactional()
    async def create_user(
            self, email: str, password1: str, password2: str, username: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(or_(User.email == email, User.username == username))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(email=email, password=Hasher.get_password_hash(password1), username=username)
        session.add(user)
        return user

    async def update_by_id(
            self,
            id: int,
            **kwargs: dict,
    ) -> User:
        kwargs["password"] = Hasher.get_password_hash(kwargs["password"])
        query = (
            update(User)
            .where(User.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(query)
        await session.commit()
        return await self.get_user_or_404(id)

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.is_admin is False:
            return False
        return True

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()
        if not Hasher.verify_password(password, user.password):
            raise PasswordDoesNotMatchException
        if not user:
            raise UserNotFoundException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
