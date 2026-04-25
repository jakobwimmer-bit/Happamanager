import streamlit as st

st.set_page_config(page_title="Einkaufsliste – Happahappa", page_icon="🛒", layout="centered", initial_sidebar_state="collapsed")

from utils.styles import apply_styles
from utils.db import (
    get_shopping_list, add_manual_item,
    toggle_shopping_item, remove_shopping_item,
    clear_checked_items, clear_all_shopping_list
)

apply_styles()

CATEGORIES = [
    "Gemüse & Obst", "Fleisch & Fisch", "Milchprodukte & Eier",
    "Brot & Backwaren", "Tiefkühl", "Gewürze & Öle",
    "Konserven & Trockenware", "Getränke", "Sonstiges"
]
UNITS = ["g", "kg", "ml", "l", "EL", "TL", "Stück", "Bund", "Prise", "Packung", "Dose", "Scheibe", ""]

st.markdown("""
<div class="page-header">
    <span class="page-header-icon">🛒</span>
    <h2>Einkaufsliste</h2>
</div>
""", unsafe_allow_html=True)

# ── Reload button ──
col_r, col_cc, col_ca = st.columns(3)
with col_r:
    if st.button("🔄 Neu laden", use_container_width=True):
        st.rerun()
with col_cc:
    if st.button("✅ Erledigte löschen", use_container_width=True):
        clear_checked_items()
        st.rerun()
with col_ca:
    if st.button("🗑️ Alle löschen", use_container_width=True):
        st.session_state.confirm_clear = True

if st.session_state.get("confirm_clear"):
    st.warning("Gesamte Einkaufsliste löschen?")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Ja", type="primary"):
            clear_all_shopping_list()
            st.session_state.confirm_clear = False
            st.rerun()
    with c2:
        if st.button("❌ Nein"):
            st.session_state.confirm_clear = False
            st.rerun()

st.markdown("---")

# ── Manual add ──
with st.expander("➕ Artikel manuell hinzufügen"):
    with st.form("manual_add", clear_on_submit=True):
        m_name = st.text_input("Artikel *", placeholder="z.B. Butter")
        mc1, mc2 = st.columns(2)
        with mc1:
            m_qty = st.number_input("Menge", min_value=0.0, value=1.0, step=0.5)
        with mc2:
            m_unit = st.selectbox("Einheit", UNITS)
        m_cat = st.selectbox("Kategorie", CATEGORIES)
        if st.form_submit_button("Hinzufügen", type="primary", use_container_width=True):
            if m_name.strip():
                add_manual_item(m_name.strip(), m_qty, m_unit, m_cat)
                st.success(f"{m_name} hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte einen Namen eingeben.")

st.markdown("---")

# ── Shopping list grouped by category ──
items = get_shopping_list()

if not items:
    st.info("Die Einkaufsliste ist leer. Füge Rezepte aus dem Wochenplaner oder manuell Artikel hinzu.")
else:
    # Count stats
    total = len(items)
    checked = sum(1 for i in items if i["checked"])
    st.markdown(f"""
    <div style="background: rgba(255,107,53,0.08); border-radius:12px; padding: 0.6rem 1rem; margin-bottom: 0.75rem; font-weight:700; font-size:0.95rem; color: var(--primary-dark);">
        ✅ {checked} von {total} Artikeln erledigt
    </div>
    """, unsafe_allow_html=True)

    # Group by category
    from collections import defaultdict
    by_cat = defaultdict(list)
    for item in items:
        by_cat[item["category"] or "Sonstiges"].append(item)

    # Sort categories by predefined order
    cat_order = {c: i for i, c in enumerate(CATEGORIES)}
    sorted_cats = sorted(by_cat.keys(), key=lambda c: cat_order.get(c, 99))

    for cat in sorted_cats:
        cat_items = by_cat[cat]
        unchecked = [i for i in cat_items if not i["checked"]]
        checked_items = [i for i in cat_items if i["checked"]]

        if not cat_items:
            continue

        st.markdown(f'<div class="shop-category-header">🏷️ {cat} ({len(unchecked)} offen)</div>', unsafe_allow_html=True)

        for item in unchecked + checked_items:
            col_check, col_info, col_del = st.columns([1, 5, 1])

            with col_check:
                new_checked = st.checkbox(
                    "✓",
                    value=item["checked"],
                    key=f"chk_{item['id']}",
                    label_visibility="collapsed"
                )
                if new_checked != item["checked"]:
                    toggle_shopping_item(item["id"], new_checked)
                    st.rerun()

            with col_info:
                qty_str = ""
                if item.get("quantity"):
                    q = item["quantity"]
                    qty_str = f"{int(q) if q == int(q) else q}"
                    if item.get("unit"):
                        qty_str += f" {item['unit']}"
                    qty_str += " · "

                name_style = "text-decoration: line-through; color: #aaa;" if item["checked"] else "font-weight:600;"
                st.markdown(f"""
                <div style="{name_style} padding: 0.35rem 0; font-size:0.95rem;">
                    {qty_str}{item['item_name']}
                    {'<span style="font-size:0.7rem; color:#aaa;"> (manuell)</span>' if item.get('added_manually') else ''}
                </div>
                """, unsafe_allow_html=True)

            with col_del:
                if st.button("✕", key=f"del_{item['id']}"):
                    remove_shopping_item(item["id"])
                    st.rerun()