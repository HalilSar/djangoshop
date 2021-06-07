from commerce.settings.base import *

DEBUG = True
from pathlib import Path
import os
ALLOWED_HOSTS = []
DATABASES = {
    'default': {                      
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresl37',
        'USER': 'postgres',
        'PASSWORD': 'covboybebop123',
        'HOST':'localhost',
        'PORT':'5432'
    }
}


STATIC_ROOT =os.path.join(BASE_DIR ,"staticfiles")
STATICFILES_DIRS = [
   os.path.join(BASE_DIR ,"static")
]

# smtp mail
# Çünkü viewde metod olarak kullandık
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'mailadress' 
# EMAIL_HOST_PASSWORD = 'mailpasswore'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# ACCOUNT_EMAIL_VERIFICATION = ""
# Redis Kullanımı
CELERY_BROKER_URL = 'redis://localhost:6379'