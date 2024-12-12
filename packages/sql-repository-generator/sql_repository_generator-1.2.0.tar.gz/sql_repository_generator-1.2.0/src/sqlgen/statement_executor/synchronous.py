from typing import Sequence

from sqlalchemy import Select, Result, ScalarResult
from sqlalchemy.orm import DeclarativeBase, Session


class SynchronousStatementExecutor[T]:
    def __init__(self, session: Session):
        """
        Initialize the SynchronousStatementExecutor.

        :param session: the db session used for the queries
        """

        self.session = session

    def execute_statement(self, statement: Select) -> Result:
        """
        Execute a SQL Select statement on the current session.

        This method takes a SQL Select statement and executes it using the current database session.

        :param statement: The SQL Select statement to execute.
        :return: The Result of the executed Select statement.
        """
        # Execute the statement using the session and return the result
        return self.session.execute(statement)

    def scalars(self, statement: Select) -> ScalarResult:
        """
        Execute a SQL Select query and return its scalars (unique or not depending on the use case).

        This method takes a SQL Select statement and executes it using the current database session.
        The result is then converted to a ScalarResult which is a special Result type that only contains
        the scalar values of the query (i.e. without the column names).

        :param statement: the SQL Select statement to execute
        :return: the scalars of the result
        """
        # Execute the statement and get the result
        result = self.execute_statement(statement)

        # If the result is not a ScalarResult, convert it to one
        if not isinstance(result, ScalarResult):
            # Uniquify the result (if needed) and convert it to a ScalarResult
            result = result.unique().scalars()

        return result

    def one[T](self, statement: Select[T]) -> T:
        """
        Execute a SQL Select statement and return only one result.

        This method executes the given SQL Select statement and returns exactly one result.
        If the query returns no results or more than one result, an exception is raised.

        :param statement: The SQL Select statement to execute.
        :return: An instance of the model(s)/property specified by the Select query.
        :raise NoResultFound: If the query returns no result.
        :raise MultipleResultsFound: If the query returns more than one result.
        """
        # Execute the statement and retrieve the scalars result.
        scalars_result = self.scalars(statement)

        # Get one result or raise an exception if no result or more than one result is found.
        return scalars_result.one()

    def one_or_none[T](self, statement: Select[T]) -> T | None:
        """
        Execute a SQL Select statement and return one result or None.

        This method executes the given SQL Select statement and returns one result if available.
        If the query returns more than one result, an exception is raised. If no result is found,
        None is returned.

        :param statement: The SQL Select statement to execute.
        :return: An instance of the model(s)/property specified by the Select query or None if not found.
        :raise MultipleResultsFound: If the query returns more than one result.
        """
        # Execute the statement and retrieve the scalar result.
        scalars_result = self.scalars(statement)

        # Get one result or None. Raise an exception if more than one result is found.
        return scalars_result.one_or_none()

    def all[T](self, statement: Select[T]) -> Sequence[T]:
        """
        Get all results for the given SQL Select.

        This method takes a SQL Select statement and executes it using the current database session.
        The result is then converted to a list of the model(s)/property specified by the Select query.

        :param statement: The SQL Select statement to execute.
        :return: A sequence of the model(s)/property specified by the Select query.
        """
        # Execute the statement and retrieve the scalars result.
        scalars_result = self.scalars(statement)

        # Get all results.
        return scalars_result.all()

    def synchronize(self):
        """
        Synchronize the current object with the database session.

        This method does not commit the changes to the database but instead
        flushes the session which means that the changes will be persisted
        to the database but the transaction will remain open. This is useful
        when you want to have the generated id of an object but don't want
        to commit the changes to the database yet.

        The object will be in the session but not yet in the database.
        A rollback of the session will remove the created object from the
        session and the database.
        """
        self.session.flush()

    def save(self):
        """
        Save the current object within the database.

        This method commits the current transaction to the database,
        persisting all changes made to the objects in the session.
        """
        # Commit the current session to persist changes
        self.session.commit()

    def restore(self):
        """
        Restore the database state to its previous state by rolling back the current transaction.

        This method is the opposite of `save()`. It will undo all changes made to the database since the last commit.

        :return: None
        """
        self.session.rollback()

    def store(self, obj: DeclarativeBase) -> None:
        """
        Add an object to the database.

        This method adds the given object to the current session, which means it will be
        persisted to the database when the session is committed.

        :param obj: The object to add to the database.
        :return: None
        """
        self.session.add(obj)
