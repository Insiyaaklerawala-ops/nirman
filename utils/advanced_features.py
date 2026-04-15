import folium
from streamlit_folium import st_folium

# ---------------------------
# 🗺️ MUMBAI MAP FUNCTION
# ---------------------------
def show_map(leaks):
    mumbai_coords = [19.0760, 72.8777]

    # Create map
    m = folium.Map(
        location=mumbai_coords,
        zoom_start=12,
        tiles="CartoDB positron"
    )

    # If no leaks → show base marker
    if not leaks:
        folium.Marker(
            mumbai_coords,
            tooltip="Mumbai City Center",
            icon=folium.Icon(color="blue")
        ).add_to(m)

    # Add leak markers
    for leak in leaks:
        lat = leak.get("lat", 19.0760)
        lon = leak.get("lon", 72.8777)

        folium.Marker(
            location=[lat, lon],
            popup=f"Leak: {leak['location']}",
            tooltip=leak['location'],
            icon=folium.Icon(color="red", icon="tint")
        ).add_to(m)

    st_folium(m, width=900, height=500)


# ---------------------------
# 🚨 ALERT GENERATOR
# ---------------------------
def generate_alert():
    return "⚠️ Multiple leak reports detected! Immediate action required in affected zones."


# ---------------------------
# 📊 METRICS CALCULATION
# ---------------------------
def calculate_metrics(leaks):
    total = len(leaks)
    water_loss = total * 50
    repair_time = total * 2
    cost = total * 1000

    return total, water_loss, repair_time, cost