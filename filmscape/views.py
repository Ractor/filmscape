from requests import JSONDecodeError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import ConnectionError
import requests
import logging

from filmscape.serializers import VideoSerializer
from filmscape.models import Video
from django.conf import settings

logger = logging.getLogger(__name__)


class UpdateFilmList(APIView):
    """
    Fetches information from the video provider and saves them locally.
    """
    def get(self, request):
        # Handle creation and updating records present in the API.
        try:
            r = requests.get(settings.FILMSCAPE_API_URL)
            data = r.json()
            serializer = VideoSerializer(data=data, many=True)

            # If there is any invalid record, parse records separately
            # and use a different HTTP status code to address this.
            if not serializer.is_valid():
                errors = serializer.errors
                for i in range(len(data)):
                    if errors[i]:
                        logger.warning(f'Record with name "{data[i].get("name") or "<no_name>"}" threw following error: ' + str(errors[i]))
                        continue

                    video = Video(**serializer.data[i])
                    video.save()
                return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        except (JSONDecodeError, ConnectionError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


