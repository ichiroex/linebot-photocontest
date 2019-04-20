# -*- coding: utf-8 -*-
""" メッセージ管理用
"""

from lib import const

def message_for_posting_a_photo(display_name, counter):
    msg = ''
    # 残り枚数のメッセージ
    thank_you_msg = '{}さん、{}\n{}枚目の投稿ですね。残り{}枚の写真を投稿できます！'.format(
        display_name,
        const.THANK_YOU_MESSAGE,
        counter,
        const.PHOTO_POST_LIMIT - counter)
    last_thank_you_msg = '{}さん、{}\n最後の5枚目の投稿ですね！ご参加いただきありがとうございました(^^)'.format(
        display_name,
        const.THANK_YOU_MESSAGE)
    stop_msg = '{}さん、{}\nしかし、どうやら既に5枚の写真が投稿されているようです... ごめんなさい。'.format(
        display_name,
        const.THANK_YOU_MESSAGE)

    # 投稿枚数によってメッセージを変える
    if counter < const.PHOTO_POST_LIMIT:
        msg = thank_you_msg
    elif counter == const.PHOTO_POST_LIMIT:
        msg = last_thank_you_msg
    else:
        msg = stop_msg

    return msg
