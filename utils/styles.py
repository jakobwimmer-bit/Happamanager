import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap');

    /* ── Global Reset & Base ── */
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .main .block-container {
        padding: 1rem 1rem 4rem 1rem;
        max-width: 480px;
        margin: 0 auto;
    }

    /* Hide default sidebar toggle on mobile */
    [data-testid="collapsedControl"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }

    /* ── Color Variables ── */
    :root {
        --primary: #FF6B35;
        --primary-light: #FF8C5A;
        --primary-dark: #E8511A;
        --secondary: #2D6A4F;
        --secondary-light: #40916C;
        --accent: #FFD166;
        --bg: #FFF8F0;
        --card-bg: #FFFFFF;
        --text: #1A1A2E;
        --text-muted: #6B7280;
        --border: #F0E4D4;
        --success: #40916C;
        --danger: #EF4444;
        --shadow: 0 2px 12px rgba(255,107,53,0.10);
        --shadow-lg: 0 8px 32px rgba(255,107,53,0.18);
        --radius: 16px;
        --radius-sm: 10px;
    }

    /* ── Background ── */
    .stApp {
        background: var(--bg);
        background-image:
            radial-gradient(circle at 10% 10%, rgba(255,107,53,0.07) 0%, transparent 50%),
            radial-gradient(circle at 90% 90%, rgba(45,106,79,0.05) 0%, transparent 50%);
    }

    /* ── Home Header ── */
    .home-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .home-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 4px 8px rgba(255,107,53,0.3));
    }
    .home-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: var(--primary);
        line-height: 1.1;
        margin: 0;
    }
    .home-subtitle {
        color: var(--text-muted);
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .home-footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 1.1rem;
        padding: 1rem 0;
    }

    /* ── Page Header ── */
    .page-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 0 0.5rem 0;
        margin-bottom: 0.5rem;
    }
    .page-header-icon { font-size: 2rem; }
    .page-header h2 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 900;
        color: var(--primary);
        margin: 0;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--card-bg);
        color: var(--text);
        border: 2px solid var(--border);
        border-radius: var(--radius);
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        padding: 1rem 0.5rem;
        min-height: 80px;
        width: 100%;
        transition: all 0.18s ease;
        box-shadow: var(--shadow);
        white-space: pre-line;
        line-height: 1.4;
    }
    .stButton > button:hover {
        border-color: var(--primary);
        color: var(--primary);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Primary action buttons */
    .stButton > button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white !important;
        border: none;
        min-height: 52px;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-light), var(--primary));
        color: white !important;
    }

    /* ── Cards ── */
    .recipe-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1.5px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.18s ease;
    }
    .recipe-card:hover {
        border-color: var(--primary-light);
        box-shadow: var(--shadow-lg);
    }
    .recipe-card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 0.25rem 0;
    }
    .recipe-card-meta {
        color: var(--text-muted);
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* ── Category Badge ── */
    .category-badge {
        display: inline-block;
        background: rgba(255,107,53,0.12);
        color: var(--primary-dark);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    /* ── Shopping List Item ── */
    .shop-category-header {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--secondary);
        border-bottom: 2px solid var(--secondary-light);
        padding-bottom: 4px;
        margin: 1rem 0 0.5rem 0;
    }
    .shop-item {
        background: var(--card-bg);
        border-radius: var(--radius-sm);
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.4rem;
        border: 1.5px solid var(--border);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .shop-item.checked {
        opacity: 0.45;
        text-decoration: line-through;
    }

    /* ── Week Plan ── */
    .weekday-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        border: 1.5px solid var(--border);
        box-shadow: var(--shadow);
    }
    .weekday-label {
        font-weight: 800;
        font-size: 0.85rem;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .weekday-recipe {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text);
    }
    .weekday-empty {
        color: var(--text-muted);
        font-size: 0.9rem;
        font-style: italic;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--border) !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 1rem !important;
        background: var(--card-bg) !important;
        color: var(--text) !important;  /* Added to ensure text is dark */
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(255,107,53,0.15) !important;
        color: var(--text) !important;  /* Ensure focused text is also dark */
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: var(--text);
        background: var(--card-bg);
        border-radius: var(--radius-sm);
        border: 1.5px solid var(--border);
    }

    /* ── Divider ── */
    hr {
        border: none;
        border-top: 1.5px solid var(--border);
        margin: 1rem 0;
    }

    /* ── Success / Info / Warning Boxes ── */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: var(--radius-sm);
        font-family: 'Nunito', sans-serif;
    }

    /* ── Bottom Nav ── */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--card-bg);
        border-top: 2px solid var(--border);
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 0.5rem 0 calc(0.5rem + env(safe-area-inset-bottom));
        z-index: 999;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
    }
    .nav-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        color: var(--text-muted);
        font-size: 0.7rem;
        font-weight: 700;
        text-decoration: none;
        padding: 0.3rem 0.8rem;
        border-radius: var(--radius-sm);
        transition: all 0.15s;
        cursor: pointer;
        background: none;
        border: none;
        font-family: 'Nunito', sans-serif;
    }
    .nav-btn .nav-icon { font-size: 1.5rem; }
    .nav-btn.active { color: var(--primary); }
    .nav-btn:hover { color: var(--primary); background: rgba(255,107,53,0.08); }

    /* ── Image in recipe ── */
    .recipe-img {
        width: 100%;
        border-radius: var(--radius);
        object-fit: cover;
        max-height: 220px;
        margin-bottom: 0.5rem;
    }

    /* ── Ingredient row ── */
    .ing-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.95rem;
    }
    .ing-amount {
        font-weight: 800;
        color: var(--primary);
        min-width: 60px;
    }
    .ing-name { color: var(--text); }

    /* Checkbox override for shopping list */
    .stCheckbox > label {
        font-family: 'Nunito', sans-serif;
        font-size: 1rem;
        font-weight: 600;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--border);
        border-radius: var(--radius-sm);
        padding: 3px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: calc(var(--radius-sm) - 2px);
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


def nav_bar(active: str):
    """Render bottom navigation bar."""
    pages = [
        ("🏠", "Start", "app"),
        ("📖", "Rezepte", "pages/1_Rezepte"),
        ("📅", "Planer", "pages/2_Wochenplaner"),
        ("🛒", "Einkauf", "pages/3_Einkaufsliste"),
    ]
    html = '<div class="bottom-nav">'
    for icon, label, page in pages:
        cls = "nav-btn active" if active == label else "nav-btn"
        html += f'<div class="{cls}" onclick="window.location=\'/{page}\'">'
        html += f'<span class="nav-icon">{icon}</span><span>{label}</span></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)