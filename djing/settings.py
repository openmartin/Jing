# Django settings for astro_render project.
import os
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
PARRENT_PATH = os.path.abspath(os.path.join(CURRENT_PATH,".."))

#PATH DEFINE
SWE_DATAFILE_PATH = os.path.join(PARRENT_PATH, 'data_file')

NATAL_TEMPLATE_PATH = os.path.join(PARRENT_PATH, 'html','templates', 'natal.xml')

TRANSIT_TEMPLATE_PATH = os.path.join(PARRENT_PATH, 'html', 'templates', 'transit.xml')

SVG_SYMBOL_PATH = os.path.join(PARRENT_PATH, 'html', 'templates', 'svg_symbol.xml')

WEBKIT_RESOURCE_PATH = os.path.join(PARRENT_PATH, 'html')


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(EXAMPLE_PATH, 'test.db'),
        'NAME': 'jing.sqlite3',
    }
}

SECRET_KEY = 'hgiozz5fwmun^gk9^m*49g8_(8^#1fiat1#koy+@s&dh$)1t#@'

ROOT_URLCONF = 'djing.urls'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Template
TEMPLATE_DIRS = (os.path.join(PARRENT_PATH,'html', 'templates'),)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
	'djing'
)

# Add by Author
DATE_FORMAT = 'Y-m-d'