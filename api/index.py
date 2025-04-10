from flask import Flask, request, jsonify, send_file, send_from_directory, abort, render_template
import os

app = Flask(__name__)

# Directory where images are stored
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(WORKING_DIR, 'images')

# API to get the image
@app.route("/get-image", methods=["GET"])
def get_image():
    file = request.args.get("file")
    if not file:
        return jsonify({"error": "Missing 'file' parameter"}), 400

    try:
        # Build the file path
        file_path = os.path.join(IMAGE_DIR, file)
        
        # Serve the file if it exists in the IMAGE_DIR
        if os.path.isfile(file_path):
            return send_file(file_path)

        # Default response for non-existent files
        return jsonify({"error": "File not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to list all images in the gallery directory
@app.route("/list-images", methods=["GET"])
def list_images():
    try:
        files = os.listdir(IMAGE_DIR)
        return jsonify({"images": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home route
@app.route("/")
def home():
    # return WORKING_DIR
    return render_template("index.html")

@app.route("/info")
def info():
    return jsonify({
        "cwd": os.getcwd(),
        "images": IMAGE_DIR
    })

# Run the Flask application
if __name__ == "__main__":
    print(WORKING_DIR)
    app.run(debug=False, port=10001)
