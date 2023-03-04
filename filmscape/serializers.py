from filmscape.models import Video
from rest_framework import serializers


class VideoSerializer(serializers.ModelSerializer):
    # Override name validation to not validate unique field
    # (model updates existing row if name is found).
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Video
        fields = '__all__'
