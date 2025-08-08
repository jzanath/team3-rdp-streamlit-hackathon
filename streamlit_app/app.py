import traceback

import streamlit as st
from database import functions as db

def main() -> None:
    welcome = st.Page("pages/welcome.py", title="Welcome", icon=":material/home:", default=False)
    dashboardLanding = st.Page("pages/dashboardLanding.py", title="Home", icon=":material/home:", default=True)
    siteBySite = st.Page(page="pages/siteBySite.py", title="Site By Site", icon=":material/factory:", default=False)
    plantData = st.Page(page="pages/plantData.py", title="Plant Data", icon=":material/manufacturing:", default=False)


    
    pg = st.navigation([
        dashboardLanding,
        siteBySite,
        plantData
    ])


    pg.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
