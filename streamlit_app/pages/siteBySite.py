import streamlit as st
import pandas as pd
import plotly.express as px
from database import functions as db
from datetime import datetime, timedelta

# ------------------ Helper Functions ------------------ #
def get_region_id(region):
    if region == "All":
        return 0
    elif region == "NA":
        return 1
    elif region == "LATAM":
        return 2
    return None

def format_date(date):
    year = str(date.year)
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    return f"{year}-{month}-{day}"

def get_time_from_input(time):
    current_datetime = datetime.now()
    if time == "Last 1 Hour":
        return format_date(current_datetime - timedelta(hours=1))
    elif time == "Last 1 Day":
        return format_date(current_datetime - timedelta(days=1))
    elif time == "Last 1 Week":
        return format_date(current_datetime - timedelta(weeks=1))
    elif time == "Last 1 Month":
        return format_date(current_datetime - timedelta(days=30))
    elif time == "Last 1 Year":
        return format_date(current_datetime - timedelta(days=365))
    elif time == "All Time":
        return format_date(current_datetime - timedelta(days=3000))
    return None

# ------------------ Streamlit Layout ------------------ #
st.set_page_config(page_title="Site-to-Site Dashboard", layout="wide")
st.title("🏭 Site-by-Site Comparison")
# ------------------ Sidebar Filters ------------------ #
st.sidebar.header("🔧 Filter Options")
current_region = st.sidebar.selectbox("Select Region", ["All", "NA", "LATAM"], index=1)
timeframe = st.sidebar.selectbox("Select Timeframe", ["Last 1 Hour", "Last 1 Day", "Last 1 Week", "Last 1 Month", "Last 1 Year", "All Time"])

# ------------------ Data Retrieval ------------------ #
all_plants = db.getPlants(get_region_id(current_region))
plant_data = []
for plant in all_plants:
    faults = db.getTotalPlantFaultsFromDate(plant, get_time_from_input(timeframe))
    plant_data.append((plant, faults))

dataframe = pd.DataFrame(plant_data, columns=["Plant", "Faults"])

# ------------------ Visualization 1 ------------------ #
st.markdown("### Faults by Plant")
fig1 = px.bar(dataframe, x="Plant", y="Faults", color="Faults", color_continuous_scale="Viridis",
              title=f"Faults per Plant in {current_region} Region ({timeframe})")
fig1.update_layout(xaxis_title="Plant", yaxis_title="Faults", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

# ------------------ Visualization 2: Volume Over Time ------------------ #
st.markdown("### Product Volume Over Time by Site")

# Dropdown for site selection
selected_site = st.selectbox("Select Site for Volume Trend", ["Chicago", "Orlando", "Houston"])

# Generate mock time series data
time_range = pd.date_range(start="2023-01-01", periods=12, freq="M")
volume_data = pd.DataFrame({
    "Time": time_range.tolist() * 3,
    "Site": ["Chicago"] * 12 + ["Orlando"] * 12 + ["Houston"] * 12,
    "Volume": (
        list((1000 + 50 * i + (i % 3) * 100) for i in range(12)) +
        list((1200 + 30 * i + (i % 2) * 80) for i in range(12)) +
        list((1100 + 40 * i + (i % 4) * 60) for i in range(12))
    )
})


# Plot volume over time for all plants
fig2 = px.line(volume_data, x="Time", y="Volume", color="Site", markers=True,
               title="Volume Produced Over Time for All Plants",
               template="plotly_white")
fig2.update_layout(xaxis_title="Month", yaxis_title="Volume Produced")
st.plotly_chart(fig2, use_container_width=True)




