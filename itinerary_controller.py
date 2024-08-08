from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from os import environ
from dotenv import load_dotenv
from datetime import datetime

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
                              start_date=datetime.strptime(data['start_date'], "%Y-%m-%d").date(),
                              end_date=datetime.strptime(data['end_date'], "%Y-%m-%d").date())
    db.session.add(new_itinerary)
    db.session.commit()

    return jsonify({"message": "Itinerary created successfully"}), 201

@app.route('/itineraries', methods=['GET'])
def get_itineraries():
    query_params = request.args
    destination_query = query_params.get('destination')
    start_date_query = query_params.get('start_date')
    end_date_query = query_params.get('end_date')
    
    query = Itinerary.query
    
    if destination_query:
        query = query.filter(Itinerary.destination.ilike(f'%{destination_query}%'))
    if start_date_query and end_date_query:
        query = query.filter(and_(Itinerary.start_date >= datetime.strptime(start_date_query, "%Y-%m-%d").date(), Itinerary.end_date <= datetime.strptime(end_date_query, "%Y-%m-%d").date()))
    
    itineraries = query.all()
    
    return jsonify([{"id": itinerary.id, "destination": itinerary.destination,
                     "start_date": str(itinerary.start_date), "end_date": str(itinerary.end_date)} for itinerary in itineraries])

@app.route('/itineraries/<int:id>', methods=['GET'])
def get_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    return jsonify({"id": itinerary.id, "destination": itinerary.destination,
                    "start_date": str(itinerary.start_date), "end_date": str(itinerary.end_date)})

@app.route('/itineraries/<int:id>', methods=['PUT'])
def update_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    data = request.get_json()

    itinerary.destination = data['destination']
    itinerary.start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    itinerary.end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

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