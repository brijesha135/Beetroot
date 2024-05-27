from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os
import csv
from io import StringIO

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/contact_db"
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/contacts', methods=['POST'])
def create_new_contact():
    name = request.form['name']
    phone_numbers = request.form.getlist('phone_numbers')
    if 'image' in request.files and allowed_file(request.files['image'].filename):
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        image_url = None

    contact = {
        "name": name,
        "image_url": image_url,
        "phone_numbers": phone_numbers
    }
    contact_id = mongo.db.contacts.insert_one(contact).inserted_id
    return jsonify(str(contact_id)), 201

@app.route('/contacts', methods=['GET'])
def fetch_all_contacts():
    contacts = mongo.db.contacts.find()
    return jsonify([{**contact, '_id': str(contact['_id'])} for contact in contacts]), 200

@app.route('/contacts/search', methods=['GET'])
def search_for_contacts():
    name = request.args.get('name')
    phone_number = request.args.get('phone_number')
    query = {}
    if name:
        query['name'] = name
    if phone_number:
        query['phone_numbers'] = {"$in": [phone_number]}
    contacts = mongo.db.contacts.find(query)
    return jsonify([{**contact, '_id': str(contact['_id'])} for contact in contacts]), 200

@app.route('/contacts/<contact_id>', methods=['PUT'])
def update_existing_contact(contact_id):
    name = request.form['name']
    phone_numbers = request.form.getlist('phone_numbers')
    if 'image' in request.files and allowed_file(request.files['image'].filename):
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        image_url = None

    query = {"_id": mongo.db.ObjectId(contact_id)}
    update = {"$set": {"name": name, "image_url": image_url, "phone_numbers": phone_numbers}}
    result = mongo.db.contacts.update_one(query, update)
    return jsonify({"modified_count": result.modified_count}), 200

@app.route('/contacts/<contact_id>', methods=['DELETE'])
def delete_existing_contact(contact_id):
    query = {"_id": mongo.db.ObjectId(contact_id)}
    result = mongo.db.contacts.delete_one(query)
    return jsonify({"deleted_count": result.deleted_count}), 200

@app.route('/contacts/export/csv', methods=['GET'])
def export_contacts_to_csv():
    contacts = mongo.db.contacts.find()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["_id", "name", "phone_numbers"])
    writer.writeheader()
    for contact in contacts:
        writer.writerow({"_id": str(contact['_id']), "name": contact['name'], "phone_numbers": ', '.join(contact['phone_numbers'])})
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, attachment_filename='contacts.csv')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0')
