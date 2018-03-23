
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request
import pymongo

app = Flask(__name__)



#app.config['MONGO_DBNAME'] = 'databasename'
#app.config['MONGO_URI'] = 'mongodb://username:password@hostname:port/databasename'

connectionString = "mongodb://FirstUser:test@cluster0-shard-00-00-59jwa.mongodb.net:27017," \
                   "cluster0-shard-00-01-59jwa.mongodb.net:27017,cluster0-shard-00-02-59jwa.mongodb.net:" \
                   "27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

mongo = pymongo.MongoClient(connectionString)
@app.route('/')
def hi():
    return 'hi'
#mongo = PyMongo(app)

@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    framework = mongo.repos.clean_repo

    output = []

    for q in framework.find():
        output.append({'name' : q['name'], 'id' : q['id']})

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.repos.clean_repo

    q = framework.find_one({'name' : name})

    if q:
        output = {'name' : q['name'], 'id' : q['id']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/framework', methods=['POST'])
def add_framework():
    framework = mongo.repos.clean_repo

    name = request.json['name']
    language = request.json['language']

    framework_id = framework.insert({'name' : name, 'language' : language})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)

