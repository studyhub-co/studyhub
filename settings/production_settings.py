import os
# import raven


DEBUG = False

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [x for x in env_hosts.split(',') if x]

# ALLOWED_HOSTS = [
#     'physicsisbeautiful.com',
#     'www.physicsisbeautiful.com',
#     'dev.physicsisbeautiful.com',
#     # 'pib-dev.us-east-1.elasticbeanstalk.com',
#     'pib-dev-v2.us-east-1.elasticbeanstalk.com',
#     '.compute-1.amazonaws.com',
# ]


# add ip to allow ebs health checker to work
import socket
ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))

CORS_ORIGIN_WHITELIST = (
    # allow mobile app to access apis
    'localhost:8080',
)

from .common_settings import *  # noqa: E402, F401

EMAIL_BACKEND = 'django_ses.SESBackend'

# django-s3-storage
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = AWS_REGION
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
AWS_S3_BUCKET_AUTH = False

# django-s3-storage media
AWS_S3_PUBLIC_URL = os.getenv('AWS_S3_PUBLIC_URL')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

# django-s3-storage static
AWS_S3_BUCKET_NAME_STATIC = os.getenv('AWS_S3_BUCKET_NAME_STATIC')
AWS_S3_PUBLIC_URL_STATIC = os.getenv('AWS_S3_PUBLIC_URL_STATIC')

DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

# depicated
# RAVEN_CONFIG = {
#     'dsn': os.getenv('RAVEN_DSN'),
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = bool(os.getenv('SESSION_COOKIE_SECURE', True))
CSRF_COOKIE_SECURE = bool(os.getenv('CSRF_COOKIE_SECURE', True))

# enable for logging to a file in production
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/var/app/current/djangodebug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }

