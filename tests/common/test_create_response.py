from rest_framework import status

from dump_in.common.response import create_response


def test_create_response():
    custom_data = {"key": "custom_value"}
    response = create_response(
        data=custom_data,
        status_code=status.HTTP_200_OK,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["code"] == 0
    assert response.data["success"] is True
    assert response.data["message"] == "Request was successful."
    assert response.data["data"] == custom_data
