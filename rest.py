from flask import Flask, jsonify, request

app = Flask(__name__)

data = {'name': 'John', 'age': 30}

@app.route('/get_data', methods=['GET'])
def get_data():
    key = request.args.get('key')
    default_value = request.args.get('default', None)

    result = data.get(key, default_value)

    return jsonify({'result': result})

