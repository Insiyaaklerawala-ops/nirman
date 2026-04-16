from flask import Flask, render_template, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename

from utils.database import save_leak, load_leaks, save_repair
from utils.ai_verifier import verify_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/report_leak", methods=["POST"])
def report_leak():
    location = request.form.get("location")
    image = request.files.get("image")

    if not location or not image:
        return jsonify({"status": "error", "message": "Missing data"})

    # ✅ SAFE UNIQUE FILENAME
    original_name = secure_filename(image.filename)
    filename = f"{uuid.uuid4().hex}_{original_name}"

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # ✅ VERIFY IMAGE
    result = verify_image(filepath)

    if result["is_valid"]:
        save_leak(location, f"/static/uploads/{filename}")
        return jsonify({
            "status": "success",
            "confidence": result["confidence"]
        })
    else:
        return jsonify({
            "status": "error",
            "message": result["message"]
        })

@app.route("/get_leaks")
def get_leaks():
    return jsonify(load_leaks())

if __name__ == "__main__":
    app.run(debug=True)