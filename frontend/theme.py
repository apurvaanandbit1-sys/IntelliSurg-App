"""
theme.py
────────
All custom CSS and HTML component builders for the IntelliSurg dashboard.

Design direction: "dark monitoring station."
- Near-black background, dark slate cards
- Glowing teal as the primary signal color (text-shadow + box-shadow glow)
- Soft red glow for high-alert states
- Rounded corners, generous whitespace

Import this once in app.py and call inject_css() at the top.
Every other function returns an HTML string — pass it to st.markdown(html, unsafe_allow_html=True).
"""

import streamlit as st

# ── Color tokens ───────────────────────────────────────────────────────────────
# Single source of truth so every card/badge stays visually consistent.
COLORS = {
    "bg_page"      : "#0B0F14",
    "bg_card"      : "#11161D",
    "bg_subcard"   : "#161C24",
    "border"       : "#232B33",
    "border_light" : "#1C232B",
    "text_primary" : "#EAF2F5",
    "text_muted"   : "#5C7A8A",
    "accent"       : "#3DE8C4",     # glowing teal — primary signal
    "accent_dark"  : "#2BC9A8",
    "accent_glow"  : "rgba(61,232,196,0.55)",
    "low_bg"       : "rgba(61,232,196,0.10)",
    "low_text"     : "#3DE8C4",
    "medium_bg"    : "rgba(239,159,39,0.12)",
    "medium_text"  : "#EF9F27",
    "high_bg"      : "rgba(226,75,74,0.12)",
    "high_text"    : "#F09595",
    "high_glow"    : "rgba(226,75,74,0.5)",
}


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS INJECTION
# ─────────────────────────────────────────────────────────────────────────────

