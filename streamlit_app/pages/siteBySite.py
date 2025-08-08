import streamlit as st
import pandas as pd
from database import functions as db

col1, col2 = st.columns(2)

with col1:
    current_region = st.selectbox("Region", ["All", "NA", "LATAM"])

with col2:
    timeframe = st.selectbox("Timeframe", ["Last 1 Hour", "Last 1 Day", "Last 1 Week", "Last 1 Month", "Last 1 Year"])

st.write("This will be the site by site comparison page: " + current_region)
barchart = st.line_chart(data = db.getPlants(current_region), x = "", y= "", x_label= "Time", y_label="Data")
st.write(pd.loc[barchart.columns > 20])
st.bar_chart(data = db.getPlants(current_region), x = "", y= "", x_label= "Time", y_label="Data", stack=False)