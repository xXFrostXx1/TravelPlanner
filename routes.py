from flask import Response, stream_with_context, jsonify
import json

@itinerary_bp.route('/itinerary/<int:itinerary_id>/places', methods=['GET'])
def show_places(itinerary_id):
    try:
        def generate_places():
            for place in get_places_in_itinerary_generator(itinerary_id):  # Assume this is a generator
                yield json.dumps(place) + '\n'
        return Response(stream_with_context(generate_places()), content_type='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500