from datetime import datetime
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError

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

def parse_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()

@app.route('/itineraries', methods=['POST'])
def create_itinerary():
    data = request.get_json()
    try:
        new_itinerary = Itinerary(
            destination=data['destination'],
            start_date=parse_date(data['start_date']),
            end_date=parse_date(data['end_date'])
        )
        db.session.add(new_itinerary)
        db.session.commit()
    except KeyError as e:
        return jsonify({"error": f"Missing field in request: {e}"}), 400
    except (ValueError, SQLAlchemyError) as e:
        return jsonify({"error": str(e)}), 400 if isinstance(e, ValueError) else 500

    return jsonify({"message": "Itinerary created successfully"}), 201

@app.route('/itineraries', methods=['GET'])
def get_itineraries():
    query_params = request.args
    query = Itinerary.query

    if destination_query := query_params.get('destination'):
        query = query.filter(Itinerary.destination.ilike(f'%{destination_query}%'))
    
    if start_date_query := query_params.get('start_date') and end_date_query := query_params.get('end_date'):
        try:
            query = query.filter(
                Itinerary.start_date >= parse_date(start_date_query), 
                Itinerary.end_date <= parse_date(end_date_query)
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    try:
        itineraries = query.options(load_only("id", "destination", "start_date", "end_date")).all()
    except SQLAlchemyError:
        return jsonify({"error": "Database error occurred"}), 500

    return jsonify([
        {
            "id": itinerary.id, 
            "destination": itinerary.destination,
            "start_date": str(itinerary.start_date), 
            "end_date": str(itinerary.end_date)
        } for itinerary in itineraries
    ])

@app.route('/itineraries/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            "id": itinerary.id,
            "destination": itinerary.destination,
            "start_date": str(itinerary.start_date),
            "end_date": str(itinerary.end_date)
        })

    if request.method == 'PUT':
        try:
            data = request.get_json()
            itinerary.destination = data['destination']
            itinerary.start_date = parse_date(data['start_date'])
            itinerary.end_date = parse_date(data['end_date'])
            db.session.commit()
            return jsonify({"message": "Itinerary updated successfully"})
        except KeyError as e:
            return jsonify({"error": f"Missing field in request: {e}"}), 400
        except (ValueError, SQLAlchemyError) as e:
            return jsonify({"error": str(e)}), 400 if isinstance(e, ValueError) else 500

    if request.method == 'DELETE':
        try:
            db.session.delete(itinerary)
            db.session.commit()
            return jsonify({"message": "Itinerary deleted successfully"})
        except SQLAlchemyError:
            return jsonify({"error": "Database error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)