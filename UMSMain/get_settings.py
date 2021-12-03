import importlib
import os


settings = importlib.import_module(os.environ.get('DJANGO_SETTINGS_MODULE'))
