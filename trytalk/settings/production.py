from default import *

import os

# Using SpatialLite backend
DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'trytalk',
		'USER': os.environ.get('DATABASE_USER'),
		'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
		'HOST': '127.0.0.1',
		'PORT': '5432',
	 }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

SERVER_EMAIL = 'django@trytalk'
ADMINS = (
	('Eric', 'eric@bravebot.com'),
)

# settings for request application
# REQUEST_IGNORE_PATHS = (
# 	r'^admin/',
# )
REQUEST_ONLY_ERRORS = True
REQUEST_HEAD_FIELDS = [
	'HTTP_AUTHORIZATION',
	'CONTENT_TYPE',
]
