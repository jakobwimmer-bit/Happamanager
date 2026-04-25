import streamlit as st
from utils.auth import require_login, logout_user

require_login()  # Prüft, ob eingeloggt; sonst zeigt Login-Form

st.set_page_config(
    page_title="Happahappamanager",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from utils.styles import apply_styles
apply_styles()

st.markdown("""
<div class="home-header">
    <div class="home-icon">🍽️</div>
    <h1>Happahappa<br>manager</h1>
    <p class="home-subtitle">Dein persönlicher Küchenassistent</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("📖\n\nRezepte", use_container_width=True, key="nav_rezepte"):
        st.switch_page("pages/1_Rezepte.py")

    if st.button("📅\n\nWochenplaner", use_container_width=True, key="nav_wochenplaner"):
        st.switch_page("pages/2_Wochenplaner.py")

with col2:
    if st.button("🛒\n\nEinkaufsliste", use_container_width=True, key="nav_einkauf"):
        st.switch_page("pages/3_Einkaufsliste.py")

st.markdown("""
<div class="home-footer">
    <p>Guten Appetit! 😋</p>
</div>
""", unsafe_allow_html=True)

# Optional: Logout-Button hinzufügen
if st.button("Logout"):
    logout_user()