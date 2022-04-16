from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://Jan_17026846:Jasiu995@uwe-azure.postgres.database.azure.com/lstm_data'
db = SQLAlchemy(app)


class LSTM(db.Model):
    __tablename__ = 'Feed'
    Month = db.Column(db.Date(), nullable=False)
    Total_Crimes = db.Column(db.Integer(), nullable=False)
    feed_id = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, Month, Total_Crimes, feed_id):
        self.Month = Month
        self.Total_Crimes = Total_Crimes
        self.feed_id = feed_id


@app.route('/feed', methods=['GET'])
def get_feed():
    all_feeds = LSTM.query.all()
    output = {"feed": []}
    for feed in all_feeds:
        current_feed = {}
        current_feed['Month'] = feed.Month
        current_feed['Total_Crimes'] = feed.Total_Crimes
        output['feed'].append(current_feed)
    return jsonify(output)


@app.route('/feed', methods=['POST'])
def post_feed():
    feed_data = request.get_json()
    feed = LSTM(Month=feed_data['Month'], Total_Crimes=feed_data['Total_Crimes'], feed_id=feed_data['feed_id'])
    db.session.add(feed)
    db.session.commit()
    return jsonify(feed_data)


if __name__ == '__main__':
    app.run()
