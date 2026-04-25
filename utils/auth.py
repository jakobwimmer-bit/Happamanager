import streamlit as st
from utils.supabase_client import get_supabase

def login_user(email: str, password: str):
    sb = get_supabase()
    try:
        response = sb.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["user"] = response.user
        st.success("Eingeloggt!")
        st.rerun()
    except Exception as e:
        st.error(f"Login fehlgeschlagen: {e}")

def logout_user():
    sb = get_supabase()
    sb.auth.sign_out()
    st.session_state.pop("user", None)
    st.rerun()

def is_logged_in():
    return "user" in st.session_state and st.session_state["user"] is not None

def _on_email_change():
    st.session_state["email_changed"] = True

def _on_password_change():
    st.session_state["password_changed"] = True

def require_login():
    if not is_logged_in():
        st.title("Login")
        email = st.text_input("E-Mail", on_change=_on_email_change)
        password = st.text_input("Passwort", type="password", on_change=_on_password_change)
        
        # Auto-login wenn beide Felder gefüllt sind
        if email and password and st.session_state.get("email_changed") and st.session_state.get("password_changed"):
            login_user(email, password)
        
        if st.button("Einloggen"):
            login_user(email, password)
        
        st.stop()

def register_user(email: str, password: str):
    sb = get_supabase()
    try:
        sb.auth.sign_up({"email": email, "password": password})
        st.success("Registrierung erfolgreich! Überprüfe deine E-Mail.")
    except Exception as e:
        st.error(f"Registrierung fehlgeschlagen: {e}")