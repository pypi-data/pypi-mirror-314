from sqlalchemy.orm import DeclarativeBase

from sqlgen.joins import resolve_model_joins, Constraint
from sqlgen.statement_generator.base import StatementGenerator
from sqlgen.statement_generator.constrained import ConstrainedStatementGenerator
from sqlgen.statement_generator.object_bound import ObjectBoundStatementGenerator


def make_statement_generator_class_for[T](cls: type[T]) -> type[StatementGenerator[T]]:
    """
    Generate a StatementGenerator class for the given model

    :param cls: the model to use for the StatementGenerator class
    :return: a child class of StatementGenerator with `cls` set
    """
    return type(f"{cls.__name__}StatementGenerator", (StatementGenerator,), {"cls": cls})


def make_object_bound_statement_generator_class_for[S, D](
        cls: type[S],
        model_to_join: type[D]
) -> type[ObjectBoundStatementGenerator[S, D]]:
    """
    Generate a ObjectBoundStatementGenerator class for the given model `cls` with filters for bounding to
    `model_to_join`

    bound model == query will be filtered to only match objects that have a relation with the instance of
    the model specified at class init (this function generate a class but does not instantiate it)

    :param cls: the model to use for the return of ObjectBoundStatementGenerator
    :param model_to_join: the model to bound for the requests
    :return: a child class of ObjectBoundStatementGenerator with `cls` set and joins to `model_to_join`
    """
    constraint: Constraint = resolve_model_joins(cls, model_to_join)
    return type(f"{model_to_join.__name__}Bound{cls.__name__}StatementGenerator", (ObjectBoundStatementGenerator,),
                {"cls": cls, "joins": constraint.joins + [constraint.joined_column]})


def make_constrained_statement_generator_class_for[T](
        cls: type[T],
        models_to_join: list[type[DeclarativeBase]]
) -> type[ConstrainedStatementGenerator[T]]:
    """
    Generate a ConstrainedStatementGenerator class for the given model `cls` with filters for bounding to the
    `models_to_join`

    bound model == query will be filtered to only match objects that have a relation with the instance of
    the model specified at class init (this function generate a class but does not instantiate it)

    :param cls: the model to use for the return of ConstrainedStatementGenerator
    :param models_to_join: the models to bound for the sql queries
    :return: a child class of ConstrainedStatementGenerator with `cls` and `constraints` set
    """
    constraints = [resolve_model_joins(cls, model_to_join) for model_to_join in models_to_join]
    generated_cls_name = "".join(f"{model_to_join.__name__}Bound" for model_to_join in models_to_join)
    generated_cls_name += f"{cls.__name__}StatementGenerator"
    return type(generated_cls_name, (ConstrainedStatementGenerator,), {"cls": cls, "constraints": constraints})
