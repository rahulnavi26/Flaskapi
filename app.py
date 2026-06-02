import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database of tasks for demonstration
tasks = [
    {
        "id": 1,
        "title": "Set up project",
        "description": "Initialize Flask application and dependencies",
        "completed": True
    },
    {
        "id": 2,
        "title": "Configure Jenkins",
        "description": "Set up Jenkinsfile and build pipeline",
        "completed": False
    }
]

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the Flask API Starter Project",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/api/tasks"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "environment": os.getenv("FLASK_ENV", "production")
    }), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        abort(404, description=f"Task with ID {task_id} not found")
    return jsonify({"task": task}), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing required field: 'title'")
    
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": request.json['title'],
        "description": request.json.get('description', ""),
        "completed": request.json.get('completed', False)
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": error.description}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": error.description}), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
