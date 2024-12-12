import abc

from sqlgen.statement_generator.base import StatementGenerator
from sqlgen.statement_generator.factories import make_statement_generator_class_for


class DatabaseRepository[T](abc.ABC):
    """
    Base class for DatabaseRepositories
    """
    # Metaclass provided
    statement_generator_factory: type[StatementGenerator[T]]
    # Consumer Provided
    cls: type[T]  # this must be set by the child class
    # other attr
    statement_generator: StatementGenerator[T]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "cls"):
            cls.statement_generator_factory = cls.get_statement_generator_factory()

    @classmethod
    def get_statement_generator_factory(cls):
        return make_statement_generator_class_for(cls.cls)

    def __init__(self, *args, **kwargs):
        if self.__class__ == DatabaseRepository:
            raise ValueError("Cannot instantiate DatabaseRepository directly")
        self.statement_generator: StatementGenerator[T] = self.statement_generator_factory(*args, **kwargs)
