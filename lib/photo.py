import urllib
import requests, json
from lib.key import (
    channel_secret, channel_access_token, google_photo_album_id,
    google_photo_client_id, google_photo_client_secret,
    google_photo_refresh_token
)

def get_photo_data(msg_id):
    # LINE から画像を取得
    url = 'https://api.line.me/v2/bot/message/'  + msg_id + '/content'
    headers = {
        "Content-Type" : "application/json; charset=UTF-8",
        'Authorization': 'Bearer ' + channel_access_token,
    }
    request = urllib.request.Request(url,
                                     method='GET',
                                     headers=headers)
    img_data = None
    with urllib.request.urlopen(request) as response:
        img_data = response.read()

    return img_data


def get_gphoto_access_token():
    # google photo アクセストークンを取得 with リフレッシュトークン
    data = [
      ('refresh_token', google_photo_refresh_token),
      ('client_id', google_photo_client_id),
      ('client_secret', google_photo_client_secret),
      ('grant_type', 'refresh_token'),
    ]

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
    res_data = response.json()
    google_photo_access_token = res_data['access_token']
    return google_photo_access_token

def get_gphoto_upload_token(gphoto_access_token, img_data, user_name):
    # GOOGLE PHOTOにアップロード
    # ヘッダ
    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    method = 'POST'
    headers = {
        'Authorization': 'Bearer ' + gphoto_access_token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': user_name.encode('utf-8'),
        'X-Goog-Upload-Protocol': 'raw',
    }
    body = img_data
    request = urllib.request.Request(url,
                                     data=body,
                                     method=method,
                                     headers=headers)
    upload_token = None
    # アップロードトークンを取得
    with urllib.request.urlopen(request) as response:
        upload_token = response.read().decode("utf-8")

    return upload_token

def upload_photo(gphoto_access_token, upload_token):
    # ライブラリに画像を追加
    if upload_token is not None:
        # 自分のライブラリに追加する
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
        headers = {
            'Authorization': 'Bearer ' + gphoto_access_token,
            'Content-type': 'application/json',
        }
        body = {
            "albumId": google_photo_album_id,
            "newMediaItems": [{"simpleMediaItem": {"uploadToken": upload_token}}]
        }
        method = 'POST'
        request = urllib.request.Request(url,
                                         data=json.dumps(body).encode('utf-8'),
                                         method=method,
                                         headers=headers)
        # アップロードトークンを取得
        with urllib.request.urlopen(request) as response:
            response = response.read().decode("utf-8")
