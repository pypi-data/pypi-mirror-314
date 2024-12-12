from typing import Sequence, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.base import ExecutableOption

from sqlgen.repository.bases.database_repository import DatabaseRepository
from sqlgen.statement_executor.asynchronous import AsyncStatementExecutor


class AsyncRepository[T](DatabaseRepository):

    def __init__(self, session: AsyncSession, *args, **kwargs):
        """
        :param session: the db session used for the queries
        """
        if self.__class__ == AsyncRepository:
            raise ValueError("Cannot instantiate AsyncRepository directly")
        super().__init__(*args, **kwargs)
        self.statement_executor = AsyncStatementExecutor(session)

    async def get_by[T](self, *args, options: list[ExecutableOption] = None,
                        load_all: bool = False, property_name: str = None, **kwargs) -> T | None:
        """
        execute a sql select for the given parameters and return the object if found.

        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :param load_all: load all relationship on the model when doing the query
        :param property_name: get a property instead of the object
        :return: a SQL Select statement with specified options, filter, ...
        """
        statement = self.statement_generator.get_by(*args, options=options, load_all=load_all,
                                                    property_name=property_name, **kwargs)
        return await self.statement_executor.one_or_none(statement)

    async def take_by[T](self, *args, options: list[ExecutableOption] = None,
                         load_all: bool = False, property_name: str = None, **kwargs) -> T:
        """
        execute a sql select for the given parameters and return the object otherwise raise NoResultFound.

        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :param load_all: load all relationship on the model when doing the query
        :param property_name: get a property instead of the object
        :raise NoResultFound: if the query return no result
        :return: a SQL Select statement with specified options, filter, ...
        """
        statement = self.statement_generator.get_by(*args, options=options, load_all=load_all,
                                                    property_name=property_name, **kwargs)
        return await self.statement_executor.one(statement)

    async def get_by_id[T](self, object_id, *args, options: list[ExecutableOption] = None,
                           load_all: bool = False, property_name: str = None, **kwargs) -> T | None:
        """
        get an object by its ID and return the object if found. (additional filters can be added like get_by)

        :param object_id: the id of the object to get
        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :param load_all: load all relationship on the model when doing the query
        :param property_name: get a property instead of the object
        :return: a SQL Select statement with specified options, filter, ...
        """
        statement = self.statement_generator.get_by_id(object_id, *args, options=options, load_all=load_all,
                                                       property_name=property_name, **kwargs)
        return await self.statement_executor.one_or_none(statement)

    async def take_by_id[T](self, object_id, *args, options: list[ExecutableOption] = None,
                            load_all: bool = False, property_name: str = None, **kwargs) -> T:
        """
        get an object by its ID and return the object if found otherwise raise NoResultFound.
        (additional filters can be added like take_by)

        :param object_id: the id of the object to get
        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :param load_all: load all relationship on the model when doing the query
        :param property_name: get a property instead of the object
        :return: a SQL Select statement with specified options, filter, ...
        """
        statement = self.statement_generator.get_by_id(object_id, *args, options=options, load_all=load_all,
                                                       property_name=property_name, **kwargs)
        return await self.statement_executor.one(statement)

    async def get_all_by[T](self, *args, options: list[ExecutableOption] = None, **kwargs) -> Sequence[T]:
        """
        generic function to get all object of given model

        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :return: the list of instances of given model
        """
        statement = self.statement_generator.get_by(*args, options=options, **kwargs)
        return await self.statement_executor.all(statement)

    async def get_all[T](self) -> Sequence[T]:
        """
        generic function to get all object of given model

        :return: the list of instances of given model
        """
        return await self.get_all_by()

    async def create[T](self, **properties) -> T:
        """
        generic function to create a db object

        :param properties: the properties of the model
        :return: the created object
        """
        obj = self.statement_generator.create(**properties)
        self.statement_executor.store(obj)
        await self.statement_executor.synchronize()
        return obj

    async def update(self, obj: DeclarativeBase | Any, save: bool = False, **properties):
        """
        update a DB object and synchronize the change with the DC

        :param obj: the object to update, or it's ID
        :param save: should we commit the changes? (default to false, flush but no commit)
        :param properties: the properties to update on the object
        """
        if not isinstance(obj, DeclarativeBase):
            obj = await self.take_by_id(obj, load_all=True)
        for prop in properties:
            setattr(obj, prop, properties[prop])
        if save:
            await self.save()
        else:
            await self.synchronize()

    async def synchronize(self):
        """
        synchronize the state of the DB and the python ones
        """
        await self.statement_executor.synchronize()

    async def save(self):
        """
        Save the state of updated objects in DB (do a commit under the hood)
        """
        await self.statement_executor.save()

    async def restore(self):
        """
        restore python object state to the latest save on the DB (rollback internally)
        """
        await self.statement_executor.restore()
