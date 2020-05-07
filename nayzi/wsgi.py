"""
WSGI config for nayzi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'nayzi/' + os.environ.get('environment', 'production.env'))
load_dotenv(dotenv_path=env_file, verbose=True)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nayzi.settings")

application = get_wsgi_application()
