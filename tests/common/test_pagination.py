from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from dump_in.common.pagination import LimitOffsetPagination, get_paginated_data
from dump_in.users.models import User

factory = APIRequestFactory()


class ExampleListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email")

    def get(self, request):
        queryset = User.objects.order_by("id")

        data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )

        return Response(data=data, status=status.HTTP_200_OK)


class TestGetPaginatedData:
    def test_response_is_paginated_correctly(self, new_users):
        request = factory.get("/some/path")
        view = ExampleListApi.as_view()
        response = view(request)

        assert response.status_code == 200

        data = response.data
        assert data["limit"] == 1
        assert data["offset"] == 0
        assert data["count"] == 11
        assert data["next"] == "http://testserver/some/path?limit=1&offset=1"
        assert data["previous"] is None

        results = data["results"]
        assert len(results) == 1
        assert results[0]["id"] == 1
        assert results[0]["email"] == "test1@test.com"

        next_page_request = factory.get("/some/path?limit=1&offset=1")
        next_page_response = view(next_page_request)

        assert next_page_response.status_code == 200

        next_page_data = next_page_response.data
        assert next_page_data["limit"] == 1
        assert next_page_data["offset"] == 1
        assert next_page_data["count"] == 11
        assert next_page_data["next"] == "http://testserver/some/path?limit=1&offset=2"
        assert next_page_data["previous"] == "http://testserver/some/path?limit=1"

        next_page_results = next_page_data["results"]
        assert len(next_page_results) == 1
        assert next_page_results[0]["id"] == 2
        assert next_page_results[0]["email"] == "test2@test.com"
