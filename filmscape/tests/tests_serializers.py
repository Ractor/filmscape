from django.test import TestCase
import copy

from rest_framework.exceptions import ErrorDetail

from filmscape.serializers import VideoSerializer


class VideoSerializerTests(TestCase):
    BASE_TESTING_DATA = {
        "name": "Some name",
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

    # Common test queries
    def _maxLengthNok(self, name: str, length: int):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = "A" * length

        serializer = VideoSerializer(data=dataset)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors,
                         {name: [ErrorDetail(string='Ensure this field has no more than 255 characters.',
                                             code='max_length')]})

    def _lengthOk(self, name: str, length: int):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = "A" * length

        serializer = VideoSerializer(data=dataset)
        self.assertTrue(serializer.is_valid())

    def _blankNok(self, name: str):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = ""

        serializer = VideoSerializer(data=dataset)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors,
                         {name: [ErrorDetail(string='This field may not be blank.',
                                             code='blank')]})

    def _blankOk(self, name: str):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = ""

        serializer = VideoSerializer(data=dataset)
        self.assertTrue(serializer.is_valid())

    def _nullNok(self, name: str):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = None

        serializer = VideoSerializer(data=dataset)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors,
                         {name: [ErrorDetail(string='This field may not be null.',
                                             code='null')]})

    def _nullOk(self, name: str):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = None

        serializer = VideoSerializer(data=dataset)
        self.assertTrue(serializer.is_valid())

    def _boolTrueOk(self, name: str):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = True

        serializer = VideoSerializer(data=dataset)
        self.assertTrue(serializer.is_valid())

    def _boolTrueNokNotString(self, name: str):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)
        dataset[name] = True

        serializer = VideoSerializer(data=dataset)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors,
                         {name: [ErrorDetail(string='Not a valid string.',
                                             code='invalid')]})

    def testOk(self):
        dataset = copy.deepcopy(self.BASE_TESTING_DATA)

        serializer = VideoSerializer(data=dataset)
        self.assertTrue(serializer.is_valid())

    # Name field

    def testNameLengthOk(self): self._lengthOk('name', 200)
    def testNameMaxLengthNok(self): self._maxLengthNok('name', 256)
    def testNameBlankNok(self): self._blankNok('name')
    def testNameNullNok(self): self._nullNok('name')
    def testNameBoolNok(self): self._boolTrueNokNotString('name')

    # ShortName field
    def testShortNameLengthOk(self): self._lengthOk('shortName', 200)
    def testShortNameMaxLengthNok(self): self._maxLengthNok('shortName', 256)
    def testShortNameBlankOk(self): self._blankOk('shortName')
    def testShortNameNullNok(self): self._nullNok('shortName')
    def testShortNameBoolNok(self): self._boolTrueNokNotString('shortName')

    def testFocusNullNok(self):
        self._nullNok('focus')
