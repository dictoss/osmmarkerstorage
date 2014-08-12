from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class MarkerBase(models.Model):
    id = models.AutoField(primary_key=True)
    create_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_dt = models.DateTimeField(auto_now_add=True, auto_now=True)
    name = models.TextField()
    x = models.TextField()
    y = models.TextField()
    auther = models.TextField()
    desc = models.TextField()
    memo = models.TextField()

    class Meta:
        abstract = True


class DemoMarker(MarkerBase):
    class Meta:
        ordering = ['-update_dt']
