# -*- coding: utf-8 -*-

class PhotoPostLimitationError (Exception):
    """
    写真の投稿枚数が上限を超えたときのエラー
    """
    def __str__ (self):
        return "PhotoPostLimitationError"
