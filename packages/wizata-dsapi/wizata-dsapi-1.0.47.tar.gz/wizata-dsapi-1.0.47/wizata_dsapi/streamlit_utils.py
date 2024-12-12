import sys


def get_streamlit_token():
    if 'streamlit' in sys.modules:
        st = sys.modules['streamlit']
        if st.query_params is not None and "auth_token" in st.query_params:
            auth_token = st.query_params["auth_token"]
            return auth_token


def get_streamlit_domain():
    if 'streamlit' in sys.modules:
        st = sys.modules['streamlit']
        if st.query_params is not None and "dsapi" in st.query_params:
            domain = st.query_params["dsapi"]
            return domain
