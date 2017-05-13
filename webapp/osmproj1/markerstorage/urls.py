from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^markerdata/$', views.markerdata_list),
    url(r'^markerdata/(?P<pk>[0-9]+)/$', views.markerdata_detail),
    #
    url(r'^osm/index.html', views.osm_index),
    url(r'^osm/first.html', views.osm_first),
    url(r'^osm/marker1.html', views.osm_marker1),
    url(r'^osm/marker2.html', views.osm_marker2),
    url(r'^osm/marker2.json', views.osm_marker2_json),
    url(r'^osm/marker3.html', views.osm_marker3),
    url(r'^osm/tile1.html', views.osm_tile1),
    url(r'^osm/tiles/(?P<tile_ver>\d+)/testtile1/(?P<tile_z>\d+)/(?P<tile_x>\d+)/(?P<tile_y>\d+).png', views.osm_tile1_image),
    url(r'^osm/$', views.osm_index),
]

urlpatterns += staticfiles_urlpatterns()
