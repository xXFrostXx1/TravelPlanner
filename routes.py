from flask import Blueprint, request, jsonify
from .itinerary_controller import create_itinerary, update_itinerary, delete_itinerary, get_itinerary

itinerary_bp = Blueprint('itinerary_bp', __name__)

@itinerary_bp.route('/itinerary', methods=['POST'])
def add_itinerary():
    data = request.get_json()
    result = create_itinerary(data)
    return jsonify(result), 201

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['PUT'])
def modify_itinerary(itinerary_id):
    data = request.get_json()
    result = update_itinerary(itinerary_id, data)
    return jsonify(result), 200

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['DELETE'])
def remove_itinerary(itinerary_id):
    result = delete_itinerary(itinerary_id)
    return jsonify(result), 204

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['GET'])
def show_itinerary(itinerary_id):
    result = get_itinerary(itinerary_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Itinerary not found'}), 404