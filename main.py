# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import tempfile
import requests, json
from io import BytesIO
from argparse import ArgumentParser
import urllib.request

from flask import Flask, request, abort, g
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
# load .env
from lib.key import (
    channel_secret, channel_access_token, google_photo_album_id,
    google_photo_client_id, google_photo_client_secret,
    google_photo_refresh_token, sqlalchemy_database_uri
)
from lib import const
from lib import photo
from lib.database import (
    db, User, add_user_to_database, get_user_counter, update_user_counter
)
from lib.messaging import (
    message_for_posting_a_photo
)
from lib.errors import (
    PhotoPostLimitationError
)

app = Flask(__name__)
# set up dataset
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
db.init_app(app)

# line bot api
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        app.logger.debug('This is debug message')
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


""" テキストメッセージが送られた場合
"""
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    text = event.message.text # 受信したメッセージ

    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Display name: ' + profile.display_name)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
    elif text == 'あいいい':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='あいいいいいいいい'))


""" BOTと友達になったとき
"""
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    # DBにユーザー情報が未登録のとき, データベースにユーザー追加
    user = User.query.get(user_id) # ユーザーがDBに存在するか
    if user is None:
        profile = line_bot_api.get_profile(user_id)
        add_user_to_database(user_id, profile.display_name, 0)


""" 画像が送られた場合
"""
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    display_name = 'None'
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        user_id = event.source.user_id
        display_name = profile.display_name

    # ユーザーのこれまでの投稿枚数を取得
    counter = get_user_counter(user_id, display_name)
    try:

        # 写真の投稿枚数の上限を超えている場合
        if counter >= const.PHOTO_POST_LIMIT:
            counter += 1
            raise PhotoPostLimitationError

        """ 画像をGooglePhotoへアップロード [ここから] """
        # LINEサーバーから画像取得
        try: img_data = photo.get_photo_data(msg_id=event.message.id)
        except: raise ValueError('LINEサーバーから画像の取得に失敗')

        # Google Photoのアクセストークンを取得
        try: gphoto_access_token = photo.get_gphoto_access_token()
        except: raise ValueError('Google Photoのアクセストークンを取得に失敗')

        # Google Photoへ画像をアップロード
        try: upload_token = photo.get_gphoto_upload_token(gphoto_access_token, img_data, display_name + '_' + str(counter+1))
        except: raise ValueError('Google Photoへ画像をアップロードに失敗')

        # 画像をGoogle Photoアルバムに追加
        try: photo.upload_photo(gphoto_access_token, upload_token)
        except: raise ValueError('画像をGoogle Photoアルバムに追加に失敗')
        """ 画像をGooglePhotoへアップロード [ここまで] """

        # カウンター(DB)をアップデート
        counter = update_user_counter(user_id, display_name)
        # カウンターによってメッセージを変更
        msg = message_for_posting_a_photo(display_name, counter)

    # 写真の投稿上限を超えている
    except PhotoPostLimitationError:
        msg = message_for_posting_a_photo(display_name, counter)
    # それ以外のエラー
    except:
        msg = const.UPLOAD_FAILED_MESSAGE

    # メッセージを返却
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


""" スタンプが送られた場合
"""
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id=event.message.package_id,
                sticker_id=event.message.sticker_id)
        )
    except:
        print ('このスタンプ持ってない')


""" 位置情報が送られた場合
"""
# @handler.add(MessageEvent, message=LocationMessage)
# def handle_location_message(event):
#     try:
#         line_bot_api.reply_message(
#             event.reply_token,
#             LocationSendMessage(
#                 title=event.message.title, address=event.message.address,
#                 latitude=event.message.latitude, longitude=event.message.longitude
#             )
#         )
#     except:
#         print ('位置情報のエラー')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
