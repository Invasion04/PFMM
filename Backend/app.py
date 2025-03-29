from flask import Flask, jsonify, request
from flask_cors import CORS
from firebase import initialize_firebase
from models import Expense
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase
try:
    db = initialize_firebase()
except Exception as e:
    print(f"Failed to initialize Firebase: {e}")
    db = None

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    if not db:
        return jsonify({"error": "Database not initialized"}), 500
    
    try:
        expenses_ref = db.collection('expenses')
        expenses = [doc.to_dict() for doc in expenses_ref.stream()]
        return jsonify(expenses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    if not db:
        return jsonify({"error": "Database not initialized"}), 500
    
    try:
        data = request.json
        expense = Expense(
            name=data.get('name'),
            amount=data.get('amount'),
            category=data.get('category', 'Uncategorized')
        )
        
        db.collection('expenses').add(expense.to_dict())
        return jsonify({"message": "Expense added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    if not db:
        return jsonify({"error": "Database not initialized"}), 500
    
    try:
        db.collection('expenses').document(expense_id).delete()
        return jsonify({"message": "Expense deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)