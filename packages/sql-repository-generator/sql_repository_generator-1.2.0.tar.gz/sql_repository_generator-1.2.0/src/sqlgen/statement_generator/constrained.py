from typing import Any

from sqlalchemy import Select, ColumnElement
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.base import ExecutableOption

from sqlgen.joins import NoValidJoins, Constraint
from sqlgen.statement_generator.base import StatementGenerator
from sqlgen.exc import ConstraintNotSafe, DirectConstraintNotSafe, ForeignKeyNotSpecified, MissingKeywordArgument
from sqlgen.utils import take, index


class ConstrainedStatementGenerator[T](StatementGenerator):
    cls: type[T]
    constraints: list[Constraint]

    def __init__(self, **bound_object_ids):
        for constraint in self.constraints:
            try:
                constraint.set_bound_object_id(
                    take(lambda item: constraint.joined_column.key == item[0], bound_object_ids.items())[1]
                )
            except KeyError:
                raise MissingKeywordArgument(constraint.joined_column.key)

    def get_by(self, *args, options: list[ExecutableOption] = None,
               load_all: bool = False, property_name: str = None, **kwargs) -> Select:
        """
        Generate the select query and filter it with the bound object id

        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :param load_all: load all relationship on the model when doing the query
        :param property_name: get a property instead of the object
        :return: a sql statement with specified options, filter, ...
        """
        statement = super().get_by(*args, options=options, load_all=load_all, property_name=property_name, **kwargs)
        for i, constraint in enumerate(self.constraints):
            for join in constraint.joins:
                statement = statement.join(join)
            statement = statement.filter(constraint.joined_column == constraint.bound_object_id)
        return statement

    def validate_constraint(self, constraint: Constraint, safe_constraints: list[Constraint], **kwargs):
        """
        Validate a constraint and return a dict of properties to add to the created model
        Not Really expected to be called from outside

        :param constraint: the constraint to validate
        :param safe_constraints: a list of constraint already validated
        :param kwargs: the properties of the created model
        :raise ConstraintNotSafe: if a constraint has not been validated yet and there is at least one Constraint that
            will return the foreign_key needed to validate this constraint
            (e.g. ProjectBoundWebserverBoundRequestRepository)
        :raise BoundObjectLinkNotSafe: if a constraint has not been validated, depends on a chain of join and the
            value of the foreign_key is provided (e.g. ProjectBoundRequestRepository)
        :raise ForeignKeyNotSpecified: if a constraint has not been validated, depends on a chain of join and the
            value of the foreign_key is NOT provided.
        :return: a dict of property_name:property_value to add to the created object
        """
        if len(constraint.joins) == 0:
            return {constraint.joined_column.key: constraint.bound_object_id}
        elif constraint in safe_constraints:
            return {}
        join_column: ColumnElement = list(constraint.joins[0].property.local_columns)[0]
        if matching_constraints := list(
                filter(lambda c: c.joined_column == join_column, self.constraints)):  # false if empty
            # case we have multiple constraint and one of them maps to
            # e.g. Request -> Webserver -> Host -> Project
            # constraint Request bound to Project and constraint Request Bound to Webserver
            # Project constraint want a request.webserver_id, but it's redundant with Webserver constraint
            # that will provide the webserver_id=bound_id
            raise ConstraintNotSafe(constraint, matching_constraints)
        elif join_column.key in kwargs:
            raise DirectConstraintNotSafe(constraint, kwargs[join_column.key], constraint.joins[0].prop.entity.class_)
        else:
            raise ForeignKeyNotSpecified(join_column.key)

    def create(self, safe_constraints: list[Constraint] = None, **kwargs: Any) -> T:
        """
        generate an instance of the cls model with specified properties plus the foreign_key=bound_object_id if
        relationship is direct

        :param kwargs: the args of the created model
        :param safe_constraints: a list of constraint considered to be safe
        :raise BoundObjectLinkNotSafe: if the foreign_key value is not bound to the bound_model
            (e.g host is bound to another project)
        :raise ForeignKeyNotSpecified: if no foreign_key parameters is present to create the model and
            bound_model relation is not direct (and safe=True is not set)
        :return: an instance of the cls model with specified properties
        """
        if safe_constraints is None:
            safe_constraints = []
        model_args = {}
        for constraint in self.constraints:
            model_args.update(self.validate_constraint(constraint, safe_constraints, **kwargs))
        model_args.update(kwargs)
        return super().create(**model_args)


def build_parent_constraint(constraint: Constraint, model: type[DeclarativeBase]):
    """
    construct a constraint from an existing constraint and filter the joins to only includes those from `model` onward
    e.g. Request constraint and Webserver model. this will remove the Request.webserver join
    e.g. Request constraint and Host model. this will remove the Request.webserver and Webserver.host joins

    :param constraint: the constraint to build the new constraint from
    :param model: the model to filter the joins for
    :return: a Constraint model for given model
        (expected to be used as a ConstrainedStatementGenerator constraint for the given model)
    """
    try:
        joins_index = index(lambda j: j.class_ == model, constraint.joins)
    except KeyError:
        if model.__table__ is not constraint.joined_column.table:
            raise NoValidJoins(constraint, model, constraint.joins)
        joins_index = len(constraint.joins)
    return Constraint(
        joins=constraint.joins[joins_index:],
        joined_model=constraint.joined_model,
        joined_column=constraint.joined_column,
        _bound_object_id=constraint.bound_object_id
    )
