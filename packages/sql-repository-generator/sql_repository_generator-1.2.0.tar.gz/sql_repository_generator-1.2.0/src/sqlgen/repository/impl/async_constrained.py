from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from sqlgen.repository.bases.constrained import ConstrainedRepository
from sqlgen.repository.impl.asynchronous import AsyncRepository
from sqlgen.statement_generator.constrained import ConstrainedStatementGenerator, build_parent_constraint
from sqlgen.joins import Constraint
from sqlgen.exc import ConstraintNotSafe, DirectConstraintNotSafe


class AsyncConstrainedRepository[T](AsyncRepository, ConstrainedRepository):
    bound_model: type[DeclarativeBase]
    bound_models: list[type[DeclarativeBase]]
    statement_generator: ConstrainedStatementGenerator[T]

    def __init__(self, session: AsyncSession, **bound_object_ids):
        """
        :param session: the db session used for the queries
        """
        if self.__class__ == AsyncConstrainedRepository:
            raise ValueError("Cannot instantiate AsyncConstrainedRepository directly")
        super().__init__(session, **bound_object_ids)

    async def create(self, *, safe_constraints: list[Constraint] = None, **properties) -> T:
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
        :param safe_constraints: a list of constraint that are considered safe
        :raise BoundObjectLinkNotSafe: if the foreign_key value is not bound to the bound_model
            (e.g host is bound to another project)
        :raise ConstraintNotSafe: if a non-direct constraint is not safe.
            e.g. Request with Bound on Webserver and Project but webserver_bound is not related to the Project_bound
            ( Webserver.host.project == 2 but bound_project == 1 )
        :raise ForeignKeyNotSpecified: if no foreign_key parameters are present to create the model,
            bound_model relation is not direct and no other constraint in the chain are set with value
        :return: the created object
        """
        if safe_constraints is None:
            safe_constraints = []
        try:
            return await super().create(**properties, safe_constraints=safe_constraints)
        except DirectConstraintNotSafe as e:
            return await self.handle_direct_constraint_not_safe(e.model, e.foreign_key_value, e.constraint,
                                                                safe_constraints=safe_constraints,
                                                                **properties)
        except ConstraintNotSafe as e:
            return await self.handle_constraint_not_safe(e.constraint, e.matching_constraints,
                                                         safe_constraints=safe_constraints,
                                                         **properties)

    async def handle_direct_constraint_not_safe(self, model: type[DeclarativeBase], foreign_key_value: Any,
                                                constraint: Constraint,
                                                safe_constraints: list[Constraint], **properties):
        """
        exception handler for BoundObjectLinkNotSafe.
        check that the link to bound_model is respected using model instance identified bu foreign_key value

        :param model: the model to validate that its instance respect the bound object links
        :param foreign_key_value: the id of the model instance to validate
        :param constraint: the constraint triggering this exception (to add to safe_constraint if safe)
        :param safe_constraints: a list of constraints that are considered as safe and won't be rechecked
        :param properties: the properties of the object to create
        :return: the created object
        """
        parent_repository: AsyncConstrainedRepository = self.get_repository_for(model)
        if await parent_repository.get_by_id(foreign_key_value) is not None:
            return await self.create(**properties, safe_constraints=safe_constraints + [constraint])
        else:
            raise

    async def handle_constraint_not_safe(self, constraint: Constraint, constraints_to_test: list[Constraint],
                                         safe_constraints: list[Constraint], **properties):
        """
        exception handler for ConstraintNotSafe.
        check that all the "constraints to test" validate the given "constraint".

        :param constraint: the constraint to validate
        :param constraints_to_test: the list of constraints to validate to ensure this constraint is safe
        :param safe_constraints: a list of constraints that are considered as safe and won't be rechecked
        :param properties: the properties of the object to create
        :return: the created object
        """
        for constraint_to_test in constraints_to_test:
            parent_repository: AsyncConstrainedRepository = self.get_repository_for(constraint_to_test.joined_model)
            if await parent_repository.get_by_id(constraint_to_test.bound_object_id) is None:
                raise
        return await self.create(**properties, safe_constraints=safe_constraints + [constraint])

    def get_repository_for(self, model: type[DeclarativeBase]) -> "AsyncConstrainedRepository":
        """
        get an AsyncObjectBoundRepository for the given model (used internally to check for bound model relation on
        create)

        :param model: the model to generate a repository for
        :return: an AsyncObjectBoundRepository bounded to the same bound_object as this repository
        """
        constraints = self.get_constraints_for(model)
        type_ = type(
            f"{self.bound_model.__name__}Bound{model.__name__}Repository",
            (AsyncConstrainedRepository,),
            {
                "cls": model,
                "bound_models": [constraint.joined_model for constraint in constraints]
            })
        return type_(self.statement_executor.session,
                     **{constraint.joined_column.key: constraint.bound_object_id for constraint in constraints})

    def get_constraints_for(self, model: type[DeclarativeBase]) -> list[Constraint]:
        """
        build the constraints concerning the given model (== exclude those bounding to the model)

        :param model: the model to build constraint for
        :return: a list of constraint based on those present on this repository without those linked to the model
        """
        return [build_parent_constraint(constraint, model) for constraint in self.statement_generator.constraints if
                constraint.joined_model != model]
