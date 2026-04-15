import streamlit as st
import os
from utils.database import load_leaks
from utils.ai_verifier import verify_image

# ---------------------------
# 🔧 PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Smart Water Monitoring",
    page_icon="💧",
    layout="wide"
)

# ---------------------------
# 🎨 CUSTOM STYLING
# ---------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .stButton>button {
            background-color: #0077b6;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .card {
            padding: 15px;
            border-radius: 15px;
            background-color: white;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 🧭 SIDEBAR NAVIGATION
# ---------------------------
st.sidebar.title("💧 Water Platform")
menu = st.sidebar.radio("Navigate", [
    "Dashboard",
    "Water Supply",
    "Report Leak",
    "View Leaks",
    "Repair Logbook"
])

# ---------------------------
# 🏠 DASHBOARD
# ---------------------------
if menu == "Dashboard":
    st.title("💧 Smart Water Monitoring System")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Leaks", "24")
    col2.metric("Repairs Completed", "18")
    col3.metric("Water Saved", "1200 L")

    st.markdown("### 📊 System Overview")

    st.info("Track leaks, monitor supply, and ensure transparency in water management.")

# ---------------------------
# 💧 WATER SUPPLY UI
# ---------------------------
elif menu == "Water Supply":
    st.header("📍 Water Supply Schedule")

    location = st.text_input("Enter your area")

    if st.button("Check Supply"):
        if location:
            st.success(f"💧 Water available in {location} from 6 AM to 9 AM")
            st.warning("Next supply: Tomorrow at 6 AM")
        else:
            st.error("Please enter a location")

# ---------------------------
# 🚨 REPORT LEAK UI
# ---------------------------
elif menu == "Report Leak":
    st.header("🚨 Report a Water Leak")

    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input("📍 Enter Leak Location")
        severity = st.selectbox("⚠️ Severity", ["Low", "Medium", "High"])

    with col2:
        image = st.file_uploader("📷 Upload Leak Image", type=["jpg", "png"])

    st.markdown("---")

    if st.button("Submit Report"):
        if location and image:
            path = f"assets/uploads/{image.name}"

            with open(path, "wb") as f:
                f.write(image.getbuffer())

            st.info("🔍 Verifying image...")

            result = verify_image(path)

            if result:
                st.success("✅ Leak reported successfully!")
                st.markdown(f"""
                <div class="card">
                    <b>Location:</b> {location} <br>
                    <b>Severity:</b> {severity}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Fake or AI-generated image detected!")

        else:
            st.warning("Please fill all fields")

# ---------------------------
# 📊 VIEW LEAKS UI
# ---------------------------
elif menu == "View Leaks":
    st.header("📊 Reported Leaks")

    leaks = load_leaks()

    if not leaks:
        st.info("No leaks reported yet")
    else:
        for leak in leaks:
            st.markdown(f"""
            <div class="card">
                📍 <b>{leak['location']}</b>
            </div>
            """, unsafe_allow_html=True)

            st.image(leak["image"], use_column_width=True)

# ---------------------------
# 🛠️ REPAIR LOGBOOK UI
# ---------------------------
elif menu == "Repair Logbook":
    st.header("🛠️ Repair Logbook")

    col1, col2 = st.columns(2)

    with col1:
        before = st.file_uploader("📷 Before Repair", key="before")

    with col2:
        after = st.file_uploader("📷 After Repair", key="after")

    time_taken = st.slider("⏱️ Repair Time (hours)", 1, 48)
    cost = st.number_input("💰 Repair Cost (₹)", min_value=0)

    if st.button("Submit Repair"):
        if before and after:
            st.success("✅ Repair logged successfully!")

            st.markdown(f"""
            <div class="card">
                ⏱️ Time Taken: {time_taken} hrs <br>
                💰 Cost: ₹{cost}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.warning("Upload both before and after images!")

# ---------------------------
# 📢 FOOTER
# ---------------------------
st.markdown("---")
st.caption("Built for Smart City Water Management 🚰")