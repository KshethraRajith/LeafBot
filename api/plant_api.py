from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin
import os
from werkzeug.utils import secure_filename
from models.plant_model import PlantModel
from models.plant_ai import PlantAI

plant_bp = Blueprint('plant', __name__)
plant_model = PlantModel()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@plant_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@plant_bp.route('/verify', methods=['POST'])
def verify_plant():
    print("Verify plant")
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    print(f"File: {file.filename}")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        print(f"Filepath: {filepath}")
        #result = plant_model.verify_plant(filepath)
        image_details= PlantAI.get_image_details(filepath)

        return jsonify(image_details)
    
    return jsonify({'error': 'Invalid file type'}), 400

@plant_bp.route('/search', methods=['GET'])
def search_plant():

    if request.method == 'GET':
        print("Search plant")
        
        plant_name = request.args.get('name', '')
        print(f"Plant name: {plant_name}")  

        if not plant_name:
            return jsonify({'error': 'No search term provided'}), 400
        
        results = plant_model.search_plant(plant_name)
        response = make_response(jsonify(results))
        print(f"Search results to Frontend")

        return response