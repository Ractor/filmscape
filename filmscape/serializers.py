from filmscape.models import Video, ExtraText, Drm, Features
from rest_framework import serializers


class ExtraTextImportSerializer(serializers.ModelSerializer):
    # Ignore the unique together validator as it will be dealt with during saving.
    def get_unique_together_validators(self): return []

    class Meta:
        model = ExtraText
        fields = '__all__'


class DrmImportSerializer(serializers.ModelSerializer):
    # Ignore the unique together validator as it will be dealt with during saving.
    def get_unique_together_validators(self): return []

    class Meta:
        model = Drm
        fields = '__all__'


class FeaturesImportSerializer(serializers.ModelSerializer):
    # Ignore the unique together validator as it will be dealt with during saving.
    def get_unique_together_validators(self): return []

    class Meta:
        model = Features
        fields = '__all__'


class VideoImportSerializer(serializers.ModelSerializer):
    """
    Serializer of Video model used when importing data from the external API.
    """
    # Override name validation to not validate unique field.
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Video
        fields = '__all__'


class ExtraTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtraText
        fields = ['uri', 'language', 'kind', 'mime']


class VideoSerializer(serializers.ModelSerializer):
    extraText = ExtraTextSerializer(many=True, read_only=True)
    drm = serializers.StringRelatedField(many=True)
    features = serializers.StringRelatedField(many=True)

    class Meta:
        model = Video
        fields = ['name', 'shortName', 'isFeatured', 'disabled', 'iconUri',
                  'description', 'extraText', 'drm', 'features']
