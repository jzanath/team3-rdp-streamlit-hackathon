import traceback

import streamlit as st

from streamlit_app._logger import log, logging_config


@st.cache_resource
def _configure_logging() -> None:
    logging_config()
    log.info("Starting application...")


def main() -> None:
    welcome = st.Page("pages/welcome.py", title="Welcome", icon=":material/home:", default=True)

    print("Hello World")
    pg = st.navigation(
        {
            "App": [welcome],
        }
    )

    pg.run()


if __name__ == "__main__":
    try:
        _configure_logging()
        main()
    except Exception as e:
        log.critical(traceback.format_exc())
        raise e
