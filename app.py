from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util, ObjectId

import pymongo
import json

connection_str = "mongodb+srv://admin:admin@cluster0.aqrf4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
cluster = MongoClient(connection_str)

db = cluster["CarDealership"]
collection = db["cars"]

app = Flask(__name__)

@app.route("/cars", methods=["POST"])
def add_car():
    car = collection.insert_one({
        'model' : request.json['model'],
        'color' : request.json['color'],
        'horsepower' : request.json['horsepower'],
        'weight' : request.json['weight'],
        '1/4 mile time' : request.json['1/4 mile time'],
        'cylinders' : request.json['cylinders'],
        'transmission' : request.json['transmission'],
        'gears' : request.json['gears']
    })
    return get_car(str(car.inserted_id))

@app.route("/cars", methods=["GET"])
def get_cars():
    cars = []
    for car in list(collection.find({})):
        cars.append({
            '_id': str(ObjectId(car['_id'])),
            'model' : car['model'],
            'color' : car['color'],
            'horsepower' : car['horsepower'],
            'weight' : car['weight'],
            '1/4 mile time' : car['1/4 mile time'],
            'cylinders' : car['cylinders'],
            'transmission' : car['transmission'],
            'gears' : car['gears']
        })
    
    return jsonify(cars)

@app.route("/cars/<id>", methods=["GET"])
def get_car(id):
    car = collection.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(car['_id'])),
        'model' : car['model'],
        'color' : car['color'],
        'horsepower' : car['horsepower'],
        'weight' : car['weight'],
        '1/4 mile time' : car['1/4 mile time'],
        'cylinders' : car['cylinders'],
        'transmission' : car['transmission'],
        'gears' : car['gears']
    })

@app.route("/cars/<id>", methods=["PUT"])
def update_car(id):
    collection.update_one({'_id': ObjectId(id)}, {'$set':{
        'model': request.json['model'],
        'color' : request.json['color'],
        'horsepower' : request.json['horsepower'],
        'weight' : request.json['weight'],
        '1/4 mile time' : request.json['1/4 mile time'],
        'cylinders' : request.json['cylinders'],
        'transmission' : request.json['transmission'],
        'gears' : request.json['gears']
    }}) 
    return get_car(id)

@app.route("/cars/<id>", methods=["DELETE"])
def delete_car(id):
    to_delete = get_car(id)
    collection.delete_one({'_id': ObjectId(id)})
    return to_delete

