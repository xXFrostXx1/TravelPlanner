from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)

@app.route('/itineraries', methods=['GET', 'POST'])
def manage_itineraries():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400
        data = request.get_json()
        return jsonify({"message": "Itinerary added", "data": data}), 201
    else:
        return jsonify({"message": "Itineraries fetched"}), 200

@app.route('/itineraries/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def itinerary_detail(id):
    if request.method == 'GET':
        return jsonify({"message": "Itinerary detail"}), 200
    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400
        data = request.get_json()
        return jsonify({"message": "Itinerary updated", "data": data}), 200
    else:
        return jsonify({"message": "Itinerary deleted"}), 204

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000))