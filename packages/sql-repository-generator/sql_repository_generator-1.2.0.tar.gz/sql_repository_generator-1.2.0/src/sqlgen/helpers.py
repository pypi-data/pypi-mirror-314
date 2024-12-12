from sqlalchemy.orm import DeclarativeBase

from sqlgen.repository.impl.async_constrained import AsyncConstrainedRepository
from sqlgen.repository.impl.async_object_bound import AsyncObjectBoundRepository
from sqlgen.repository.impl.asynchronous import AsyncRepository


def make_async_repository_class_for[T](model: type[T]) -> type[AsyncRepository[T]]:
    return type(model.__name__ + "Repository", (AsyncRepository,), {"cls": model})


def make_async_object_bound_repository_class_for[T](model: type[T],
                                                    bound_model: type[DeclarativeBase]) -> type[AsyncObjectBoundRepository]:
    return type(model.__name__ + "Repository", (AsyncObjectBoundRepository,),
                {"cls": model, "bound_model": bound_model})


def make_async_constrained_repository_class_for[T](model: type[T],
                                                   bound_model: type[DeclarativeBase],
                                                   bound_models: list[type[DeclarativeBase]]
                                                   ) -> type[AsyncConstrainedRepository[T]]:
    return type(model.__name__ + "ConstrainedRepository", (AsyncConstrainedRepository,),
                {"cls": model, "bound_model": bound_model, "bound_models": bound_models})
