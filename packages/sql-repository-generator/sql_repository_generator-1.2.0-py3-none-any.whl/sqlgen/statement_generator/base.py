from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import joinedload, class_mapper
from sqlalchemy.sql.base import ExecutableOption


class StatementGenerator[T]:
    cls: type[T]

    def get_by[T](self, *args, options: list[ExecutableOption] = None,
                  load_all: bool = False, property_name: str = None, **kwargs) -> Select[T]:
        """
        Generate a SQL Select query with the associated filters/options

        :param args: filter arguments for sqlalchemy filter function
        :param options: optional options for the query (mostly ofr joinedloads)
        :param kwargs: arguments to filter the model to return
        :param load_all: load all relationship on the model when doing the query
        :param property_name: get a property instead of the object
        :return: a SQL Select statement with specified options, filter, ...
        """
        if property_name is None:
            statement = Select(self.cls)
        else:
            statement = Select(getattr(self.cls, property_name))
        if len(kwargs) > 0:
            statement = statement.filter_by(**kwargs)
        if len(args) > 0:
            statement = statement.filter(*args)
        if load_all:
            joins = map(joinedload, class_mapper(self.cls).relationships)
            if options is None:
                options = joins
            else:
                options += list(joins)
        if options:
            statement = statement.options(*options)
        return statement

    def get_by_id(self, object_id, *args, **kwargs):
        """
        generate a SQL select filtering on object_id

        :param object_id: the id of the object to filter the query for
        :param args: optional additional filters
        :param kwargs: additional parameters for get_by
        :return: a SQL Select statement with specified options, filter, ...
        """
        return self.get_by(*args, id=object_id, **kwargs)

    def create(self, **kwargs: Any) -> T:
        """
        generate an instance of the cls model with specified properties

        :param kwargs: the arguments provided by the consumer of the repository to filter, update ...
        :return: an instance of the cls model with specified properties
        """
        return self.cls(**kwargs)
