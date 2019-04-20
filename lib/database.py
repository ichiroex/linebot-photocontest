# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""MEMO
To create the initial database, just import the db object
from an interactive Python shell and run the SQLAlchemy.create_all() method
to create the tables and database:
>>> from yourapplication import db
>>> db.create_all()
"""
class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Text, primary_key=True, unique=True)
    display_name = db.Column(db.Text, unique=False)
    counter = db.Column(db.Integer, unique=False)

    def __init__(self, userid, display_name, counter):
        self.userid = userid
        self.display_name = display_name
        self.counter = counter

    def __repr__(self):
        return '<User %r>' % self.id


def add_user_to_database(user_id, display_name, counter):
    """ データベースにユーザ情報を追加する
    """
    # 追加
    add_user = User(user_id, display_name, counter) # userid, 表示名, カウンタ
    db.session.add(add_user)
    db.session.commit()


def get_user_counter(user_id, display_name):
    """ ユーザーが投稿した枚数を取得
    """
    # Getting user by primary key
    user = User.query.get(user_id) # ユーザーがDBに存在するか
    if user is None:
        add_user_to_database(user_id, display_name, 0) # DBに存在しない場合は追加
        user = User.query.get(user_id)

    return user.counter


def update_user_counter(user_id, display_name):
    """ 画像投稿数をカウントアップ
    """
    # Getting user by primary key
    user = User.query.get(user_id) # ユーザーがDBに存在するか
    # カウントアップ
    if user is not None:
        user.counter = user.counter + 1
        db.session.add(user)
        db.session.commit() # カウンタのアップデートをDBに反映
    else:
        add_user_to_database(user_id, display_name, 1) # DBに存在しない場合は追加
        user = User.query.get(user_id) # ユーザーがDBに存在するか

    return user.counter
