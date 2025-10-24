# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Render sets this
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Create table
with app.app_context():
    db.create_all()

# GET all products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    return jsonify(result)

# POST add product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    product = Product(name=data.get("name"), price=data.get("price"))
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name, "price": product.price}), 201

# DELETE product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
