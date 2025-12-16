"""
Demo Flask API Application
A simple REST API for demonstrating Jenkins CI/CD pipeline
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demo purposes
items = []


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Welcome to the Demo API",
        "version": "1.0.0"
    })


@app.route("/api/items", methods=["GET"])
def get_items():
    """Get all items"""
    return jsonify({"items": items, "count": len(items)})


@app.route("/api/items", methods=["POST"])
def create_item():
    """Create a new item"""
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    item = {
        "id": len(items) + 1,
        "name": data["name"],
        "description": data.get("description", "")
    }
    items.append(item)

    return jsonify({"item": item, "message": "Item created successfully"}), 201


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Get a specific item by ID"""
    item = next((i for i in items if i["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"item": item})


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item by ID"""
    global items
    item = next((i for i in items if i["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    items = [i for i in items if i["id"] != item_id]
    return jsonify({"message": "Item deleted successfully"})


def add_numbers(a, b):
    """Simple utility function for testing"""
    return a + b


def multiply_numbers(a, b):
    """Simple utility function for testing"""
    return a * b


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
