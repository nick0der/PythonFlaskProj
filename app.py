from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util, ObjectId

import bson
import pymongo
import json

connection_str = "mongodb+srv://admin:admin@cluster0.aqrf4.mongodb.net/myFirstDatabase?ssl=true&ssl_cert_reqs=CERT_NONE"
cluster = MongoClient(connection_str)

db = cluster["CarDealership"]
collection = db["cars"]

app = Flask(__name__)

#ADD
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

#GET ALL
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

#GET BY ID
@app.route("/cars/<id>", methods=["GET"])
def get_car(id):

    if not bson.objectid.ObjectId.is_valid(id):
        return jsonify({
            'message' : "'id' format is incorrect"
        })

    car = collection.find_one({'_id': ObjectId(id)})

    if car is None:
        return jsonify({
            'message' : 'Record does not exist in the database'
        })

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

#UPDATE
@app.route("/cars/<id>", methods=["PUT"])
def update_car(id):

    #Check if 'id' is correct
    if not bson.objectid.ObjectId.is_valid(id):
        return jsonify({
            'message' : "'id' format is incorrect"
        })

    #Check if object exists
    if collection.find_one({'_id': ObjectId(id)}) is None:
        return jsonify({
            'message' : 'Record does not exist in the database'
        })
    
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
    return jsonify({
            'message' : 'Successfully updated'
        })

#DELETE
@app.route("/cars/<id>", methods=["DELETE"])
def delete_car(id):

    #Check if 'id' is correct
    if not bson.objectid.ObjectId.is_valid(id):
        return jsonify({
            'message' : "'id' format is incorrect"
        })

    #Check if object exists
    if collection.find_one({'_id': ObjectId(id)}) is None:
        return jsonify({
            'message' : 'Record does not exist in the database'
        })
    
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({
            'message' : 'Successfully deleted'
    })

