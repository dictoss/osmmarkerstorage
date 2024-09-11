from django.test import TestCase, Client
from django.urls import reverse

from .models import (
    DemoMarker,
)

class MarkerDataListViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:markerdata_list'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class MarkerDataDetailViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:markerdata_detail'

    def test_get(self):
        # add model
        _o = DemoMarker(
            name='test_marker_1',
            x='35.685175',
            y='139.7528',
            auther='a',
            desc='b',
            memo='memomemo')
        _o.save()

        _response = self.client.get(reverse(self.view_name, args=[_o.id]))
        self.assertEqual(_response.status_code, 200)

class OsmIndexViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_index'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmFirstViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol2_first'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmMarker1ViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol2_marker1'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmMarker2ViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol2_marker2_html'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmMarker2JsonViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol2_marker2_json'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmMarker3ViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol2_marker3'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmTile1ViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol2_tile1'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)
class OsmTile1ImageViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_tiles_testtile1_ver_zxy'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name, args=[1, 1, 2, 3]))
        self.assertEqual(_response.status_code, 200)

class OsmOl5FirstViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol5_first'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)

class OsmOl5Marker1ViewTestCase(TestCase):
    fixtures = []
    view_name = 'markerstorage:osm_ol5_marker1'

    def test_get(self):
        _response = self.client.get(reverse(self.view_name))
        self.assertEqual(_response.status_code, 200)
