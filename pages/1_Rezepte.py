import streamlit as st

st.set_page_config(page_title="Rezepte – Happahappa", page_icon="📖", layout="centered", initial_sidebar_state="collapsed")

from utils.styles import apply_styles
from utils.db import (
    get_all_recipes, get_recipe, get_recipe_ingredients,
    create_recipe, update_recipe, delete_recipe,
    save_recipe_ingredients, add_recipe_to_shopping_list,
    WEEKDAYS
)

apply_styles()

CATEGORIES = [
    "Gemüse & Obst", "Fleisch & Fisch", "Milchprodukte & Eier",
    "Brot & Backwaren", "Tiefkühl", "Gewürze & Öle",
    "Konserven & Trockenware", "Getränke", "Sonstiges"
]
UNITS = ["g", "kg", "ml", "l", "EL", "TL", "Stück", "Bund", "Prise", "Packung", "Dose", "Scheibe"]

# ── State ──────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "list"        # list | detail | edit | new
if "selected_recipe_id" not in st.session_state:
    st.session_state.selected_recipe_id = None
if "edit_ingredients" not in st.session_state:
    st.session_state.edit_ingredients = []


def go_list():
    st.session_state.view = "list"
    st.session_state.selected_recipe_id = None
    st.session_state.edit_ingredients = []

def go_detail(recipe_id):
    st.session_state.view = "detail"
    st.session_state.selected_recipe_id = recipe_id

def go_edit(recipe_id=None):
    st.session_state.view = "edit"
    st.session_state.selected_recipe_id = recipe_id
    if recipe_id:
        ings = get_recipe_ingredients(recipe_id)
        st.session_state.edit_ingredients = [
            {
                "name": ri["ingredients"]["name"],
                "category": ri["ingredients"]["category"],
                "quantity": ri["quantity"],
                "unit": ri["unit"],
            }
            for ri in ings
        ]
    else:
        st.session_state.edit_ingredients = []


