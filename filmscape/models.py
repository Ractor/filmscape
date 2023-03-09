from django.db import models


class Video(models.Model):
    """
    Root model for fetched records.
    """
    name = models.CharField(max_length=255, unique=True)
    shortName = models.CharField(max_length=255, blank=True)
    iconUri = models.URLField()
    manifestUri = models.URLField()
    source = models.SlugField()
    focus = models.BooleanField()
    disabled = models.BooleanField()
    # extraText -> dependent model
    # certificateUri is always null, skipped
    description = models.TextField(null=True)
    isFeatured = models.BooleanField()
    # drm -> dependent model
    # features -> dependent model
    licenseServers = models.JSONField()
    licenseRequestHeaders = models.JSONField()
    # requestFilter is always null, skipped
    # responseFilter is always null, skipped
    # clearKeys is always empty object, skipped
    # extraConfig is always null, skipped
    adTagUri = models.URLField(max_length=2048, null=True)
    imaVideoId = models.SlugField(null=True)
    # imaAssetKey is always null, skipped
    imaContentSrcId = models.PositiveIntegerField(null=True)
    # mimeType is always null, skipped
    # mediaPlaylistFullMimeType is always null, skipped
    storedProgress = models.PositiveIntegerField(null=True)
    storedContent = models.JSONField(null=True)


class ExtraText(models.Model):
    """
    Secondary table for Video model containing subtitles and other secondary text.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="extraText")
    uri = models.URLField()
    language = models.CharField(max_length=2)
    kind = models.CharField(max_length=20)
    mime = models.CharField(max_length=20)

    class Meta:
        unique_together = ('video', 'uri')


class Drm(models.Model):
    """
    Secondary table for Video model containing Digital Rights Management (DRM) information.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="drm")
    drm = models.SlugField()

    class Meta:
        unique_together = ('video', 'drm')

    def __str__(self):
        return f'{self.drm}'


class Features(models.Model):
    """
    Secondary table for Video model containing information about features.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="features")
    feature = models.SlugField()

    class Meta:
        unique_together = ('video', 'feature')

    def __str__(self):
        return f'{self.feature}'
