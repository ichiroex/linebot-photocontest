import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

############################################################################
# LINE API_KEYを設定
############################################################################
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.environ.get('LINE_CHANNEL_SECRET', None)
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)
google_photo_client_id = os.environ.get('GOOGLE_PHOTO_CLIENT_ID', None)
google_photo_client_secret = os.environ.get('GOOGLE_PHOTO_CLIENT_SECRET', None)
google_photo_album_id = os.environ.get('GOOGLE_PHOTO_ALBUM_ID', None)
google_photo_refresh_token = os.environ.get('GOOGLE_PHOTO_REFRESH_TOKEN', None)
sqlalchemy_database_uri = os.environ.get('DATABASE_URI', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if google_photo_client_id is None:
    print('Specify GOOGLE_PHOTO_CLIENT_ID as environment variable.')
    sys.exit(1)
if google_photo_client_secret is None:
    print('Specify GOOGLE_PHOTO_CLIENT_SECRET as environment variable.')
    sys.exit(1)
if google_photo_album_id is None:
    print('Specify GOOGLE_PHOTO_ALBUM_ID as environment variable.')
    sys.exit(1)
if google_photo_refresh_token is None:
    print('Specify GOOGLE_PHOTO_REFRESH_TOKEN as environment variable.')
    sys.exit(1)
if sqlalchemy_database_uri is None:
    print('Specify SQLALCHEMY_DATABASE_URI as environment variable.')
    sys.exit(1)