# ══════════════════════════════════════════════
# VIEW: LIST
# ══════════════════════════════════════════════
if st.session_state.view == "list":
    st.markdown("""
    <div class="page-header">
        <span class="page-header-icon">📖</span>
        <h2>Rezepte</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕  Neues Rezept", type="primary", use_container_width=True):
        go_edit(None)
        st.rerun()

    st.markdown("---")

    recipes = get_all_recipes()

    if not recipes:
        st.info("Noch keine Rezepte vorhanden. Lege dein erstes Rezept an!")
    else:
        search = st.text_input("🔍 Suchen…", placeholder="Rezept suchen…", label_visibility="collapsed")
        filtered = [r for r in recipes if search.lower() in r["title"].lower()] if search else recipes

        for recipe in filtered:
            with st.container():
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                    <div class="recipe-card" style="cursor:pointer;">
                        <div class="recipe-card-title">{recipe['title']}</div>
                        <div class="recipe-card-meta">
                            👥 {recipe.get('servings', 2)} Portionen
                            {'&nbsp;&nbsp;🎥' if recipe.get('video_url') else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.button("👁️", key=f"view_{recipe['id']}", help="Ansehen"):
                        go_detail(recipe["id"])
                        st.rerun()


# ══════════════════════════════════════════════
# VIEW: DETAIL
# ══════════════════════════════════════════════
elif st.session_state.view == "detail":
    recipe = get_recipe(st.session_state.selected_recipe_id)
    ings = get_recipe_ingredients(st.session_state.selected_recipe_id)

    col_back, col_edit = st.columns([1, 1])
    with col_back:
        if st.button("← Zurück"):
            go_list(); st.rerun()
    with col_edit:
        if st.button("✏️ Bearbeiten", type="primary"):
            go_edit(recipe["id"]); st.rerun()

    st.markdown(f"""
    <div class="page-header">
        <span class="page-header-icon">🍳</span>
        <h2>{recipe['title']}</h2>
    </div>
    """, unsafe_allow_html=True)

    if recipe.get("image_url"):
        st.image(recipe["image_url"], use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**👥 Portionen:** {recipe.get('servings', 2)}")
    with col2:
        if recipe.get("video_url"):
            st.markdown(f"[🎥 Video ansehen]({recipe['video_url']})")

    if recipe.get("description"):
        st.markdown(f"> {recipe['description']}")

    st.markdown("---")
    st.markdown("**🛒 Zutaten**")

    for ri in ings:
        qty = ri["quantity"]
        qty_str = str(int(qty)) if qty == int(qty) else str(qty)
        st.markdown(f"""
        <div class="ing-row">
            <span class="ing-amount">{qty_str} {ri['unit']}</span>
            <span class="ing-name">{ri['ingredients']['name']}</span>
            <span class="category-badge">{ri['ingredients']['category']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_shop, col_del = st.columns(2)
    with col_shop:
        if st.button("🛒 Zur Einkaufsliste", type="primary", use_container_width=True):
            add_recipe_to_shopping_list(recipe["id"])
            st.success("Zutaten zur Einkaufsliste hinzugefügt!")
    with col_del:
        if st.button("🗑️ Löschen", use_container_width=True):
            st.session_state.confirm_delete = True

    if st.session_state.get("confirm_delete"):
        st.warning("Rezept wirklich löschen?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Ja, löschen", type="primary"):
                delete_recipe(recipe["id"])
                st.session_state.confirm_delete = False
                go_list(); st.rerun()
        with c2:
            if st.button("❌ Abbrechen"):
                st.session_state.confirm_delete = False; st.rerun()


# ══════════════════════════════════════════════
# VIEW: EDIT / NEW
# ══════════════════════════════════════════════
elif st.session_state.view == "edit":
    is_new = st.session_state.selected_recipe_id is None
    recipe = None if is_new else get_recipe(st.session_state.selected_recipe_id)

    if st.button("← Zurück"):
        if recipe:
            go_detail(recipe["id"])
        else:
            go_list()
        st.rerun()

    st.markdown(f"""
    <div class="page-header">
        <span class="page-header-icon">{'➕' if is_new else '✏️'}</span>
        <h2>{'Neues Rezept' if is_new else 'Rezept bearbeiten'}</h2>
    </div>
    """, unsafe_allow_html=True)

    with st.form("recipe_form", clear_on_submit=False):
        title = st.text_input("📝 Name *", value=recipe["title"] if recipe else "")
        description = st.text_area("📄 Beschreibung", value=recipe.get("description", "") if recipe else "", height=80)
        servings = st.number_input("👥 Portionen", min_value=1, max_value=20, value=recipe.get("servings", 2) if recipe else 2)
        video_url = st.text_input("🎥 Video-Link (TikTok, YouTube…)", value=recipe.get("video_url", "") if recipe else "")
        image_file = st.file_uploader("🖼️ Bild hochladen", type=["jpg", "jpeg", "png", "webp"])
        submitted = st.form_submit_button("💾 Speichern", type="primary", use_container_width=True)

    # ── Ingredient editor (outside form so we can add/remove dynamically) ──
    st.markdown("---")
    st.markdown("**🥕 Zutaten**")

    ings = st.session_state.edit_ingredients

    for i, ing in enumerate(ings):
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 3, 1])
            with c1:
                ings[i]["name"] = st.text_input("Zutat", value=ing["name"], key=f"ing_name_{i}", label_visibility="collapsed", placeholder="Zutat")
            with c2:
                ings[i]["quantity"] = st.number_input("Menge", value=float(ing["quantity"]), min_value=0.0, step=0.5, key=f"ing_qty_{i}", label_visibility="collapsed")
            with c3:
                unit_idx = UNITS.index(ing["unit"]) if ing["unit"] in UNITS else 0
                ings[i]["unit"] = st.selectbox("Einheit", UNITS, index=unit_idx, key=f"ing_unit_{i}", label_visibility="collapsed")
            with c4:
                cat_idx = CATEGORIES.index(ing["category"]) if ing["category"] in CATEGORIES else len(CATEGORIES)-1
                ings[i]["category"] = st.selectbox("Kategorie", CATEGORIES, index=cat_idx, key=f"ing_cat_{i}", label_visibility="collapsed")
            with c5:
                if st.button("✕", key=f"ing_del_{i}"):
                    ings.pop(i)
                    st.rerun()

    if st.button("➕ Zutat hinzufügen", use_container_width=True):
        ings.append({"name": "", "category": "Sonstiges", "quantity": 1.0, "unit": "Stück"})
        st.rerun()

    # ── Save logic ──
    if submitted:
        if not title.strip():
            st.error("Bitte einen Namen eingeben.")
        else:
            image_bytes = image_file.read() if image_file else None
            image_name = image_file.name if image_file else None
            valid_ings = [i for i in ings if i["name"].strip()]

            if is_new:
                rid = create_recipe(title, description, video_url, servings, image_bytes, image_name)
            else:
                rid = recipe["id"]
                update_recipe(rid, title, description, video_url, servings, image_bytes, image_name)

            save_recipe_ingredients(rid, valid_ings)
            st.success("Rezept gespeichert!")
            go_detail(rid)
            st.rerun()