from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)  # Pour initialiser l'application
app.config["DEBUG"] = True # Pour activer le débogage et le rechargement automatique du code


app.config['MONGO_DBNAME'] = 'final_exam'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/final_exam'
mongo = PyMongo(app)

# Récupérer tous les documents de la collection
@app.route('/documents', methods=['GET'])
def get_all_documents():
    documents = mongo.db.collection.find()
    output = []
    for document in documents:
        output.append({'id': str(document['_id']), 'name': document['name'], 'description': document['description']})
    return jsonify({'result': output})

# Récupérer un document par son ID
@app.route('/documents/<document_id>', methods=['GET'])
def get_document_by_id(document_id):
    document = mongo.db.collection.find_one({'_id': ObjectId(document_id)})
    if document:
        output = {'id': str(document['_id']), 'name': document['name'], 'description': document['description']}
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


'''
@app.route('/', methods=['GET'])
def home():
   return "<h1>Annuaire Internet</h1><p>Ce site est le prototype dune API mettant à disposition des données sur les employés dune entreprise.</p>"
'''
#app.run()
if __name__ == '__main__':
    app.run(debug=True)