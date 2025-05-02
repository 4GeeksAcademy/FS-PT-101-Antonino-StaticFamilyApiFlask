"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete(id):
    result = jackson_family.delete_member(id)
    if result:
        return jsonify({"message": f"Miembro con id {id} eliminado"}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404

@app.route('/members/<int:id>', methods=['GET'])
def handle_get(id):
    result = jackson_family.get_member(id)
    if result:
        return jsonify({"message": f"Miembro con id {id} : {result}"}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404
    
@app.route('/members/<int:id>', methods=['PUT'])
def handle_put(id):
    data = request.json  # Extraer datos del cuerpo de la solicitud
    name = data.get("first_name")
    age = data.get("age")
    numbers = data.get("lucky_numbers")

    result = jackson_family.edit_member(id, name, age, numbers)
    
    if result:
        return jsonify({"message": f"Miembro con id {id} actualizado"}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404

@app.route('/members', methods=['POST'])
def new_member():
    data = request.json
    new = jackson_family.add_member(data)
    response_body = {"success": True,
                     "family": new}
    return jsonify(response_body), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
