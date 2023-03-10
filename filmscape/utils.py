from filmscape.models import ExtraText, Features, Drm, Video
from filmscape.serializers import VideoImportSerializer, ExtraTextImportSerializer, FeaturesImportSerializer, \
    DrmImportSerializer


def create_or_update_video_instances(video_data, logger=None):
    """
    Updates existing Video instances (and related) with given data. Non existent instances it creates.

    :param video_data: List of videos decoded from API JSON.
    :param logger: Logging instance
    :return: Tuple of (ok, instances).
        Value of 'ok' is False if there were any (minor) errors during processing, True otherwise.
        The 'instances' contain dictionary of lists of 'video', 'drm', 'features' and 'extraText' instances.
    """
    output_ok = True
    output_instances = {
        'video': [],
        'drm': [],
        'features': [],
        'extraText': [],
    }
    stats = {
        'video': [0, 0, 0],  # [created, updated, warning]
        'drm': [0, 0, 0],
        'features': [0, 0, 0],
        'extraText': [0, 0, 0],
    }

    # Processing videos
    for d in video_data:
        video_name = d.get("name") or "<no_name>"
        if logger:
            logger.debug(f'Processing record "{video_name}".')
        serializer = VideoImportSerializer(data=d)

        # If there is any invalid record use a different HTTP status code to address this.
        if not serializer.is_valid():
            output_ok = False
            stats['video'][2] += 1
            if logger:
                logger.warning(f'Record "{video_name}" threw following error: {str(serializer.errors)}')
            continue

        # Save video itself
        video_instance, created = Video.objects.update_or_create(name=d.get("name"),
                                                                 defaults=serializer.validated_data)
        stats['video'][0 if created else 1] += 1
        if logger:
            logger.debug(f'Record "{video_name}" processed successfully.')

        # Process data for secondary tables
        # - drm
        if 'drm' in d:
            if type(d['drm']) != list:
                output_ok = False
                if logger:
                    logger.warning(f'Record "{video_name}" drm argument is not list.')
                continue
            else:
                for drm in d['drm']:
                    drm_data = {'drm': drm, 'video': video_instance.pk}
                    drm_serializer = DrmImportSerializer(data=drm_data)
                    if not drm_serializer.is_valid():
                        output_ok = False
                        stats['drm'][2] += 1
                        if logger:
                            logger.warning(f'Record "{video_name}" threw following error ' +
                                           f'for drm: {str(drm_serializer.errors)}')
                        continue
                    drm_instance, created = Drm.objects.update_or_create(video=video_instance,
                                                                         drm=drm,
                                                                         defaults=drm_serializer.validated_data)
                    stats['drm'][0 if created else 1] += 1
                    output_instances['drm'].append(drm_instance)

        # - features
        if 'features' in d:
            if type(d['features']) != list:
                output_ok = False
                if logger:
                    logger.warning(f'Record "{video_name}" features argument is not list.')
                continue
            else:
                for feature in d['features']:
                    features_data = {'feature': feature, 'video': video_instance.pk}
                    features_serializer = FeaturesImportSerializer(data=features_data)
                    if not features_serializer.is_valid():
                        output_ok = False
                        stats['features'][2] += 1
                        if logger:
                            logger.warning(f'Record "{video_name}" threw following error ' +
                                           f'for features: {str(features_serializer.errors)}')
                        continue
                    features_instance, created = Features.objects.update_or_create(video=video_instance,
                                                                                   feature=feature,
                                                                                   defaults=features_serializer.
                                                                                   validated_data)
                    stats['features'][0 if created else 1] += 1
                    output_instances['features'].append(features_instance)
        output_instances['video'].append(video_instance)

        # - extraText
        # (the extraText information is not essential for video playback,
        # that's why it does not come before listing the video itself)
        if 'extraText' in d:
            if type(d['extraText']) != list:
                output_ok = False
                stats['extraText'][2] += 1
                if logger:
                    logger.warning(f'Record "{video_name}" extraText argument is not list.')
            else:
                for et_data in d['extraText']:
                    et_serializer = ExtraTextImportSerializer(data={**et_data, 'video': video_instance.pk})
                    if not et_serializer.is_valid():
                        output_ok = False
                        if logger:
                            logger.warning(f'Record "{video_name}" threw following error ' +
                                           f'for extraText: {str(et_serializer.errors)}')
                        continue
                    et_instance, created = ExtraText.objects.update_or_create(video=video_instance,
                                                                              uri=et_serializer.validated_data['uri'],
                                                                              defaults=et_serializer.validated_data)
                    stats['extraText'][0 if created else 1] += 1
                    output_instances['extraText'].append(et_instance)
    if logger:
        s = 'Processing ended with following results (created, updated, warning):\n' + \
            f'Video:\t{stats["video"][0]}\t{stats["video"][1]}\t{stats["video"][2]}\n' + \
            f'DRM:\t{stats["drm"][0]}\t{stats["drm"][1]}\t{stats["drm"][2]}\n' + \
            f'Features:\t{stats["features"][0]}\t{stats["features"][1]}\t{stats["features"][2]}\n' + \
            f'extraText:\t{stats["extraText"][0]}\t{stats["extraText"][1]}\t{stats["extraText"][2]}'
        logger.info(s)
    return output_ok, output_instances


def delete_obsolete_video_instances(video_data, logger=None):
    """
    Deletes Video (and related) records which became obsolete.

    :param video_data: Dictionary of lists of 'video', 'drm', 'features' and 'extraText' instances to be kept.
    :param logger: Logging instance.
    :return: None
    """
    # Handle deletion of obsolete records in the database.
    if logger:
        logger.info('Deleting obsolete records.')
    all_videos = list(Video.objects.all())
    obsolete_videos = [v for v in all_videos if v not in video_data['video']]
    for video in obsolete_videos:
        if logger:
            logger.debug(f'Deleting record "{video.name}".')
        video.delete()

    if logger:
        logger.info('Deleting obsolete drms.')
    all_drm = list(Drm.objects.all())
    obsolete_drm = [drm for drm in all_drm if drm not in video_data['drm']]
    for drm in obsolete_drm:
        drm.delete()

    if logger:
        logger.info('Deleting obsolete features.')
    all_features = list(Features.objects.all())
    obsolete_features = [features for features in all_features if features not in video_data['features']]
    for features in obsolete_features:
        features.delete()

    if logger:
        logger.info('Deleting obsolete extraTexts.')
    all_extratext = list(ExtraText.objects.all())
    obsolete_extratext = [et for et in all_extratext if et not in video_data['extraText']]
    for extratext in obsolete_extratext:
        extratext.delete()
    if logger:
        s = f'Deleted {len(obsolete_videos)} videos, {len(obsolete_drm)} drm, {len(obsolete_features)} ' + \
            f'features, {len(obsolete_extratext)} extraTexts'
        logger.info(s)
