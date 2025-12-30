from sqlalchemy import select, update
from database.models import User, Activation, Transaction, async_session
from typing import Optional, List

class DBManager:
    @staticmethod
    async def get_user(user_id: int) -> Optional[User]:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def create_user(user_id: int, username: str) -> User:
        async with async_session() as session:
            user = User(id=user_id, username=username)
            session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def update_balance(user_id: int, amount: float, tx_type: str, description: str = ""):
        async with async_session() as session:
            # Update user balance
            await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(balance=User.balance + amount)
            )
            # Record transaction
            tx = Transaction(user_id=user_id, amount=amount, type=tx_type, description=description)
            session.add(tx)
            await session.commit()

    @staticmethod
    async def add_activation(user_id: int, activation_id: str, service: str, country: int, number: str, cost: float):
        async with async_session() as session:
            activation = Activation(
                user_id=user_id,
                activation_id=activation_id,
                service_code=service,
                country_id=country,
                number=number,
                cost=cost
            )
            session.add(activation)
            await session.commit()

    @staticmethod
    async def get_active_activations(user_id: int) -> List[Activation]:
        async with async_session() as session:
            result = await session.execute(
                select(Activation).where(Activation.user_id == user_id, Activation.status == "WAITING")
            )
            return list(result.scalars().all())

    @staticmethod
    async def update_activation_status(activation_id: str, status: str, sms_code: str = None):
        async with async_session() as session:
            stmt = update(Activation).where(Activation.activation_id == activation_id).values(status=status)
            if sms_code:
                stmt = stmt.values(sms_code=sms_code)
            await session.execute(stmt)
            await session.commit()
            
    @staticmethod
    async def get_activation_by_id(activation_id: str) -> Optional[Activation]:
        async with async_session() as session:
            result = await session.execute(select(Activation).where(Activation.activation_id == activation_id))
            return result.scalar_one_or_none()
