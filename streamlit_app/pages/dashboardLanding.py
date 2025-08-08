import streamlit as st
from database import functions as db

st.write("This will be the dashboad landing page :smile:")
st.divider()

plants = db.getPlants()
st.write(plants)

st.divider()
for plant in plants:
    numOfFaults = db.getTotalPlantFaults(plant)
    st.write("%s has %s faults." % (plant, numOfFaults))

st.divider()
for plant in plants:
    avgKWH = db.getAvgPlantKWH(plant)
    if avgKWH is not None:
        st.write("%s is using %s KWh on average." % (plant, avgKWH))
    else:
        st.write("%s does not appear in the utility_summary table." % (plant))