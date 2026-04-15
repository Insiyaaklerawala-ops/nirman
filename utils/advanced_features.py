import folium
from streamlit_folium import st_folium
import random

# ---------------------------
# 🗺️ MAP VIEW
# ---------------------------
def show_map(leaks):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    for leak in leaks:
        lat = leak.get("lat", random.uniform(18, 28))
        lon = leak.get("lon", random.uniform(70, 85))

        folium.Marker(
            location=[lat, lon],
            popup=f"Leak at {leak['location']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

    st_folium(m, width=700)


# ---------------------------
# 🚨 SMART ALERT SYSTEM
# ---------------------------
def generate_alert(leaks):
    if not leaks:
        return "No active issues"

    high_risk = [l for l in leaks if l.get("status") == "Pending"]

    if len(high_risk) > 5:
        return "🚨 Multiple leaks detected! Immediate action required"

    return f"⚠️ {len(high_risk)} active leaks need attention"


# ---------------------------
# 📊 ANALYTICS
# ---------------------------
def calculate_metrics(leaks):
    total = len(leaks)

    if total == 0:
        return 0, 0, 0, 0

    water_loss = sum([random.randint(100, 300) for _ in leaks])
    repair_time = sum([random.randint(2, 10) for _ in leaks]) / total
    cost = water_loss * 2

    return total, water_loss, repair_time, cost