from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS += ['silk']

MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

INTERNAL_IPS = ['127.0.0.1']

SILKY_PYTHON_PROFILER = True
SILKY_ANALYZE_QUERIES = True
