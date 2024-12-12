from uuid import uuid4

from pytest_unordered import unordered

from sqlgen import AsyncRepository, AsyncObjectBoundRepository, AsyncConstrainedRepository
from sqlgen.helpers import make_async_repository_class_for, make_async_object_bound_repository_class_for, \
    make_async_constrained_repository_class_for
from sqlgen.joins import Constraint
from test_data.models import VulnerabilityClass, Project, VulnerabilityInstance, Host, Webserver, Request


def test_make_async_repository_class_for_should_return_async_repository(mocker):
    repository_class = make_async_repository_class_for(VulnerabilityClass)
    repository = repository_class(mocker.Mock())
    # then
    assert isinstance(repository, AsyncRepository)
    assert repository.statement_generator.cls == VulnerabilityClass


def test_make_async_object_bound_repository_class_for_should_return_async_object_bound_repository(mocker):
    session = mocker.Mock()
    project_id = uuid4()
    # when
    repository_class = make_async_object_bound_repository_class_for(VulnerabilityClass, Project)
    repository = repository_class(session, project_id)
    # then
    assert isinstance(repository, AsyncObjectBoundRepository)
    assert repository.statement_generator.cls == VulnerabilityClass
    assert repository.statement_generator.joins == [VulnerabilityClass.instances, VulnerabilityInstance.request,
                                                    Request.webserver, Webserver.host, Host.project_id]
    assert repository.statement_generator.bound_object_id == project_id


def test_make_async_constrained_repository_class_for_should_return_async_constrained_repository(mocker):
    session = mocker.Mock()
    request_id = uuid4()
    project_id = uuid4()
    # when
    repository_class = make_async_constrained_repository_class_for(VulnerabilityClass, Request, [Project])
    repository = repository_class(session, request_id=request_id, project_id=project_id)
    # then
    assert isinstance(repository, AsyncConstrainedRepository)
    assert repository.statement_generator.cls == VulnerabilityClass
    assert repository.statement_generator.constraints == unordered([
        Constraint(joined_column=VulnerabilityInstance.__table__.columns["request_id"],
                   joined_model=Request,
                   joins=[VulnerabilityClass.instances],
                   _bound_object_id=request_id),
        Constraint(joined_column=Host.__table__.columns["project_id"],
                   joined_model=Project,
                   joins=[VulnerabilityClass.instances, VulnerabilityInstance.request, Request.webserver,
                          Webserver.host],
                   _bound_object_id=project_id)])
