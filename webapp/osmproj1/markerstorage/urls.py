from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

app_name = 'markerstorage'

from .views import (
    MarkerDataListView,
    MarkerDataDetailView,
    OsmIndexView,
    OsmFirstView,
    OsmMarker1View,
    OsmMarker2View,
    OsmMarker2JsonView,
    OsmMarker3View,
    OsmTile1View,
    OsmOl5FirstView,
    OsmOl5Marker1View,
    OsmTile1ImageView,
)

urlpatterns = [
    path('markerdata/', MarkerDataListView.as_view(), name='markerdata_list'),
    path('markerdata/<int:pk>/', MarkerDataDetailView.as_view(), name='markerdata_detail'),
    #
    path('osm/index.html', OsmIndexView.as_view(), name='osm_index'),
    # OpenLayer-2
    path('osm/ol2/first.html', OsmFirstView.as_view(), name='osm_ol2_first'),
    path('osm/ol2/marker1.html', OsmMarker1View.as_view(), name='osm_ol2_marker1'),
    path('osm/ol2/marker2.html', OsmMarker2View.as_view(), name='osm_ol2_marker2_html'),
    path('osm/ol2/marker2.json', OsmMarker2JsonView.as_view(), name='osm_ol2_marker2_json'),
    path('osm/ol2/marker3.html', OsmMarker3View.as_view(), name='osm_ol2_marker3'),
    path('osm/ol2/tile1.html', OsmTile1View.as_view(), name='osm_ol2_tile1'),
    # OpenLayer-5
    path('osm/ol5/first.html', OsmOl5FirstView.as_view(), name='osm_ol5_first'),
    path('osm/ol5/marker1.html', OsmOl5Marker1View.as_view(), name='osm_ol5_marker1'),
    #
    path('osm/tiles/<int:tile_ver>/testtile1/<int:tile_z>/<int:tile_x>/<int:tile_y>.png', OsmTile1ImageView.as_view(), name='osm_tiles_testtile1_ver_zxy'),
    path('osm/', OsmIndexView.as_view(), name='osm_index'),
    path('', RedirectView.as_view(url='osm'), name='index'),
]

urlpatterns += staticfiles_urlpatterns()