def inject_css():
    """
    Call once at the top of app.py, right after st.set_page_config().
    Restyles Streamlit's native chrome (sidebar, buttons, tabs, inputs)
    to match the dark monitoring-station look.
    """
    st.markdown(
        f"""
        <style>
        /* ---- Page background ---- */
        .stApp {{
            background-color: {COLORS['bg_page']};
        }}

        /* ---- Typography — force light text everywhere on dark bg ---- */
        html, body, [class*="css"] {{
            font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: {COLORS['text_primary']};
        }}
        p, span, label, div {{
            color: {COLORS['text_primary']};
        }}

        /* ---- Hide default Streamlit chrome we don't want ---- */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{
            background-color: {COLORS['bg_page']};
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['bg_card']};
            border-right: 1px solid {COLORS['border']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['text_primary']};
        }}

        /* ---- Tabs styled as dark segmented control ---- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background-color: {COLORS['bg_subcard']};
            padding: 4px;
            border-radius: 12px;
            border: 1px solid {COLORS['border']};
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 40px;
            border-radius: 9px;
            padding: 0 18px;
            background-color: transparent;
            color: {COLORS['text_muted']};
            font-weight: 500;
            font-size: 14px;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['bg_card']} !important;
            color: {COLORS['accent']} !important;
            box-shadow: 0 0 0 1px {COLORS['border']}, 0 0 14px rgba(61,232,196,0.18);
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: transparent;
        }}

        /* ---- Buttons — glowing teal ---- */
        .stButton > button{{
            background-color:#29C7A7;
            color:white;
            border:none;
            border-radius:10px;
            padding:0.6rem 1.5rem;
            font-weight:600;

            box-shadow:none;

            transition:0.2s;
        }}

        .stButton > button:hover{{
            background-color:#20B294;
            box-shadow:0 4px 14px rgba(41,199,167,.22);
            transform:translateY(-1px);
        }}
        /* ---- Inputs / selects / text areas ---- */
        .stTextInput input, .stNumberInput input, .stTextArea textarea,
        div[data-baseweb="select"] > div {{
            background-color: {COLORS['bg_subcard']} !important;
            border-radius: 9px !important;
            border-color: {COLORS['border']} !important;
            color: {COLORS['text_primary']} !important;
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: {COLORS['text_muted']} !important;
        }}
        div[data-baseweb="select"] span {{
            color: {COLORS['text_primary']} !important;
        }}
        /* dropdown menu popover */
        div[data-baseweb="popover"] li {{
            background-color: {COLORS['bg_subcard']} !important;
            color: {COLORS['text_primary']} !important;
        }}

        /* ---- File uploader ---- */
        [data-testid="stFileUploaderDropzone"] {{
            background-color: {COLORS['bg_subcard']};
            border-radius: 12px;
            border: 1.5px dashed {COLORS['border']};
        }}
        [data-testid="stFileUploaderDropzone"] * {{
            color: {COLORS['text_muted']} !important;
        }}

        /* ---- Expander ---- */
        .streamlit-expanderHeader, [data-testid="stExpander"] {{
            background-color: {COLORS['bg_subcard']} !important;
            border-radius: 10px !important;
            border: 1px solid {COLORS['border']} !important;
            color: {COLORS['text_primary']} !important;
        }}

        /* ---- Code blocks ---- */
        .stCodeBlock, pre {{
            background-color: {COLORS['bg_subcard']} !important;
        }}

        /* ---- Section headers inside forms ---- */
        .section-label {{
            font-size: 11px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: {COLORS['text_muted']};
            margin: 18px 0 8px 0;
            font-weight: 500;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# COMPONENT BUILDERS — each returns an HTML string
# ─────────────────────────────────────────────────────────────────────────────

def page_header(eyebrow: str, title: str, subtitle: str = "") -> str:
    """Top-of-page header used consistently across all four tabs."""
    sub_html = f'<p style="font-size:14px; color:{COLORS["text_muted"]}; margin:4px 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom: 20px;">
        <p style="font-size:11px; letter-spacing:0.06em; color:{COLORS['text_muted']};
                   text-transform:uppercase; margin:0 0 4px;">{eyebrow}</p>
        <p style="font-size:22px; font-weight:500; color:{COLORS['text_primary']}; margin:0;">{title}</p>
        {sub_html}
    </div>
    """


def status_badge(level: str) -> str:
    """
    Small pill badge with subtle glow. level must be 'low', 'medium', or 'high'.
    Used for risk labels, alert levels, triage tiers.
    """
    level = level.lower()
    config = {
        "low"    : (COLORS["low_bg"],    COLORS["low_text"],    "rgba(61,232,196,0.35)",  "Low"),
        "medium" : (COLORS["medium_bg"], COLORS["medium_text"], "rgba(239,159,39,0.3)",   "Medium"),
        "high"   : (COLORS["high_bg"],   COLORS["high_text"],   COLORS["high_glow"],      "High"),
    }
    bg, color, glow, label = config.get(level, config["medium"])
    return f"""
    <span style="background:{bg}; color:{color}; border:1px solid {glow}; border-radius:20px; padding:5px 14px;
                  font-size:13px; font-weight:500; display:inline-flex; align-items:center; gap:6px;
                  box-shadow: 0 0 10px {glow};">
        <span style="width:7px; height:7px; border-radius:50%; background:{color};
                      box-shadow: 0 0 6px {glow}; display:inline-block;"></span>
        {label}
    </span>
    """


def metric_card(icon_class: str, label: str, value: str, pct: float, color: str = None) -> str:
    color = color or COLORS["accent"]
    pct = max(0, min(100, pct))

    return (
        f'<div style="background:{COLORS["bg_subcard"]};border:1px solid {COLORS["border"]};'
        f'border-radius:12px;padding:14px;">'
        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;">'
        f'<i class="ti {icon_class}" style="font-size:16px;color:{color};"></i>'
        f'<span style="font-size:11px;color:{COLORS["text_muted"]};">{label}</span>'
        f'</div>'
        f'<p style="font-size:15px;font-weight:500;margin:0 0 8px;">{value}</p>'
        f'<div style="height:5px;background:{COLORS["border_light"]};border-radius:3px;overflow:hidden;">'
        f'<div style="width:{pct}%;height:100%;background:{color};"></div>'
        f'</div>'
        f'</div>'
    )

def big_metric_card(
    eyebrow: str,
    title: str,
    big_value: str,
    big_label: str,
    pct: float,
    badge_level: str,
    sub_cards_html: str = "",
):
    pct = max(0, min(100, pct))

    glow = COLORS["high_text"] if badge_level.lower()=="high" else COLORS["accent"]
    bar = COLORS["high_text"] if badge_level.lower()=="high" else COLORS["accent"]

    return (
        f'<div style="background:{COLORS["bg_card"]};border:1px solid {COLORS["border"]};'
        f'border-radius:16px;padding:24px;">'

        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;'
        f'margin-bottom:20px;padding-bottom:18px;border-bottom:1px solid {COLORS["border_light"]};">'

        f'<div>'
        f'<p style="font-size:11px;color:{COLORS["text_muted"]};text-transform:uppercase;">{eyebrow}</p>'
        f'<p style="font-size:22px;font-weight:600;margin:0;">{title}</p>'
        f'</div>'

        f'{status_badge(badge_level)}'

        f'</div>'

        f'<div style="display:flex;align-items:baseline;gap:10px;">'
        f'<span style="font-size:46px;font-weight:700;color:{glow};">{big_value}</span>'
        f'<span style="font-size:14px;color:{COLORS["text_muted"]};">{big_label}</span>'
        f'</div>'

        f'<div style="height:8px;background:{COLORS["border_light"]};border-radius:5px;overflow:hidden;margin-top:18px;margin-bottom:20px;">'
        f'<div style="width:{pct}%;height:100%;background:{bar};"></div>'
        f'</div>'

        f'{sub_cards_html}'

        f'</div>'
    )
def disclaimer_footer() -> str:
    """Compliance-style disclaimer, styled like a quiet footer note rather than a warning banner."""
    return f"""
    <div style="display:flex; align-items:center; gap:8px; background:rgba(239,159,39,0.08);
                border:1px solid rgba(239,159,39,0.2); border-radius:10px; padding:10px 14px; margin-top:18px;">
        <i class="ti ti-alert-triangle" style="font-size:15px; color:{COLORS['medium_text']};"></i>
        <span style="font-size:12px; color:{COLORS['medium_text']}; opacity:0.9;">
            Demo application for educational and portfolio purposes only. Not intended for clinical decision-making.
        </span>
    </div>
    """


def empty_state(icon_class: str, message: str) -> str:
    """Shown before the user has run a prediction — invites action, doesn't apologize."""
    return f"""
    <div style="background:{COLORS['bg_subcard']}; border:1px dashed {COLORS['border']};
                border-radius:14px; padding:36px 20px; text-align:center;">
        <i class="ti {icon_class}" style="font-size:28px; color:{COLORS['text_muted']};"></i>
        <p style="font-size:14px; color:{COLORS['text_muted']}; margin:10px 0 0;">{message}</p>
    </div>
    """


def error_card(message: str) -> str:
    """Styled error state with red glow — used when the backend call fails."""
    return f"""
    <div style="background:{COLORS['high_bg']}; border:1px solid {COLORS['high_glow']};
                border-radius:12px; padding:14px 16px; display:flex; align-items:flex-start; gap:10px;
                box-shadow:0 0 14px rgba(226,75,74,0.15);">
        <i class="ti ti-alert-circle" style="font-size:18px; color:{COLORS['high_text']}; margin-top:1px;"></i>
        <div>
            <p style="font-size:14px; font-weight:500; color:{COLORS['high_text']}; margin:0 0 2px;">
                Prediction failed
            </p>
            <p style="font-size:13px; color:{COLORS['high_text']}; margin:0; opacity:0.85;">{message}</p>
        </div>
    </div>
    """


def inject_tabler_icons():
    """
    Loads the Tabler outline icon webfont so <i class="ti ti-*"> works.
    Call once, anywhere before the first icon is rendered.
    """
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tabler-icons/2.44.0/iconfont/tabler-icons.min.css">
        """,
        unsafe_allow_html=True,
    )
