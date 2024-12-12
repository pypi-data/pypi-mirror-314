from typing import Sequence

from sqlalchemy import Select, Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class AsyncStatementExecutor[T]:
    def __init__(self, session: AsyncSession):
        """
        :param session: the db session used for the queries
        """
        self.session = session

    async def execute_statement(self, statement: Select) -> Result:
        """
        execute a SQL Select on the current session

        :param statement: the SQL Select statement to execute
        :return: the Result of the Select
        """
        return await self.session.execute(statement)

    async def scalars(self, statement: Select) -> ScalarResult:
        """
        Execute a SQL Select query and return its scalars
        (automatically uniquify the result for joined loads to succeed, not sure if there is some side effect)

        :param statement: the SQL Select statement to execute
        :return: the scalars of the result
        """
        return (await self.execute_statement(statement)).unique().scalars()

    async def one[T](self, statement: Select[T]) -> T:
        """
        Get only one result for the given SQL Select or raise an exception if No result of more than one

        :param statement: the SQL Select statement to execute
        :return: an instance of the model(s)/property specified by the Select query
        """
        return (await self.scalars(statement)).one()

    async def one_or_none[T](self, statement: Select[T]) -> T | None:
        """
        Get one result or None for the given SQL Select, raise an exception if more than one result are returned by the
        query

        :param statement: the SQL Select statement to execute
        :return: an instance of the model(s)/property specified by the Select query or None if not found
        """
        return (await self.scalars(statement)).one_or_none()

    async def all[T](self, statement: Select[T]) -> Sequence[T]:
        """
        Get all results for the given SQL Select.

        :param statement: the SQL Select statement to execute
        :return: a sequence of the model(s)/property specified by the Select query
        """
        return (await self.scalars(statement)).all()

    async def synchronize(self):
        """
        synchronize current object with the database session
        (don't save but flush == set id but rollback would remove the created object)
        """
        await self.session.flush()

    async def save(self):
        """
        save current object within the database
        """
        await self.session.commit()

    async def restore(self):
        """
        restore Database state on the db objects (SQL rollback)
        """
        await self.session.rollback()

    def store(self, obj: DeclarativeBase):
        """
        add an object to DB

        :param obj: the object to add to the database
        """
        self.session.add(obj)
