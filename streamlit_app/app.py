import traceback

import streamlit as st
from database import functions as db

def main() -> None:
    welcome = st.Page("pages/welcome.py", title="Welcome", icon=":material/home:", default=False)
    dashboardLanding = st.Page("pages/dashboardLanding.py", title="Home", icon=":material/home:", default=True)

    pg = st.navigation(
        {
            "Dashboard Landing": [dashboardLanding],
            "App": [welcome],
        }
    )

    pg.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
