from flask import Blueprint, request, jsonify
from .itinerary_controller import (create_itinerary, update_itinerary, delete_itinerary, get_itinerary,
                                   add_place_to_itinerary, update_place_in_itinerary, delete_place_from_itinerary,
                                   get_places_in_itinerary, recommend_places_for_itinerary)

itinerary_bp = Blueprint('itinerary_bp', __name__)

@itinerary_bp.route('/itinerary/<int:itinerary_id>/places', methods=['POST'])
def add_place(itinerary_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        result = add_place_to_itinerary(itinerary_id, data)
        if not result:
            return jsonify({'error': 'Failed to add place to itinerary'}), 500
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>/places/<int:place_id>', methods=['PUT'])
def modify_place(itinerary_id, place_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        result = update_place_in_itinerary(itinerary_id, place_id, data)
        if result is None:
            return jsonify({'error': 'Place not found or update failed'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>/places/<int:place_id>', methods=['DELETE'])
def remove_place(itinerary_id, place_id):
    try:
        result = delete_place_from_itinerary(itinerary_id, place_id)
        if not result:
            return jsonify({'error': 'Place not found or delete failed'}), 404
        return jsonify({'success': True}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>/places', methods=['GET'])
def show_places(itinerary_id):
    try:
        result = get_places_in_itinerary(itinerary_id)
        if not result:
            return jsonify({'error': 'No places found for this itinerary'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itinerary_bp.route('/itinerary/<int:itinerary_id>/recommendations', methods=['GET'])
def recommend_places(itinerary_id):
    try:
        recommendations = recommend_places_for_itinerary(itinerary_id)
        if not recommendations:
            return jsonify({'error': 'No recommendations available'}), 404
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500