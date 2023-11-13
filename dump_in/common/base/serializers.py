from rest_framework import serializers

from dump_in.common.exception.exceptions import InvalidParameterFormatException


class BaseSerializer(serializers.Serializer):
    """
    기본 API 입출력 Serializer 클래스입니다.
    data 필드에는 각 API의 입출력 데이터가 정의됩니다.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "data" in kwargs and not self.is_valid():
            raise InvalidParameterFormatException()

    class Meta:
        ref_name = None


class BaseModelSerializer(serializers.ModelSerializer):
    """
    기본 API 출력 Serializer 클래스입니다.
    이 클래스는 Model의 필드를 기반으로 자동으로 필드를 생성합니다.
    """

    class Meta:
        ref_name = None


class BaseResponseSerializer(serializers.Serializer):
    """
    기본 API 응답 Serializer 클래스입니다.
    이 클래스는 모든 API의 Swagger 문서에 응답 형식을 표시하기 위해 사용됩니다.

    Attributes:
        code (int) : 응답 코드
        success (bool) : 응답 성공 여부
        message (str) : 응답 메시지
        data (list) : 응답 데이터
    """

    code = serializers.IntegerField()
    success = serializers.BooleanField()
    message = serializers.CharField()

    def __init__(self, *args, **kwargs):
        data_serializer = kwargs.pop("data_serializer", None)
        super().__init__(*args, **kwargs)

        if data_serializer is not None:
            self.fields["data"] = data_serializer()

    class Meta:
        ref_name = None
