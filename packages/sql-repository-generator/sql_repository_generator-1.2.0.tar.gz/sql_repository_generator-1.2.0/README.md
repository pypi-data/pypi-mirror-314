![logo](LOGO.jpg)

# SQLRepositoryGenerator

![pipeline](https://gitlab.com/Tagashy/sqlgen/badges/master/pipeline.svg)
![coverage](https://gitlab.com/Tagashy/sqlgen/badges/master/coverage.svg)
![release](https://gitlab.com/Tagashy/sqlgen/-/badges/release.svg)

## Description

SQLRepositoryGenerator is a wrapper above [SQLAlchemy](https://www.sqlalchemy.org/) to allow the generation of
Repository class from
SQLAlchemy models.

This way one can concentrate the repository code to non standard SQL query and have the common one auto generated.

## Installation

```bash
pip install sql-repository-generator
```

## Usage

two scenario are considered regarding the usage of the library:

- The most common one as base class for your repository to inherit
- A functional approach though function that generate repository class.

### Hierarchical

to use SQLRepositoryGenerator, it is needed to make a child class of one of the Repository base class

#### AsyncRepository

AsyncRepository is a base class that just hide the internal of query making for a given model

##### Example

```python
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from sqlgen import AsyncRepository

UUID_PK = Annotated[UUID, mapped_column(primary_key=True)]
PROJECT_FK = Annotated[UUID, mapped_column(ForeignKey("project.id"))]


class Base(DeclarativeBase):
    id: Mapped[UUID_PK] = mapped_column(default=uuid4)


class Host(Base):
    __tablename__ = "host"
    name: Mapped[str]
    project_id: Mapped[PROJECT_FK]
    project: Mapped["Project"] = relationship(back_populates="hosts")


class HostRepository(AsyncRepository):
    cls = Host  # Model to query


async def main(session: AsyncSession):
    repository = HostRepository(session)
    host = await repository.create(name="toto")
    hosts = await repository.get_all()

```

#### AsyncConstrainedRepository (Deprecated)

AsyncConstrainedRepository handle more complex case where some constraint are needed to be fulfilled for every
interaction with the database.
Those constraints are defined on the child class using `bound_model` and `bound_models` class variable.
if they are set every query will filter using the link between `cls` and each `bound_model` to ensure they fulfill the
constraint.

In other word, considering we have a Database with a Customer, Project, Host and Request table.
and the following class

```python
class HostRepository(AsyncConstrainedRepository):
    cls = Host
    bound_model = Customer
```

every query will be automatically added a filter `Host.project.customer_id==customer_id`, this is also true for objects
creation however the logic is a bit different, instead of adding a filter to the select query, when creating an object,
every constraint will be validated though a dedicated query, raising an exception if failing, before adding the object.

##### Example

```python
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from sqlgen import AsyncConstrainedRepository

UUID_PK = Annotated[UUID, mapped_column(primary_key=True)]
HOST_FK = Annotated[UUID, mapped_column(ForeignKey("host.id"))]
PROJECT_FK = Annotated[UUID, mapped_column(ForeignKey("project.id"))]
WEBSERVER_FK = Annotated[UUID, mapped_column(ForeignKey("webserver.id"))]


class Base(DeclarativeBase):
    id: Mapped[UUID_PK] = mapped_column(default=uuid4)


class Request(Base):
    webserver_id: Mapped[WEBSERVER_FK]
    webserver: Mapped["Webserver"] = relationship(back_populates="requests")


class Webserver(Base):
    __tablename__ = "webserver"

    host_id: Mapped[HOST_FK]
    host: Mapped["Host"] = relationship(back_populates="webservers")
    requests: Mapped[list["Request"]] = relationship(back_populates="webserver", cascade="all, delete-orphan")


class Host(Base):
    __tablename__ = "host"
    name: Mapped[str]
    project_id: Mapped[PROJECT_FK]
    project: Mapped["Project"] = relationship(back_populates="hosts")
    webservers: Mapped[list["Webserver"]] = relationship(back_populates="host", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "project"
    hosts: Mapped[list["Host"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class ProjectBoundRepository(AsyncConstrainedRepository):
    bound_model = Project


class WebserverBoundRepository(AsyncConstrainedRepository):
    bound_model = Webserver


class RequestRepository(ProjectBoundRepository, WebserverBoundRepository):
    cls = Request


async def main(session: AsyncSession):
    project_id = uuid4()
    webserver_id = uuid4()
    repository = RequestRepository(session, project_id=project_id, webserver_id=webserver_id)
    request = await repository.create(name="toto")  # check that webserver_id is bound to project_id
    requests = await repository.get_all()  # filtered by Request.webserver.host.project.id == project_id

```

#### AsyncObjectBoundRepository (Deprecated)

AsyncObjectBoundRepository allows to have a repository filtered for a specific object_id:

##### Example

```python
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from sqlgen import AsyncObjectBoundRepository

UUID_PK = Annotated[UUID, mapped_column(primary_key=True)]
HOST_FK = Annotated[UUID, mapped_column(ForeignKey("host.id"))]
PROJECT_FK = Annotated[UUID, mapped_column(ForeignKey("project.id"))]


class Base(DeclarativeBase):
    id: Mapped[UUID_PK] = mapped_column(default=uuid4)


class Webserver(Base):
    __tablename__ = "webserver"

    host_id: Mapped[HOST_FK]
    host: Mapped["Host"] = relationship(back_populates="webservers")


class Host(Base):
    __tablename__ = "host"
    name: Mapped[str]
    project_id: Mapped[PROJECT_FK]
    project: Mapped["Project"] = relationship(back_populates="hosts")
    webservers: Mapped[list["Webserver"]] = relationship(back_populates="host", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "project"
    hosts: Mapped[list["Host"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class WebserverRepository(AsyncObjectBoundRepository):
    cls = Webserver  # Model to query
    bound_model = Project


async def main(session: AsyncSession):
    project_id = uuid4()
    repository = WebserverRepository(session, project_id)
    host = await repository.create(name="toto")  # Not Filtered
    hosts = await repository.get_all()  # filtered by Webserver.host.project.id == project_id

```

### Functional

three helper function are defined to generate repository classes:

- make_async_repository_class_for
- make_async_object_bound_repository_class_for
- make_async_constrained_repository_class_for

each of those function return an appropriate repository class for the parameters given to them.
Here is an example of their usage:

```python
# Async Repository
from sqlgen import make_async_repository_class_for, make_async_constrained_repository_class_for,

make_async_object_bound_repository_class_for

repository_class = make_async_repository_class_for(VulnerabilityClass)
repository = repository_class(session)
assert isinstance(repository, AsyncRepository)
# Object Bound Repository
repository_class = make_async_object_bound_repository_class_for(VulnerabilityClass, Project)
repository = repository_class(session, project_id)
assert isinstance(repository, AsyncObjectBoundRepository)
# Constrained Repository
repository_class = make_async_constrained_repository_class_for(VulnerabilityClass, Request, [Project])
repository = repository_class(session, request_id=request_id, project_id=project_id)
assert isinstance(repository, AsyncConstrainedRepository)
```

## Support

Any help is welcome. you can either:

- [create an issue](https://gitlab.com/Tagashy/sqlgen/issues/new)
- look for TODO in the code and provide a MR with changes
- provide a MR for support of new class

## Roadmap

- Make a public python package

## Authors and acknowledgment

Currently, solely developed by Tagashy but any help is welcomed and will be credited here.

## License

See the [LICENSE](LICENSE) file for licensing information as it pertains to
files in this repository.
