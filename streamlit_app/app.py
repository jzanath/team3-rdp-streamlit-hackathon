import traceback

import streamlit as st

def main() -> None:
    welcome = st.Page("pages/welcome.py", title="Welcome", icon=":material/home:", default=True)
    dashboardLanding = st.Page("pages/dashboardLanding.py", title="Home", icon=":material/home:", default=False)

    print("Hello World")
    print("Im on staging!")

    pg = st.navigation(
        {
            "App": [welcome],
            "Dashboard Landing": [dashboardLanding],
        }
    )

    pg.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
