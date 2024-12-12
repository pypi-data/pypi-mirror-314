import pytest

from sqlgen.utils import take, index
from test_data.models import Request, Webserver, VulnerabilityInstance


def test_take_should_return_valid_object():
    # given
    dataset = [Webserver.host, Request.webserver, VulnerabilityInstance.vulnerability_class, Request.vulnerabilities]
    model = VulnerabilityInstance
    # when
    result = take(lambda j: j.class_ == model, dataset)
    # then
    assert result is VulnerabilityInstance.vulnerability_class


def test_take_should_raise_if_not_found():
    # given
    dataset = [Webserver.host, Request.webserver, VulnerabilityInstance.vulnerability_class, Request.vulnerabilities]
    # then
    with pytest.raises(KeyError):
        # when
        take(lambda x: False, dataset)


def test_take_should_raise_if_multiple_result():
    # given
    dataset = [Webserver.host, Request.webserver, VulnerabilityInstance.vulnerability_class, Request.vulnerabilities]
    # then
    with pytest.raises(KeyError):
        # when
        take(lambda x: True, dataset)


def test_index_should_return_valid_index():
    # given
    dataset = [Webserver.host, Request.webserver, VulnerabilityInstance.vulnerability_class,
               Request.vulnerabilities]
    model = VulnerabilityInstance
    # when
    result = index(lambda j: j.class_ == model, dataset)
    # then
    assert result == 2
