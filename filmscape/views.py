from django_filters.rest_framework import DjangoFilterBackend
from requests import JSONDecodeError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from requests.exceptions import ConnectionError
import requests
import logging

from filmscape.filters import CaseInsensitiveOrderingFilter
from filmscape.serializers import VideoImportSerializer, VideoSerializer, ExtraTextImportSerializer, \
    DrmImportSerializer, FeaturesImportSerializer
from filmscape.models import Video, ExtraText, Drm, Features
from django.conf import settings

logger = logging.getLogger(__name__)


class UpdateFilmListView(APIView):
    """
    Fetches information from the video provider and saves them locally.
    """
    def get(self, request):
        status_code = status.HTTP_200_OK

        # Handle creation and updating records present in the API.
        try:
            logger.debug('Attempting to get data from API.')
            r = requests.get(settings.FILMSCAPE_API_URL)
            data = r.json()
            logger.debug('Serializing fetched data.')

            # Processing videos
            api_videos = []
            api_drm = []
            api_features = []
            api_extratext = []
            for d in data:
                video_name = d.get("name") or "<no_name>"
                logger.debug(f'Processing record "{video_name}".')
                serializer = VideoImportSerializer(data=d)

                # If there is any invalid record use a different HTTP status code to address this.
                if not serializer.is_valid():
                    status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                    logger.warning(f'Record "{video_name}" threw following error: {str(serializer.errors)}')
                    continue

                # Save video itself
                video_instance, _ = Video.objects.update_or_create(name=d.get("name"),
                                                                   defaults=serializer.validated_data)
                logger.debug(f'Record "{video_name}" processed successfully.')

                # Process data for secondary tables
                # - drm
                if 'drm' in d:
                    if type(d['drm']) != list:
                        status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                        logger.warning(f'Record "{video_name}" drm argument is not list.')
                        continue
                    else:
                        for drm in d['drm']:
                            drm_data = {'drm': drm, 'video': video_instance.pk}
                            drm_serializer = DrmImportSerializer(data=drm_data)
                            if not drm_serializer.is_valid():
                                status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                                logger.warning(f'Record "{video_name}" threw following error ' +
                                               f'for drm: {str(drm_serializer.errors)}')
                                continue
                            drm_instance, _ = Drm.objects.update_or_create(video=video_instance,
                                                                           drm=drm,
                                                                           defaults=drm_serializer.validated_data)
                            api_drm.append(drm_instance)

                # - features
                if 'features' in d:
                    if type(d['features']) != list:
                        status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                        logger.warning(f'Record "{video_name}" features argument is not list.')
                        continue
                    else:
                        for feature in d['features']:
                            features_data = {'feature': feature, 'video': video_instance.pk}
                            features_serializer = FeaturesImportSerializer(data=features_data)
                            if not features_serializer.is_valid():
                                status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                                logger.warning(f'Record "{video_name}" threw following error ' +
                                               f'for features: {str(features_serializer.errors)}')
                                continue
                            features_instance, _ = Features.objects.update_or_create(video=video_instance,
                                                                                     feature=feature,
                                                                                     defaults=features_serializer.
                                                                                     validated_data)
                            api_features.append(features_instance)

                api_videos.append(video_instance)

                # - extraText
                # (the extraText information is not essential for video playback,
                # that's why it does not come before listing the video itself)
                if 'extraText' in d:
                    if type(d['extraText']) != list:
                        status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                        logger.warning(f'Record "{video_name}" extraText argument is not list.')
                    else:
                        for et_data in d['extraText']:
                            et_serializer = ExtraTextImportSerializer(data={**et_data, 'video': video_instance.pk})
                            if not et_serializer.is_valid():
                                status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                                logger.warning(f'Record "{video_name}" threw following error ' +
                                               f'for extraText: {str(et_serializer.errors)}')
                                continue
                            et_instance, _ = ExtraText.objects.update_or_create(video=video_instance,
                                                                                uri=et_serializer.validated_data['uri'],
                                                                                defaults=et_serializer.validated_data)
                            api_extratext.append(et_instance)

        except (JSONDecodeError, ConnectionError) as err:
            logger.error(f'Error occurred during API data processing: {err}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle deletion of obsolete records in the database.
        logger.debug('Deleting obsolete records.')
        all_videos = list(Video.objects.all())
        obsolete_videos = [v for v in all_videos if v not in api_videos]
        for video in obsolete_videos:
            logger.debug(f'Deleting record "{video.name}".')
            video.delete()

        logger.debug('Deleting obsolete drms.')
        all_drm = list(Drm.objects.all())
        obsolete_drm = [drm for drm in all_drm if drm not in api_drm]
        for drm in obsolete_drm:
            drm.delete()

        logger.debug('Deleting obsolete features.')
        all_features = list(Features.objects.all())
        obsolete_features = [features for features in all_features if features not in api_features]
        for features in obsolete_features:
            features.delete()

        logger.debug('Deleting obsolete extraTexts.')
        all_extratext = list(ExtraText.objects.all())
        obsolete_extratext = [et for et in all_extratext if et not in api_extratext]
        for extratext in obsolete_extratext:
            extratext.delete()

        return Response(status=status_code)


class VideosView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, CaseInsensitiveOrderingFilter]
    filterset_fields = ['disabled', 'isFeatured']
    search_fields = ['name', 'shortName']
    ordering_fields = ['name']
