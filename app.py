import streamlit as st
from utils.auth import require_login, logout_user

require_login()  # Prüft, ob eingeloggt; sonst zeigt Login-Form

st.set_page_config(
    page_title="Happahappamanager",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from utils.styles import apply_styles, nav_bar
apply_styles()

st.markdown("""
<div class="home-header">
    <div class="home-icon">🍽️</div>
    <h1>Happahappa<br>manager</h1>
    <p class="home-subtitle">Dein persönlicher Küchenassistent</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Bottom navigation
nav_bar("Start")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="home-footer">
    <p>Guten Appetit! 😋</p>
</div>
""", unsafe_allow_html=True)

# Optional: Logout-Button hinzufügen
if st.button("Logout"):
    logout_user()