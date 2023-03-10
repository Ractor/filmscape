from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
import logging

from filmscape.filters import CaseInsensitiveOrderingFilter
from filmscape.serializers import VideoSerializer
from filmscape.models import Video

logger = logging.getLogger(__name__)


class VideosView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, CaseInsensitiveOrderingFilter]
    filterset_fields = ['disabled', 'isFeatured']
    search_fields = ['name', 'shortName']
    ordering_fields = ['name']
