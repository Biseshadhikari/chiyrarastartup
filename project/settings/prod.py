from .base import *
import os 
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR/"static"]
STATIC_ROOT= '/home7/ngsaahco/chiyarastartup.com/static/'


MEDIA_ROOT = '/home7/ngsaahco/chiyarastartup.com/media/'
MEDIA_URL = '/media/'