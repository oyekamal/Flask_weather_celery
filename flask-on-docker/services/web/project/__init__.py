from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .weather_request import get_weather_by_city
import json
from flask_apscheduler import APScheduler
scheduler = APScheduler()


engine = create_engine(
    'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev',
    echo=True
)
# postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.config.from_object('project.config.Config')

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
        fields = ('city', 'active')

def scheduleTask():
    cities = session.query(Subscription.city).distinct().all()
    print(cities)
    for each_city in cities:
        print(each_city[0])
        data  = get_weather_by_city(each_city[0])
        with open(f"./weather_json/{each_city[0]}.json", "w") as outfile:
            json.dump(data, outfile)
        main = data.get('main')
        if main:
            if main['temp'] < 300:
                with open(f"./email_folder/{each_city[0]}.txt", 'w') as f:
                    text = f"send mail to {each_city[0]} with temperature {main['temp']}"
                    f.write(text)
            
    print("This test runs every 30 seconds")

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