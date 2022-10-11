from .base import *


ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = "django-insecure-wxo4b14j=hq6e8jw&s(^x6-rb(m#)oy$9ckn=b%!nnbyvh)9r8"
DEBUG = False

try:
    from .local import *
except ImportError:
    pass
