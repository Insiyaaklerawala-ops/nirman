from flask import Flask, render_template, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename

from utils.database import save_leak, load_leaks, save_repair, load_repairs, update_leak_status
from utils.ai_verifier import verify_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------
# 🏠 HOME
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# 🚨 REPORT LEAK
# ---------------------------
@app.route("/report_leak", methods=["POST"])
def report_leak():
    location = request.form.get("location")
    image = request.files.get("image")

    if not location or not image:
        return jsonify({"status": "error", "message": "Missing data"})

    filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

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

# ---------------------------
# 📋 GET ALL LEAKS
# ---------------------------
@app.route("/get_leaks")
def get_leaks():
    return jsonify(load_leaks())

# ---------------------------
# 📊 DASHBOARD METRICS
# ---------------------------
@app.route("/metrics")
def metrics():
    leaks = load_leaks()
    repairs = load_repairs()

    total_leaks = len(leaks)
    repaired = len([l for l in leaks if l["status"] == "Repaired"])
    pending = total_leaks - repaired

    water_loss = total_leaks * 50
    cost = len(repairs) * 1000

    return jsonify({
        "total": total_leaks,
        "repaired": repaired,
        "pending": pending,
        "water_loss": water_loss,
        "cost": cost
    })

# ---------------------------
# 🛠 SAVE REPAIR
# ---------------------------
@app.route("/repair", methods=["POST"])
def repair():
    leak_id = int(request.form.get("leak_id"))
    before = request.files.get("before")
    after = request.files.get("after")

    if not before or not after:
        return jsonify({"status": "error", "message": "Images required"})

    before_name = f"{uuid.uuid4().hex}_{secure_filename(before.filename)}"
    after_name = f"{uuid.uuid4().hex}_{secure_filename(after.filename)}"

    before_path = os.path.join(UPLOAD_FOLDER, before_name)
    after_path = os.path.join(UPLOAD_FOLDER, after_name)

    before.save(before_path)
    after.save(after_path)

    save_repair(
        leak_id,
        f"/static/uploads/{before_name}",
        f"/static/uploads/{after_name}",
        cost=1000,
        water_loss=50
    )

    return jsonify({"status": "success"})

# ---------------------------
# 🔄 UPDATE STATUS
# ---------------------------
@app.route("/update_status", methods=["POST"])
def update_status():
    leak_id = int(request.form.get("leak_id"))
    status = request.form.get("status")

    update_leak_status(leak_id, status)

    return jsonify({"status": "success"})

# ---------------------------
# 📈 GET REPAIRS
# ---------------------------
@app.route("/get_repairs")
def get_repairs():
    return jsonify(load_repairs())

if __name__ == "__main__":
    app.run(debug=True)