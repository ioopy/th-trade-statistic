import streamlit as st

def authenticated_menu(initial_page=False):
    st.sidebar.page_link("pages/Ehscode02.py", label="1️⃣ การส่งออกของไทยรายประเทศ")
    st.sidebar.page_link("pages/Ecomcode03.py", label="2️⃣ สินค้าส่งออกสำคัญของไทยรายประเทศ")
    st.sidebar.markdown("---")
    st.session_state.authenticator.logout("Logout", "sidebar")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")


def menu(initial_page):
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is None:
        unauthenticated_menu()
        return
    authenticated_menu(initial_page)


def menu_with_redirect():
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is None:
        st.switch_page("app.py")
    authenticated_menu()