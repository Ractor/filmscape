from requests import JSONDecodeError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import ConnectionError
import requests

from filmscape.serializers import VideoSerializer
from filmscape.models import Video
from django.conf import settings


class UpdateFilmList(APIView):
    """
    Fetches information from the video provider and saves them locally.
    """
    def get(self, request):
        try:
            r = requests.get(settings.FILMSCAPE_API_URL)
            data = r.json()
            serializer = VideoSerializer(data=data, many=True)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        except (JSONDecodeError, ConnectionError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
