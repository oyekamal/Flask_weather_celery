from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from celery import Celery


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


app = Flask(__name__)
app.config.from_object(Config)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

ma = Marshmallow(app)
db = SQLAlchemy(app)

class Subscription(db.Model):
    __tablename__ = "subscription"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, city):
        self.city = city

class SubscriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription
        fields = ('city', 'active')


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route('/api/sub/', methods=['Post'])
def subs_create():
    city = request.json['city']
    sub = Subscription(city)
    sub_schema = SubscriptionSchema()
    db.session.add(sub)
    db.session.commit()
    return jsonify(sub_schema.dump(sub))


@app.route('/api/sub/', methods=['GET'])
def subs():
    sub = Subscription.query.filter()
    subs_schema=SubscriptionSchema(many=True)
    return jsonify(subs_schema.dump(sub))


@app.route('/api/sub/<int:sub_id>/', methods=['GET'])
def sub_detail(sub_id):
    note = Subscription.query.get(sub_id)
    sub_schema=SubscriptionSchema()
    return sub_schema.jsonify(note)


@app.route('/api/sub/<int:sub_id>/', methods=['PATCH'])
def update_note(sub_id):
    sub = Subscription.query.get(sub_id)
    sub_schema=SubscriptionSchema()
    city = request.json.get("city")
    sub.city = city
    db.session.add(sub)
    db.session.commit()
    return sub_schema.jsonify(sub)


@app.route('/api/sub/<int:sub_id>/', methods=['DELETE'])
def delete_note(sub_id):
    sub = Subscription.query.get(sub_id)
    sub_schema=SubscriptionSchema()
    db.session.delete(sub)
    db.session.commit()
    return sub_schema.jsonify(sub)