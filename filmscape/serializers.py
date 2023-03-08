from filmscape.models import Video, ExtraText
from rest_framework import serializers


class VideoListImportSerializer(serializers.ListSerializer):
    """
    Extension of List Serializer to update existing Video instances if applicable.
    """
    def create(self, validated_data):
        output = []
        for attrs in validated_data:
            try:
                output.append(self.child.update(Video.objects.get(name=attrs['name']), attrs))
            except Video.DoesNotExist:
                output.append(self.child.create(attrs))
        return output


class VideoImportSerializer(serializers.ModelSerializer):
    """
    Serializer of Video model used when importing data from the external API.
    """
    # Override name validation to not validate unique field
    # (model updates existing row if name is found, see overwritten save() method).
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Video
        fields = '__all__'
        list_serializer_class = VideoListImportSerializer

    def _get_existing_model_instance(self, **kwargs):
        """
        Looks for existing Video model based on given name variable.

        :return: Video|None Video if found, None otherwise.
        """
        validated_data = {**self.validated_data, **kwargs}
        try:
            return Video.objects.get(name=validated_data['name'])
        except Video.DoesNotExist:
            return None

    def save(self, **kwargs):
        """
        Checks if there is existing model instance before calling parent save() method.

        :param kwargs: See super().save() for more information.
        :return:
        """

        self.instance = self._get_existing_model_instance(**kwargs)
        return super(self.__class__, self).save(**kwargs)


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['name', 'shortName', 'isFeatured', 'disabled', 'iconUri', 'description']
