import streamlit as st
import pandas as pd
from database import functions as db
from enum import Enum
from pygments.lexer import default
from datetime import datetime, timedelta


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
    if date.month < 10:
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = "0" + str(date.day)
    else:
        day = str(date.day)

    return year + "-" + month + "-" + day

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

col1, col2 = st.columns(2)

with col1:
    current_region = st.selectbox("Region", ["All", "NA", "LATAM"], index=1)

with col2:
    timeframe = st.selectbox("Timeframe", ["Last 1 Hour", "Last 1 Day", "Last 1 Week", "Last 1 Month", "Last 1 Year", "All Time"])

all_plants = db.getPlants(get_region_id(current_region))

plant_data = []
for plant in all_plants:
    faults = db.getTotalPlantFaultsFromDate(plant, get_time_from_input(timeframe))
    plant_data.append((plant,faults))

dataframe = pd.DataFrame(plant_data, columns=["Plant", "Faults"])

# st.line_chart(data = dataframe, x = "Plant", y = "Faults", x_label= "Plant", y_label="Faults")
barchart = st.bar_chart(data = dataframe, x = "Plant", y = "Faults", x_label= "Plant", y_label="Faults", stack=False)
# st.write(pd.DataFrame.loc[barchart.columns > 20])
