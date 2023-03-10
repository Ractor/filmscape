from django.test import TestCase

from filmscape.models import Video
from filmscape.utils import create_or_update_video_instances, delete_obsolete_video_instances


class UtilsTests(TestCase):
    VIDEO_ADDING_TEST_DATA = [
        {
            "name": "Correct film",
            "shortName": "",
            "iconUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "manifestUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "source": "DEMO_ALPHA",
            "focus": False,
            "disabled": False,
            "extraText": [],
            "description": None,
            "isFeatured": False,
            "drm": [
                "DEMO_BETA"
            ],
            "features": [
                "DEMO_GAMMA",
                "DEMO_DELTA_EPSILON",
                "DEMO_IOTA",
                "DEMO_MHI",
            ],
            "licenseServers": {
            },
            "licenseRequestHeaders": {
            },
            "adTagUri": None,
            "imaVideoId": None,
            "imaContentSrcId": None,
            "storedProgress": 1,
            "storedContent": None
        },
        {
            "name": "Correct film 2",
            "shortName": "",
            "iconUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "manifestUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "source": "DEMO_ALPHA",
            "focus": False,
            "disabled": False,
            "extraText": [],
            "description": None,
            "isFeatured": False,
            "drm": [
                "DEMO_BETA"
            ],
            "features": [],
            "licenseServers": {
            },
            "licenseRequestHeaders": {
            },
            "adTagUri": None,
            "imaVideoId": None,
            "imaContentSrcId": None,
            "storedProgress": 1,
            "storedContent": None
        },
        {
            "name": "Incorrect film",
            "shortName": "",
            "iconUri": "something not URI",
            "manifestUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "source": "DEMO_ALPHA",
            "focus": False,
            "disabled": False,
            "extraText": [],
            "description": None,
            "isFeatured": "Some random value",
            "drm": [
                "DEMO_BETA"
            ],
            "features": [
                "DEMO_GAMMA",
                "DEMO_DELTA_EPSILON",
                "DEMO_IOTA",
                "DEMO_MHI",
            ],
            "licenseServers": {
            },
            "licenseRequestHeaders": {
            },
            "adTagUri": None,
            "imaVideoId": None,
            "imaContentSrcId": None,
            "storedProgress": 1,
            "storedContent": None
        },
    ]

    VIDEO_REMOVING_TEST_DATA = [
        {
            "name": "Correct film",
            "shortName": "",
            "iconUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "manifestUri": "https://dummyimage.com/640x360/fff/aaa.png",
            "source": "DEMO_ALPHA",
            "focus": False,
            "disabled": False,
            "extraText": [],
            "description": None,
            "isFeatured": False,
            "drm": [
                "DEMO_BETA"
            ],
            "features": [
                "DEMO_GAMMA",
                "DEMO_DELTA_EPSILON",
                "DEMO_IOTA",
                "DEMO_MHI",
            ],
            "licenseServers": {
            },
            "licenseRequestHeaders": {
            },
            "adTagUri": None,
            "imaVideoId": None,
            "imaContentSrcId": None,
            "storedProgress": 1,
            "storedContent": None
        }
    ]

    def test_video_adding(self):
        ok, instances = create_or_update_video_instances(self.__class__.VIDEO_ADDING_TEST_DATA)

        self.assertFalse(ok)
        try:
            Video.objects.get(name='Incorrect film')
            self.fail('Incorrect film should not be added.')
        except Video.DoesNotExist:
            pass

        Video.objects.get(name='Correct film')
        Video.objects.get(name='Correct film 2')

    def test_video_deleting(self):
        create_or_update_video_instances(self.__class__.VIDEO_ADDING_TEST_DATA)
        _, instances = create_or_update_video_instances(self.__class__.VIDEO_REMOVING_TEST_DATA)

        delete_obsolete_video_instances(instances)

        try:
            Video.objects.get(name='Correct film 2')
            self.fail('Correct film should be deleted.')
        except Video.DoesNotExist:
            pass

        Video.objects.get(name='Correct film')


