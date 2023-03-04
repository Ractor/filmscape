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
    # licenseServers -> TBA dependent model
    # licenseRequestHeaders -> TBA dependent model
    # requestFilter is always null, skipped
    # responseFilter is always null, skipped
    # clearKeys is always empty object, skipped
    # extraConfig is always null, skipped
    adTagUri = models.TextField(max_length=2048, null=True) # @todo change to URL field but it breaks of one URI (dunno why)
    imaVideoId = models.SlugField(null=True)
    # imaAssetKey is always null, skipped
    imaContentSrcId = models.PositiveIntegerField(null=True)
    # mimeType is always null, skipped
    # mediaPlaylistFullMimeType is always null, skipped
    storedProgress = models.PositiveIntegerField(null=True)
    # storedContent -> TBA dependent model

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs
    ):
        """
        Override function to original save() to update existing values (e.g. with the existing "name" value)
        """
        # Try to find existing record.
        try:
            video = Video.objects.get(name=self.name)
            self.id = video.id
        except Video.DoesNotExist:
            pass
        super().save(*args, **kwargs)
