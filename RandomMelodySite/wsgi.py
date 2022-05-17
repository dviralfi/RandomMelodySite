"""
WSGI config for RandomMelodySite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RandomMelodySite.settings')

application = get_wsgi_application()
"""
#I added this due to python path problems:
root_path = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(root_path, 'RandomMelodySite'))
sys.path.insert(0, root_path)
"""