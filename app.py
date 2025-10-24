from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = [
    {"id": 1, "name": "Chocolate Cake", "price": 20},
    {"id": 2, "name": "Blueberry Muffin", "price": 5},
    {"id": 3, "name": "Croissant", "price": 3}
]

# GET all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

# GET single product
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

# POST - add new product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid product data"}), 400
    new_id = max(p["id"] for p in products) + 1 if products else 1
    product = {"id": new_id, "name": data["name"], "price": data["price"]}
    products.append(product)
    return jsonify(product), 201

# DELETE product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return jsonify({"message": "Product deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
