from default import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

# Using SpatialLite backend
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# For GeoDjango to be able to find the SpatiaLite library
SPATIALITE_LIBRARY_PATH='/usr/local/lib/mod_spatialite.dylib'