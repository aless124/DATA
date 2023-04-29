from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)  # Pour initialiser l'application
app.config["DEBUG"] = True # Pour activer le débogage et le rechargement automatique du code


app.config['MONGO_DBNAME'] = 'final_exam'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/final_exam'
mongo = PyMongo(app)
collection = mongo.db.final_exam
# Récupérer tous les documents de la collection
@app.route('/documents', methods=['GET'])
def get_all_documents():
    documents = collection.find()
    output = []
    for document in documents:
        #print(document)
        output.append({'id': str(document['_id']), 'Titre': document['Titre'].strip(), 'Origine': document['Origine']})
    return jsonify({'result': output})

# Récupérer un document par son ID
@app.route('/documents/<document_id>', methods=['GET'])
def get_document_by_id(document_id):
    document = collection.find_one({'_id': ObjectId(document_id)})
    if document:
        output = {'id': str(document['_id']), 'Titre': document['Titre'].strip(), 'Origine': document['Origine']}
    else:
        output = 'Document not found'
    return jsonify({'result': output})

# Ajouter un nouveau document
@app.route('/documents', methods=['POST'])
def add_document():
    name = request.json['name']
    description = request.json['description']
    document_id = mongo.db.collection.insert({'name': name, 'description': description})
    new_document = mongo.db.collection.find_one({'_id': document_id })
    output = {'id': str(new_document['_id']), 'name': new_document['name'], 'description': new_document['description']}
    return jsonify({'result': output})

# Mettre à jour un document
@app.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    document = mongo.db.collection.find_one({'_id': ObjectId(document_id)})
    if document:
        name = request.json['name']
        description = request.json['description']
        mongo.db.collection.update({'_id': ObjectId(document_id)}, {'$set': {'name': name, 'description': description}})
        updated_document = mongo.db.collection.find_one({'_id': ObjectId(document_id)})
        output = {'id': str(updated_document['_id']), 'name': updated_document['name'], 'description': updated_document['description']}
    else:
        output = 'Document not found'
    return jsonify({'result': output})

# Supprimer un document
@app.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = mongo.db.collection.find_one({'_id': ObjectId(document_id)})
    if document:
        mongo.db.collection.remove({'_id': ObjectId(document_id)})
        output = 'Document deleted successfully'
    else:
        output = 'Document not found'
    return jsonify({'result': output})

# Recuperer uniquement X documents
@app.route('/documents/&limit=<int:limit>', methods=['GET'])
def get_document_by_limit(limit):
    documents = collection.find().limit(limit)
    output = []
    for document in documents:
        output.append({'id': str(document['_id']), 'Titre': document['Titre'].strip(), 'Origine': document['Origine']})
    return jsonify({'result': output})

# Recuperer uniquement les documents dont le titre contient un mot
@app.route('/documents/&titre=<string:titre>', methods=['GET'])
def get_document_by_titre(titre):
    print("debug",titre)
    print(collection.find_one()['Titre'])
    document = str(collection.find_one({'Titre': titre})).strip()

    print("debug oo",document)
    if document:
        output = {'id': str(document['_id']), 'Titre': document['Titre'], 'Origine': document['Origine']}
    else:
        output = 'Document not found'
    return jsonify({'result': output})

# affiche le titre du premier document


#app.run()
if __name__ == '__main__':
    app.run(debug=True)