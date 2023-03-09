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
    # extraText -> TBA dependent model
    # certificateUri is always null, skipped
    description = models.TextField(null=True)
    isFeatured = models.BooleanField()
    # drm -> TBA dependent model
    # features -> TBA dependent model
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
