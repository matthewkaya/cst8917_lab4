from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functions.createDocument import create_document
from functions.readDocument import read_document

load_dotenv()

app = Flask(__name__)

@app.route('/create-document', methods=['POST'])
def create_document_route():
    req_body = request.json
    result = create_document(req_body)
    return jsonify(result), 201

@app.route('/read-document/<doc_id>', methods=['GET'])
def read_document_route(doc_id):
    result = read_document(doc_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
