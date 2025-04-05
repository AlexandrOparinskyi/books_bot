from sqlalchemy import select, func

from database.connect import get_async_session
from database.models import User


async def get_rating(user: User):
    async with get_async_session() as session:
        subquery = (
            select(
                User.id,
                func.rank().over(order_by=User.minutes.desc()).label("rank")
            ).subquery()
        )
        query = (
            select(
                User,
                subquery.c.rank
            ).join(
                subquery, User.id == subquery.c.id
            ).where(User.id == user.id)
        )

        result = await session.execute(query)
        return result.first()