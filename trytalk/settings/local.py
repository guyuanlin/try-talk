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

# mobile_notifications settings
APNS_USE_SANDBOX = False
APNS_CERT_PEM = 'mobile_notifications/certificates/apns-production-cert.pem'
APNS_KEY_PEM = 'mobile_notifications/certificates/apns-production-key-noenc.pem'

# LOGGING CONFIGURATION
# A logging configuration that writes log messages to the console.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	# Formatting of messages.
	'formatters': {
		# Don't need to show the time when logging to console.
		'console': {
			'format': '%(levelname)s %(name)s.%(funcName)s (%(lineno)d) %(message)s'
		}
	},
	# The handlers decide what we should do with a logging message - do we email
	# it, ditch it, or write it to a file?
	'handlers': {
		# Writing to console. Use only in dev.
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'console'
		},
		# Send logs to /dev/null.
		'null': {
			'level': 'DEBUG',
			'class': 'django.utils.log.NullHandler',
		},
	},
	# Loggers decide what is logged.
	'loggers': {
		'': {
			# Default (suitable for dev) is to log to console.
			'handlers': ['console'],
			'level': 'INFO',
			'propagate': False,
		},
		# logging of SQL statements. Default is to ditch them (send them to
		# null). Note that this logger only works if DEBUG = True.
		'django.db.backends': {
			'handlers': ['null'],
			'level': 'DEBUG',
			'propagate': False,
		},
	}
}