from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
  
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"<Itinerary {self.destination}>"

@app.route('/itineraries', methods=['POST'])
def create_itinerary():
    data = request.get_json()

    new_itinerary = Itinerary(destination=data['destination'],
                              start_date=data['start_date'],
                              end_date=data['end_date'])
    db.session.add(new_itinerary)
    db.session.commit()

    return jsonify({"message": "Itinerary created successfully"}), 201

@app.route('/itineraries', methods=['GET'])
def get_itineraries():
    itineraries = Itinerary.query.all()
    return jsonify([{"id": itinerary.id, "destination": itinerary.destination,
                     "start_date": itinerary.start_date, "end_date": itinerary.end_date} for itinerary in itineraries])

@app.route('/itineraries/<int:id>', methods=['GET'])
def get_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    return jsonify({"id": itinerary.id, "destination": itinerary.destination,
                    "start_date": itinerary.start_date, "end_date": itinerary.end_date})

@app.route('/itineraries/<int:id>', methods=['PUT'])
def update_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    data = request.get_json()

    itinerary.destination = data['destination']
    itinerary.start_date = data['start_date']
    itinerary.end_date = data['end_date']

    db.session.commit()

    return jsonify({"message": "Itinerary updated successfully"})

@app.route('/itineraries/<int:id>', methods=['DELETE'])
def delete_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    db.session.delete(itinerary)
    db.session.commit()

    return jsonify({"message": "Itinerary deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)