from flask import Flask, request, jsonify
from pymongo import MongoClient
from data import *
from forms import *

app = Flask(__name__)
# Получаем объект коллекции с данными форм.
collection = MongoClient(MONGO_HOST, 27017)[DATABASE][COLLECTION]

@app.route('/', methods=['POST'])
def handle_post():
    data = request.json # получаем данные, пришедшие от пользователя
    forms = list(collection.find({}, {"_id": 0})) # получаем данные форм из базы данных
    data_types = determine_types(data) # генерируем словарь из данных пользователя, где ставим соответствие (имя поля): (тип поля)
    form_template = get_correct_form(forms, data) # получаем форму, которая по названиям соответствует пришедшим от пользователя данным
    if not form_template:
        return jsonify(data_types) # возвращаем типы данных, пришедших от пользователя в случае отсутствия подходящей формы в базе данных.
    # проводим проверку, соответствуют ли типы данных пользователя типам, которые указаны для отобранной нами формы.
    for key in list(form_template.keys())[1:]:
        if form_template[key] != data_types[key]:
            return jsonify(data_types) # возвращаем типы данных, пришедших от пользователя в случае отсутствия подходящей формы в базе данных.
    return form_template['name'] # возвращаем имя формы



if __name__ == '__main__':
    app.run(debug=True, port=8000, host=HOST)