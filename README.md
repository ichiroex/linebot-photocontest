# LINE Bot for Photo Contest

## Requirements
- python 3.6.6

## Getting started
```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN

$ pip install -r requirements.txt
```

## Usage
```
$ python main.py
```

## Deploy
```
# To github repository
$ git push origin master

# To heroku server
$ git push heroku master
```

## Google Photos APIの使い方
### AUTH CODEを取得する（ブラウザで開く）
```
$ CLIENT_ID=<認証情報の作成で作成した文字列>
$ CLIENT_SECRET=<認証情報の作成で作成した文字列>
$ REDIRECT_URI=urn:ietf:wg:oauth:2.0:oob
$ SCOPE=https://www.googleapis.com/auth/photoslibrary

# 下記URLへアクセス
$ echo "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URI&scope=$SCOPE&access_type=offline"
```

### 環境変数を設定
```
$ source ./set_envs_local.sh
```

### アクセストークンを取得
```
# REFRESH_TOKENとACCESS_TOKENをメモする
$ AUTH_CODE=<ブラウザアクセスで取得した認証コード>
$ curl -s --data "code=$AUTH_CODE" --data "client_id=$CLIENT_ID" --data "client_secret=$CLIENT_SECRET" --data "redirect_uri=$REDIRECT_URI" --data "grant_type=authorization_code" --data "access_type=offline" https://www.googleapis.com/oauth2/v4/token
{
 "access_token": "***",
 "token_type": "Bearer",
 "expires_in": 3600,
 "refresh_token": "***"
}


# REFRESH_TOKEN取得後のACCESS_TOKEN取得方法
$ curl --data "grant_type=refresh_token" --data "client_id=$CLIENT_ID" --data "client_secret=$CLIENT_SECRET" --data "refresh_token=$REFRESH_TOKEN" https://www.googleapis.com/oauth2/v4/token
{
  "access_token": "***",
  "expires_in": 3600,
  "scope": "https://www.googleapis.com/auth/photoslibrary",
  "token_type": "Bearer"
}
```

### アルバムIDを取得
```
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" 'https://photoslibrary.googleapis.com/v1/albums'
```

### get image binary from line messaging api (LINE Messaging API)
```
curl -X GET -v -H 'Content-Type: application/json; charset=UTF-8' -H 'Authorization: Bearer YOUR_LINE_CHANNEL_ACCESS_TOKEN' https://api.line.me/v2/bot/message/LINE_MESSAGE_ID/content
```

### upload a photo
```
curl -v --data '{"newMediaItems":[{"simpleMediaItem":{"uploadToken":"YOUR_UOLOAD_TOKEN"}}]}' -H 'Content-type: application/json' -H 'Authorization: Bearer YOUT_ACCESS_TOKEN' "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"
```

### create photo album (optional)
```
$ curl -X POST -v --data '{"album": {"title": "TITLE_OF_ALBUM"}}' -H 'Content-type: application/json' -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' https://photoslibrary.googleapis.com/v1/albums
```
