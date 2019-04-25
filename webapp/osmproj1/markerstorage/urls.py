from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^markerdata/$', views.markerdata_list),
    url(r'^markerdata/(?P<pk>[0-9]+)/$', views.markerdata_detail),
    #
    url(r'^osm/index.html', views.osm_index),
    # OpenLayer-2
    url(r'^osm/ol2/first.html', views.osm_first),
    url(r'^osm/ol2/marker1.html', views.osm_marker1),
    url(r'^osm/ol2/marker2.html', views.osm_marker2),
    url(r'^osm/ol2/marker2.json', views.osm_marker2_json),
    url(r'^osm/ol2/marker3.html', views.osm_marker3),
    url(r'^osm/ol2/tile1.html', views.osm_tile1),
    # OpenLayer-5
    url(r'^osm/ol5/first.html', views.osm_ol5_first),
    url(r'^osm/ol5/marker1.html', views.osm_ol5_marker1),
    #
    url(r'^osm/tiles/(?P<tile_ver>\d+)/testtile1/(?P<tile_z>\d+)/(?P<tile_x>\d+)/(?P<tile_y>\d+).png', views.osm_tile1_image),
    url(r'^osm/$', views.osm_index),
    url(r'^$', RedirectView.as_view(url='osm')),
]

urlpatterns += staticfiles_urlpatterns()
