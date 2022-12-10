from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config.from_object("project.config.Config")
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