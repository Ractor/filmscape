from django_filters.rest_framework import DjangoFilterBackend
from requests import JSONDecodeError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from requests.exceptions import ConnectionError
import requests
import logging

from filmscape.filters import CaseInsensitiveOrderingFilter
from filmscape.serializers import VideoImportSerializer, VideoSerializer
from filmscape.models import Video
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
            serializer = VideoImportSerializer(data=data, many=True)

            # If there is any invalid record, parse records separately
            # and use a different HTTP status code to address this.
            if not serializer.is_valid():
                logger.debug('Serialization was not valid. Processing records one by one.')
                api_videos = []
                status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                errors = serializer.errors
                for i in range(len(data)):
                    logger.debug(f'Processing record "{data[i].get("name") or "<no_name>"}".')
                    if errors[i]:
                        logger.warning(f'Record with name "{data[i].get("name") or "<no_name>"}" threw following error: {str(errors[i])}')
                        continue

                    video = Video(**serializer.data[i])
                    video.save()
                    api_videos.append(video)
            else:
                logger.debug('Serialization was valid. Saving all records.')
                api_videos = serializer.save()
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

        return Response(status=status_code)


class VideosView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, CaseInsensitiveOrderingFilter]
    filterset_fields = ['disabled', 'isFeatured']
    search_fields = ['name', 'shortName']
    ordering_fields = ['name']
