from datetime import datetime, timezone

import pytest
from rest_framework import serializers

from dump_in.common.utils import inline_serializer, make_mock_object


@pytest.fixture
def mock_datetime():
    return datetime(year=2021, month=1, day=1, hour=1, minute=1, second=1, microsecond=1, tzinfo=timezone.utc)


@pytest.fixture
def mock_object(mock_datetime):
    return make_mock_object(foo=1, bar="bar", dt=mock_datetime)


def test_inline_serializer_creates_a_serializer(mock_datetime, mock_object):
    expected_dt = "2021-01-01T10:01:01.000001+09:00"

    serializer = inline_serializer(
        fields={
            "foo": serializers.IntegerField(),
            "bar": serializers.CharField(),
            "dt": serializers.DateTimeField(),
        }
    )

    # Output
    result = serializer.to_representation(mock_object)
    expected = {"foo": 1, "bar": "bar", "dt": expected_dt}
    assert expected == result

    # Input
    payload = {"foo": 1, "bar": "bar", "dt": expected_dt}
    result = serializer.to_internal_value(payload)
    expected = {"foo": 1, "bar": "bar", "dt": mock_datetime}
    assert expected == result


def test_inline_serializer_passes_kwargs(mock_object):
    serializer = inline_serializer(
        many=True,
        fields={
            "foo": serializers.IntegerField(),
        },
    )

    objects = [mock_object]

    # Output
    result = serializer.to_representation(objects)
    expected = [{"foo": 1}]
    assert expected == result

    # Input
    payload = [{"foo": 1}]
    result = serializer.to_internal_value(payload)
    expected = [{"foo": 1}]
    assert expected == result
