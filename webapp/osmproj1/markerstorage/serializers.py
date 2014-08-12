from django.forms import widgets
from rest_framework import serializers
from markerstorage.models import *


class DemoMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoMarker
        fields = ('id', 'create_dt', 'update_dt', 'name',
                  'x', 'y', 'auther', 'desc', 'memo')
