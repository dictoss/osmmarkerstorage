import os
import sys

path = os.path.realpath(os.path.dirname(__file__))
if not path in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'osmproj1.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

