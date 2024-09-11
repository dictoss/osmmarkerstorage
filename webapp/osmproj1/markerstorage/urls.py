from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('markerdata/', views.markerdata_list),
    path('markerdata/<int:pk>/', views.markerdata_detail),
    #
    path('osm/index.html', views.osm_index),
    # OpenLayer-2
    path('osm/ol2/first.html', views.osm_first),
    path('osm/ol2/marker1.html', views.osm_marker1),
    path('osm/ol2/marker2.html', views.osm_marker2),
    path('osm/ol2/marker2.json', views.osm_marker2_json),
    path('osm/ol2/marker3.html', views.osm_marker3),
    path('osm/ol2/tile1.html', views.osm_tile1),
    # OpenLayer-5
    path('osm/ol5/first.html', views.osm_ol5_first),
    path('osm/ol5/marker1.html', views.osm_ol5_marker1),
    #
    path('osm/tiles/<int:tile_ver>/testtile1/<int:tile_z>/<int:tile_x>/<int:tile_y>.png', views.osm_tile1_image),
    path('osm/', views.osm_index),
    path('', RedirectView.as_view(url='osm')),
]

urlpatterns += staticfiles_urlpatterns()
