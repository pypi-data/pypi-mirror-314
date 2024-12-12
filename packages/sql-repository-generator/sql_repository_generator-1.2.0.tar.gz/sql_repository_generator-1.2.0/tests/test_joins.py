import pytest

from sqlgen.joins import resolve_model_joins, NoValidJoins, Constraint
from test_data.models import Project, Host, Webserver, Request, User, VulnerabilityInstance, VulnerabilityClass


@pytest.mark.parametrize("source,destination,constraint", [
    (Host, Project, Constraint(Host.project_id, Project, [])),
    (Webserver, Project, Constraint(Host.project_id, Project, [Webserver.host])),
    (Request, Project, Constraint(Host.project_id, Project, [Request.webserver, Webserver.host])),
    (VulnerabilityInstance, Project,
     Constraint(Host.project_id, Project, [VulnerabilityInstance.request, Request.webserver, Webserver.host])),
    (Request, VulnerabilityClass,
     Constraint(VulnerabilityInstance.vulnerability_class_id, VulnerabilityClass, [Request.vulnerabilities])),
    (Project, Host, Constraint(Host.id, Host, [Project.hosts])),
])
def test_resolve_model_joins_should_return_list_of_joins(source, destination, constraint):
    assert resolve_model_joins(source, destination) == constraint


def test_resolve_model_joins_should_raise_if_no_relation_exist_between_models():
    with pytest.raises(NoValidJoins) as exc_info:
        resolve_model_joins(User, Project)
    assert str(exc_info.value) == ("No Relation between self.source=<class 'test_data.models.User'> and "
                                   "self.destination=<class 'test_data.models.Project'>")
