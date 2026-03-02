"""Production settings: debug off, use env for SECRET_KEY and ALLOWED_HOSTS."""
from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False
