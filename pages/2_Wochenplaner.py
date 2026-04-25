import streamlit as st
from utils.auth import require_login, logout_user

require_login()  # Prüft, ob eingeloggt; sonst zeigt Login-Form

st.set_page_config(page_title="Wochenplaner – Happahappa", page_icon="📅", layout="centered", initial_sidebar_state="collapsed")

from utils.styles import apply_styles, nav_bar
apply_styles()

st.markdown("""
<div class="page-header">
    <span class="page-header-icon">📅</span>
    <h2>Wochenplaner</h2>
</div>
""", unsafe_allow_html=True)

recipes = get_all_recipes()
week_plan = get_week_plan()

# Build lookup: weekday → plan entry
plan_map = {entry["weekday"]: entry for entry in week_plan}
recipe_map = {r["id"]: r["title"] for r in recipes}
recipe_options = ["– kein Rezept –"] + [r["title"] for r in recipes]
recipe_id_by_title = {r["title"]: r["id"] for r in recipes}

st.markdown("### Diese Woche")

for day in WEEKDAYS:
    entry = plan_map.get(day)
    current_recipe_title = entry["recipes"]["title"] if entry and entry.get("recipes") else None
    current_idx = recipe_options.index(current_recipe_title) if current_recipe_title and current_recipe_title in recipe_options else 0

    with st.container():
        st.markdown(f'<div class="weekday-label">{day}</div>', unsafe_allow_html=True)

        col_sel, col_act = st.columns([4, 1])
        with col_sel:
            selected = st.selectbox(
                day,
                recipe_options,
                index=current_idx,
                key=f"wp_{day}",
                label_visibility="collapsed"
            )
        with col_act:
            if selected != "– kein Rezept –":
                rid = recipe_id_by_title[selected]
                if st.button("🛒", key=f"wp_shop_{day}", help="Zur Einkaufsliste"):
                    add_recipe_to_shopping_list(rid)
                    st.success(f"{selected} zur Einkaufsliste hinzugefügt!")

        # Auto-save when selection changes
        if selected == "– kein Rezept –":
            new_rid = None
        else:
            new_rid = recipe_id_by_title[selected]

        old_rid = entry["recipe_id"] if entry else None
        if new_rid != old_rid:
            if new_rid:
                set_week_plan_entry(day, new_rid)
            else:
                remove_week_plan_entry(day)

        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Add all planned recipes to shopping list ──
planned = [(day, entry) for day, entry in plan_map.items() if entry.get("recipes")]

if planned:
    st.markdown("### 🛒 Alle geplanten Rezepte einkaufen")
    if st.button("Alle Zutaten der Woche zur Einkaufsliste", type="primary", use_container_width=True):
        for day, entry in planned:
            add_recipe_to_shopping_list(entry["recipe_id"])
        st.success(f"{len(planned)} Rezepte zur Einkaufsliste hinzugefügt!")

    st.markdown("**Geplante Gerichte:**")
    for day, entry in planned:
        title = entry["recipes"]["title"] if entry.get("recipes") else "?"
        st.markdown(f"""
        <div class="weekday-card">
            <div class="weekday-label">{day}</div>
            <div class="weekday-recipe">🍽️ {title}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Noch keine Rezepte geplant. Wähle oben Rezepte für die Woche aus.")

# Bottom navigation
st.markdown('<div class="bottom-nav-buttons">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Start", key="nav_start"):
        st.switch_page("app.py")
with col2:
    if st.button("📖 Rezepte", key="nav_rezepte"):
        st.switch_page("pages/1_Rezepte.py")
with col3:
    if st.button("📅 Planer", key="nav_planer"):
        st.switch_page("pages/2_Wochenplaner.py")
with col4:
    if st.button("🛒 Einkauf", key="nav_einkauf"):
        st.switch_page("pages/3_Einkaufsliste.py")
st.markdown('</div>', unsafe_allow_html=True)