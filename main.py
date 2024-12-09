from flask import Flask, request, jsonify
from PIL import Image, ImageFilter
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if an image is included in the request
    if 'image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Generate a unique filename for the uploaded image
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    # Save the uploaded image
    file.save(filepath)

    # Convert the image to an artistic format
    art_filepath = apply_art_effect(filepath)

    return jsonify({
        "message": "Image uploaded and processed successfully",
        "original_image": f"/static/uploads/{unique_filename}",
        "processed_image": f"/static/uploads/{os.path.basename(art_filepath)}"
    })

def apply_art_effect(filepath):
    """Applies an artistic effect to the image."""
    img = Image.open(filepath)
    # Apply an artistic filter (e.g., contour)
    img = img.filter(ImageFilter.CONTOUR)

    # Save the processed image
    art_filepath = filepath.replace('.jpg', '_art.jpg').replace('.png', '_art.png')
    img.save(art_filepath)
    return art_filepath

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
