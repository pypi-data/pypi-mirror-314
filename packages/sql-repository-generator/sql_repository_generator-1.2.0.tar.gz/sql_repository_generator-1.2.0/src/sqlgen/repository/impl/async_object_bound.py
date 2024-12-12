from typing import Generic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from sqlgen.repository.bases.object_bound import ObjectBoundRepository
from sqlgen.repository.impl.asynchronous import AsyncRepository
from sqlgen.exc import BoundObjectLinkNotSafe


class AsyncObjectBoundRepository[T, PK](AsyncRepository, ObjectBoundRepository):
    def __init__[PK](self, session: AsyncSession, bound_object_id: PK):
        """
        :param session: the db session used for the queries
        """
        if self.__class__ == AsyncObjectBoundRepository:
            raise ValueError("Cannot instantiate AsyncObjectBoundRepository directly")
        super().__init__(session=session, bound_object_id=bound_object_id)

    async def create(self, safe: bool = False, **properties) -> T:
        """
        override of AsyncRepository create, that will create an instance of the repository model.
        It will also set the foreign_key value automatically if bound_model is directly accessible, otherwise
        it will check for the foreign_model link to the bound_model before creating object.
        E.G we have three model: Project -> Host -> Webserver
        - if host_id is not set, an exc is raised (not if safe is set to true, but SQLAlchemy will surely if foreign_key
        is not nullable)
        - if host_id is set, a check is done for Host.project_id == self.bound_model_id (Project_id set at repo init)

        :param properties: the properties of the created model (don't include foreign_key if directly bound,
            otherwise needed)
        :param safe: a special parameter for forcing the generation even if the bound_model relation is not respected
        :raise BoundObjectLinkNotSafe: if the foreign_key value is not bound to the bound_model
            (e.g host is bound to another project)
        :raise ForeignKeyNotSpecified: if no foreign_key parameters is present to create the model and
            bound_model relation is not direct (and safe=True is not set)
        :return: the created object
        """
        try:
            return await super().create(**properties, safe=safe)
        except BoundObjectLinkNotSafe as e:
            parent_repository: AsyncObjectBoundRepository = self.get_repository_for(e.model)
            if await parent_repository.get_by_id(e.foreign_key_value) is not None:
                return await super().create(**properties, safe=True)
            else:
                raise

    def get_repository_for(self, model: DeclarativeBase) -> "AsyncObjectBoundRepository":
        """
        get an AsyncObjectBoundRepository for the given model (used internally to check for bound model relation on
        create)

        :param model: the model to generate a repository for
        :return: an AsyncObjectBoundRepository bounded to the same bound_object as this repository
        """
        type_ = type(
            f"{self.bound_model.__name__}Bound{model.__name__}Repository",
            tuple(filter(lambda x: x is not Generic, self.__class__.__mro__)),
            {
                "cls": model,
                "bound_model": self.bound_model
            })
        return type_(self.statement_executor.session, self.statement_generator.bound_object_id)
