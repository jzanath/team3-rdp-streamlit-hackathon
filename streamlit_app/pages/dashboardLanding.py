import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from database import functions as db

# Set page config for better layout
st.set_page_config(page_title="Production Metrics Dashboard", layout="wide")

# Title with icon and reduced spacing
st.markdown("""
    <h2 style='text-align: center; margin-bottom: 10px;'>📊 Production Metrics Dashboard</h2>
""", unsafe_allow_html=True)

# Selection boxes in a styled container
with st.container():
    st.markdown("### Filter Options")
    col_sel1, col_sel2 = st.columns([1, 1])
    with col_sel1:
        region = st.selectbox("🌍 Region", ["All", "NA", "LATAM"])
    with col_sel2:
        time_period = st.selectbox("⏱️ Time Period", ["Last Day", "Last Week", "Last Month", "Last Year"])

# Divider
st.markdown("---")

# Metrics section
st.markdown("### Key Metrics")
col1, col2 = st.columns(2)

def get_region_id(region):
    if region == "All":
        return 0
    elif region == "NA":
        return 1
    elif region == "LATAM":
        return 2
    return None

# Function call to database
all_plants = db.getPlants(get_region_id(region)) # time goes here

total_faults = 0
for plant in all_plants:
    total_faults += db.getTotalPlantFaults(plant)

with col1:
    avg_batch_time = np.random.uniform(1.0, 10.0)
    st.metric(label="🕒 Avg Batch Time (Hours)", value=f"{avg_batch_time:.2f}")

with col2:
    alerts_faults = np.random.randint(0, 20)
    st.metric(label="⚠️ Alerts / Faults", value=total_faults)

# Divider
st.markdown("---")

# Energy usage chart
st.markdown("### 📈 Avg Energy Usage Over Time")
energy_usage = np.random.uniform(100, 500, size=10)
fig, ax = plt.subplots()
ax.plot(energy_usage, marker='o', linestyle='-', color='teal')
ax.set_title("Energy Usage Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Energy (kWh)")
ax.grid(True)
st.pyplot(fig)
