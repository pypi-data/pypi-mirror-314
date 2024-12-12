import django

author = 'ayhan'
version = "1.0.10"

if django.VERSION < (3, 2):
    default_app_config = "bigcode.apps.bigcodeConfig"


