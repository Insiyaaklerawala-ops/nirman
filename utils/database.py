import json
import datetime

LEAK_FILE = "data/leaks.json"
REPAIR_FILE = "data/repairs.json"

# ---------------------------
# 📥 LOAD DATA
# ---------------------------
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

# ---------------------------
# 💾 SAVE DATA
# ---------------------------
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# 🚨 SAVE LEAK REPORT
# ---------------------------
def save_leak(location, image, lat=None, lon=None):
    leaks = load_data(LEAK_FILE)

    new_leak = {
        "id": len(leaks) + 1,
        "location": location,
        "image": image,   # ✅ FIXED (use passed value)
        "lat": lat,
        "lon": lon,
        "status": "Pending",
        "time_reported": str(datetime.datetime.now())
    }

    leaks.append(new_leak)
    save_data(LEAK_FILE, leaks)

# ---------------------------
# 📊 GET ALL LEAKS
# ---------------------------
def load_leaks():
    return load_data(LEAK_FILE)

# ---------------------------
# 🛠️ SAVE REPAIR DATA
# ---------------------------
def save_repair(leak_id, before_img, after_img, cost, water_loss):

    repairs = load_data(REPAIR_FILE)

    repair_entry = {
        "leak_id": leak_id,
        "before": before_img,
        "after": after_img,
        "cost": cost,
        "water_loss": water_loss,
        "repair_time": str(datetime.datetime.now())
    }

    repairs.append(repair_entry)
    save_data(REPAIR_FILE, repairs)

    update_leak_status(leak_id, "Repaired")

# ---------------------------
# 🔄 UPDATE LEAK STATUS
# ---------------------------
def update_leak_status(leak_id, status):
    leaks = load_data(LEAK_FILE)

    for leak in leaks:
        if leak["id"] == leak_id:
            leak["status"] = status

    save_data(LEAK_FILE, leaks)

# ---------------------------
# 📈 GET REPAIR LOGS
# ---------------------------
def load_repairs():
    return load_data(REPAIR_FILE)