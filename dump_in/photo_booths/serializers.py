from rest_framework import serializers

from dump_in.photo_booths.models import Hashtag, PhotoBoothBrandImage


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            "id",
            "name",
        )


class PhotoBoothBrandImageSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source="photo_booth_brand_image_url")

    class Meta:
        model = PhotoBoothBrandImage
        fields = (
            "id",
            "image_url",
        )
