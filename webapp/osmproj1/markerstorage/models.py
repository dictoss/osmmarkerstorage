from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class MarkerBase(models.Model):
    id = models.AutoField(primary_key=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    name = models.TextField()
    x = models.TextField()
    y = models.TextField()
    auther = models.TextField()
    desc = models.TextField()
    memo = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return '%s - %s' % (self.id, self.name)


@python_2_unicode_compatible
class DemoMarker(MarkerBase):
    class Meta:
        ordering = ['-update_dt']

    def __str__(self):
        return '%s - %s' % (self.id, self.name)
