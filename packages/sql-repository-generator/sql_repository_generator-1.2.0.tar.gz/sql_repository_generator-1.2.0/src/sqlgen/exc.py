import typing

from sqlalchemy.orm import DeclarativeBase

if typing.TYPE_CHECKING:
    from sqlgen import Constraint


class SQLGenException(Exception):
    """
    Base Exception Class for all sqlgen Exception
    """


class NoBoundModelDefined(SQLGenException):
    """
    Exception raised when trying to generate a ConstrainedRepository without constraints.
    Use DatabaseRepository instead
    """


class ConstraintNotSafe(SQLGenException):
    def __init__(self, constraint: "Constraint", matching_constraints: list["Constraint"]):
        self.constraint = constraint
        self.matching_constraints = matching_constraints


class DirectConstraintNotSafe(SQLGenException):
    def __init__(self, constraint: "Constraint", foreign_key_value, model: "type[DeclarativeBase]"):
        self.constraint = constraint
        self.foreign_key_value = foreign_key_value
        self.model = model


class BoundObjectLinkNotSafe(SQLGenException):
    def __init__(self, foreign_key_value, model: "type[DeclarativeBase]"):
        self.foreign_key_value = foreign_key_value
        self.model = model


class ForeignKeyNotSpecified(SQLGenException):
    def __init__(self, foreign_key: str):
        self.foreign_key = foreign_key

    def __str__(self):
        return ("Cannot return create args due to multiple joins between created model and "
                "bound model. To fix this error, please specify the first join relation of the "
                f"chain in the parameters ({self.foreign_key}). "
                f"e.g: repository.create({self.foreign_key}=123, your_arguments)."
                "if you have an idea on how to resolve this properly make a "
                "suggestion to the dev i'll happily listen to it.")


class ConstraintUninitialized(SQLGenException):
    def __init__(self, constraint: "Constraint"):
        self.constraint = constraint


class MissingKeywordArgument(SQLGenException):
    def __init__(self, argument_name: str):
        self.argument_name = argument_name
