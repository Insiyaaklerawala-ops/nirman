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
# 🚨 ALERT SIMULATION
# ---------------------------
def generate_alert():
    alerts = [
        "🚨 High leakage detected in Sector 12",
        "⚠️ Pipeline pressure drop in Zone 5",
        "🚨 Underground leak suspected near main road",
        "⚠️ Sensor anomaly detected"
    ]
    return random.choice(alerts)


# ---------------------------
# 📊 ANALYTICS
# ---------------------------
def calculate_metrics(leaks):
    total = len(leaks)

    water_loss = total * random.randint(100, 500)
    repair_time = random.randint(2, 24)
    cost = total * random.randint(500, 2000)

    return total, water_loss, repair_time, cost