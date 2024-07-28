from flask import Blueprint, request, jsonify
from .itinerary_controller import create_itinerary, update_itinerary, delete_itinerary, get_itinerary

itinerary_bp = Blueprint('itinerary_bp', __name__)

@itinerary_bp.route('/itinerary', methods=['POST'])
def add_itinerary():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        result = create_itinerary(data)
        if not result:
            return jsonify({'error': 'Failed to create itinerary'}), 500
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['PUT'])
def modify_itinerary(itinerary_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        result = update_itinerary(itinerary_id, data)
        if result is None:  # Assuming None is returned when update fails
            return jsonify({'error': 'Itinerary not found or update failed'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['DELETE'])
def remove_itinerary(itinerary_id):
    try:
        result = delete_itinerary(itinerary_id)
        if not result:
            return jsonify({'error': 'Itinerary not found or delete failed'}), 404
        return jsonify(result), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>', methods=['GET'])
def show_itinerary(itinerary_id):
    try:
        result = get_itinerary(itinerary_id)
        if not result:
            return jsonify({'error': 'Itinerary not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500