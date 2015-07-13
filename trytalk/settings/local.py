from default import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

# Using SpatialLite backend
DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'trytalk',
		'USER': 'test',
		'PASSWORD': 'test',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	 }
}

# settings for request application
REQUEST_IGNORE_PATHS = (
	r'^admin/',
)
REQUEST_ONLY_ERRORS = True
REQUEST_HEAD_FIELDS = [
	'HTTP_AUTHORIZATION',
	'CONTENT_TYPE',
]