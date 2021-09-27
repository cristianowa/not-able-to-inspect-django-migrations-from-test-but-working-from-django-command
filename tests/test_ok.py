import pytest

from sampleapp.models import SampleModel


@pytest.mark.django_db
def test_pass():
    sm = SampleModel()
    sm.one_field = 1
    sm.save()
    assert isinstance(sm, SampleModel)

