from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)  # Pour initialiser l'application
app.config["DEBUG"] = True # Pour activer le débogage et le rechargement automatique du code


app.config['MONGO_DBNAME'] = 'final_exam'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/final_exam'
mongo = PyMongo(app)
collection = mongo.db.final_exam
for doc in collection.find():
    titre = str(doc['Titre']).replace('\n', '').replace('\r', '').strip()
    collection.update_one({'_id': doc['_id']}, {'$set': {'Titre': titre}})

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
    titre = request.json['titre']
    origine = request.json['origine']
    document_id = collection.insert_one({'Titre': titre, 'Origine': origine}).inserted_id
    new_document = collection.find_one({'_id': document_id })
    output = {'id': str(new_document['_id']), 'Titre': new_document['Titre'], 'Origine': new_document['Origine']}
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
        output.append({'id': str(document['_id']), 'Titre': document['Titre'], 'Origine': document['Origine']})
    return jsonify({'result': output})

# Recuperer uniquement les documents dont le titre contient un mot
@app.route('/documents/&titre=<string:titre>', methods=['GET'])
def get_document_by_titre(titre):
    document = collection.find_one({'Titre': titre})
    if document:
        output = {'id': str(document['_id']), 'Titre': document['Titre'], 'Origine': document['Origine']}
    else:
        output = 'Document not found'
    return jsonify({'result': output})

# Recuperer uniquement les documents avec les origines
@app.route('/documents/&origine=<string:origine>', methods=['GET'])
def get_document_by_origine(origine):
    def checkRequest(Req):
        if Req == "japon":
            Req = "Japon"
        elif Req.lower() == "coreedusud" or Req.lower() == "coréedusud":
            Req = "CoréeDuSud"
        elif Req.lower() == "chine":
            Req = "Chine"
        return Req
    origine = checkRequest(origine)
    documents = collection.find({'Origine': origine})
    output = []
    for document in documents:
        output.append({'id': str(document['_id']), 'Titre': document['Titre'], 'Origine': document['Origine']})
    return jsonify({'result': output})


#app.run()
if __name__ == '__main__':
    app.run(debug=True)