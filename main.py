from flask import Flask, request, jsonify
from pymongo import MongoClient
from data import *
from forms import *

app = Flask(__name__)
collection = MongoClient(MONGO_HOST, 27017)[DATABASE][COLLECTION]

@app.route('/', methods=['POST'])
def handle_post():
    data = request.json
    forms = list(collection.find({}, {"_id": 0}))
    data_types = determine_types(data)
    form_template = get_correct_form(forms, data)
    if not form_template:
        return jsonify(data_types)
    for key in list(form_template.keys())[1:]:
        if form_template[key] != data_types[key]:
            return jsonify(data_types)
    return form_template['name']



if __name__ == '__main__':
    app.run(debug=True, port=8000, host=HOST)