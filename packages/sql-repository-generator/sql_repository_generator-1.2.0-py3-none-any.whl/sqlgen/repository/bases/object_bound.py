from sqlgen.exc import NoBoundModelDefined
from sqlgen.repository.bases.database_repository import DatabaseRepository
from sqlgen.statement_generator.factories import make_object_bound_statement_generator_class_for
from sqlgen.statement_generator.object_bound import ObjectBoundStatementGenerator


class ObjectBoundRepository[T, D](DatabaseRepository):
    bound_model: type[D]
    statement_generator: ObjectBoundStatementGenerator[T, D]

    @classmethod
    def get_statement_generator_factory(cls):
        if hasattr(cls, "bound_model"):
            return make_object_bound_statement_generator_class_for(cls.cls, cls.bound_model)
        else:
            raise NoBoundModelDefined(cls.cls)

    def __init__(self, bound_object_id, *args, **kwargs):
        if self.__class__ == ObjectBoundRepository:
            raise ValueError("Cannot instantiate ObjectBoundRepository directly")
        super().__init__(*args, bound_object_id=bound_object_id, **kwargs)
