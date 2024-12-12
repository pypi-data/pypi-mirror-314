from logging import getLogger

from sqlgen.exc import NoBoundModelDefined
from sqlgen.repository.bases.database_repository import DatabaseRepository
from sqlgen.statement_generator.factories import make_constrained_statement_generator_class_for

logger = getLogger(__name__)


class ConstrainedRepository(DatabaseRepository):

    @classmethod
    def get_statement_generator_factory(cls):
        bound_models = set()
        for class_ in cls.__mro__:  # check all class linked to this cls == this and parents and parents of parents ...
            if hasattr(class_, "bound_models"):
                bound_models |= set(class_.bound_models)
            if hasattr(class_, "bound_model"):
                bound_models.add(class_.bound_model)
        if len(bound_models) > 0:
            return make_constrained_statement_generator_class_for(cls.cls, list(bound_models))
        else:
            raise NoBoundModelDefined(cls.cls)
