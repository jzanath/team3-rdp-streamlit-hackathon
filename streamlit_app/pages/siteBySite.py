import streamlit as st
import pandas as pd
from database import functions as db
from enum import Enum
from pygments.lexer import default

col1, col2 = st.columns(2)

with col1:
    current_region = st.selectbox("Region", ["All", "NA", "LATAM"], index=1)

with col2:
    timeframe = st.selectbox("Timeframe", ["Last 1 Hour", "Last 1 Day", "Last 1 Week", "Last 1 Month", "Last 1 Year"])

st.write("This will be the site by site comparison page: " + current_region)

def get_region_id(region):
    if region == "All":
        return 0
    elif region == "NA":
        return 1
    elif region == "LATAM":
        return 2
    return None

all_plants = db.getPlants(get_region_id(current_region))

plant_data = []
for plant in all_plants:
    faults = db.getTotalPlantFaults(plant)
    plant_data.append((plant,faults))

dataframe = pd.DataFrame(plant_data, columns=["Plant", "Faults"])

st.line_chart(data = dataframe, x = "Plant", y = "Faults", x_label= "Plant", y_label="Faults")
barchart = st.bar_chart(data = dataframe, x = "Plant", y = "Faults", x_label= "Plant", y_label="Faults", stack=False)
st.write(pd.DataFrame.loc[barchart.columns > 20])
