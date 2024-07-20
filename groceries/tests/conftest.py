import pytest
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': settings.DB_HOST,
        'NAME': settings.TEST_DB_NAME,
        'USER': settings.DB_USER,
        'PASSWORD': settings.DB_PASSWORD,
        'PORT': settings.DB_PORT,
    }