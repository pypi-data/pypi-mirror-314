from typing import Any

from sqlalchemy import Select, ColumnElement, Column
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.base import ExecutableOption

from sqlgen.statement_generator.base import StatementGenerator
from sqlgen.exc import BoundObjectLinkNotSafe, ForeignKeyNotSpecified


class ObjectBoundStatementGenerator[P, M](StatementGenerator):
    """
    Internal Class

    Statement Generator filtering on a bound_object_id (specified at object creation)
    using joins and primary_key (specified by the class) to filter the result
    """
    cls: type[M]
    joins: list[InstrumentedAttribute | Column]

    def __init__(self, bound_object_id: P):
        self.bound_object_id = bound_object_id

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

        for join in self.joins[:-1]:
            statement = statement.join(join)
        return statement.filter(self.joins[-1] == self.bound_object_id)

    def create(self, safe: bool = False, **kwargs: Any) -> M:
        """
        generate an instance of the cls model with specified properties plus the foreign_key=bound_object_id if
        relationship is direct

        :param kwargs: the args of the created model
        :param safe: a special parameter for forcing the generation even if the bound_model relation is not respected
        :raise BoundObjectLinkNotSafe: if the foreign_key value is not bound to the bound_model
            (e.g host is bound to another project)
        :raise ForeignKeyNotSpecified: if no foreign_key parameters is present to create the model and
            bound_model relation is not direct (and safe=True is not set)
        :return: an instance of the cls model with specified properties
        """
        model_args = {}
        if len(self.joins) == 1:
            model_args = {self.joins[-1].key: self.bound_object_id}
        elif len(self.joins) == 0:
            raise NotImplementedError("this should not happens ... how to bound to nowhere ???")
        elif safe is False:
            join_column: ColumnElement = list(self.joins[0].property.local_columns)[0]
            if join_column.key in kwargs:
                raise BoundObjectLinkNotSafe(kwargs[join_column.key], self.joins[0].prop.entity.class_)
            else:
                raise ForeignKeyNotSpecified(join_column.key)
        model_args.update(kwargs)
        return super().create(**model_args)
