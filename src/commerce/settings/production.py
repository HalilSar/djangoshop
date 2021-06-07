from commerce.settings.base import *
import os
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['halil-deploy27.herokuapp.com','127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES['default'] = dj_database_url.parse('postgres://snfvsfuuefmhee:ad7f2542f3c0aef7fe07ee011719e1444c468bda40e155bcc60990da85da241e@ec2-18-215-111-67.compute-1.amazonaws.com:5432/dgkabr41tlt0d', conn_max_age=600)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]
