import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

st.title("🚀 Streamlit & Supabase Ready!")

# Supabase Verbindung testen
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if url and key:
    supabase = create_client(url, key)
    st.success("Verbindung zu Supabase steht im Hintergrund!")
else:
    st.error("Fehler: Umgebungsvariablen nicht gefunden.")
    