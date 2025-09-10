# -*- coding: utf-8 -*-
import os
import sys
from django.core.wsgi import get_wsgi_application


sys.path.insert(0, "/var/www/u2608216/data/www/e-studio.store/danke")
sys.path.insert(1, "/var/www/u2608216/data/venv/lib/python3.9/site-packages")
os.environ["DJANGO_SETTINGS_MODULE"] = "danke.settings"

application = get_wsgi_application()
