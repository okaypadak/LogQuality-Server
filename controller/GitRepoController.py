from flask import Blueprint, request, jsonify

get_route = Blueprint('get_route', __name__)

@get_route.route('/')
def get_method():
    return "Hello, this is the GET method!"

post_route = Blueprint('post_route', __name__)

@post_route.route('/post', methods=['POST'])
def post_method():
    data = request.json
    if "proje_adi" in data:
        proje_adi = data["proje_adi"]

        return jsonify({"success": True, "message": f"Proje adı alındı: {proje_adi}"})
    else:
        return jsonify({"success": False, "message": "Proje adı bulunamadı."})