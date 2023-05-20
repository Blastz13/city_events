from typing import Optional, List, Dict

from sqlalchemy import or_, select, update, func

from app.user.models import User, UserRating
from app.user.schemas.user import LoginResponseSchema
from core.db import session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException, NotFoundException, DuplicateValueException,
)
from core.utils.password_hasher import Hasher
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
            self,
            limit: int = 10,
            prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

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

    async def create_user(
            self, email: str, password1: str, password2: str, username: str, is_admin: bool = False
    ) -> User:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(or_(User.email == email, User.username == username))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(email=email, password=Hasher.get_password_hash(password1), username=username, is_admin=is_admin)
        session.add(user)
        await session.commit()
        await session.refresh(user)
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
        if not user:
            raise UserNotFoundException
        if not Hasher.verify_password(password, user.password):
            raise PasswordDoesNotMatchException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

    async def add_user_rating(
            self,
            user_id: int,
            evaluated_id: int,
            rating: int
    ) -> UserRating:
        evaluated = await UserService().get_user_or_404(evaluated_id)
        user_rating = await session.scalars(select(UserRating).where(user_id == user_id, evaluated_id == evaluated.id))
        if user_rating.first():
            raise DuplicateValueException
        rating = UserRating(user_id=user_id, evaluated_id=evaluated.id, rating=rating)
        session.add(rating)
        await session.commit()
        await session.refresh(rating)
        return rating

    async def remove_user_rating(
            self,
            id: int,
    ) -> Dict:
        result = await session.execute(select(UserRating).where(UserRating.id == id))
        instance = result.scalar()
        if not instance:
            raise NotFoundException
        await session.delete(instance)
        await session.commit()
        return {}

    async def get_user_rating(
            self,
            user_id: int,
    ) -> int:
        result = await session.execute(
            select(User.id, func.sum(UserRating.rating))
            .where(User.id == user_id)
            .join(UserRating, UserRating.evaluated_id == User.id).group_by(User.id))
        instance = result.unique().first()
        if not instance:
            return 0
        return instance[1]
