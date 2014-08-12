from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('markerstorage.views',
    url(r'^markerdata/$', 'markerdata_list'),
    url(r'^markerdata/(?P<pk>[0-9]+)/$', 'markerdata_detail'),
    #
    url(r'^osm/index.html', 'osm_index'),
    url(r'^osm/first.html', 'osm_first'),
    url(r'^osm/marker1.html', 'osm_marker1'),
    url(r'^osm/marker2.html', 'osm_marker2'),
    url(r'^osm/marker2.json', 'osm_marker2_json'),
    url(r'^osm/marker3.html', 'osm_marker3'),
    url(r'^osm/$', 'osm_index'),
)

urlpatterns += staticfiles_urlpatterns()
