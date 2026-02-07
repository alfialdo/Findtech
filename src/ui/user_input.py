import base64

import streamlit as st

from src.ui import load_recommender_engine
from src.ui.config import BRAND_LOGO, BRANDS, EXTRAS, SCREEN_SIZES, USAGE_TYPES
from src.ui.styles import question_header


def toggle_brand(brand):
    if brand in st.session_state.q_brands:
        st.session_state.q_brands.remove(brand)
    else:
        st.session_state.q_brands.append(brand)


def get_img_html(file_path):
    try:
        with open(file_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        # We assign a custom class 'brand-logo' here!
        return f'<img src="data:image/png;base64,{data}" class="brand-logo">'
    except FileNotFoundError:
        return ""


def clear_brands():
    st.session_state.q_brands = []


def run_recommendation():
    selected_size = SCREEN_SIZES[st.session_state.q_screen]
    selected_extra = [1 if feat in st.session_state.q_extras else 0 for feat in EXTRAS]

    user_data = {
        "brands": st.session_state.q_brands,
        "budget": st.session_state.q_budget,
        "usage": st.session_state.q_usage,
        "portability": st.session_state.q_portability_val,
        "size": selected_size,
        "extra": selected_extra,
    }

    with st.spinner("Preferences Saved! Analyzing recommendations..."):
        recom, laptop_emb = load_recommender_engine()
        top_items, scores = recom.predict_top_k(user_data, laptop_emb, top_k=5)

    st.session_state.recommendations = top_items
    st.session_state.scores = scores
    st.session_state.show_results = True

    st.rerun()


@st.fragment
def render_brand_preference():
    question_header("Q1. Any favorite brands?", "🏆")

    if "q_brands" not in st.session_state:
        st.session_state.q_brands = []

    is_all_selected = len(st.session_state.q_brands) == 0

    st.button(
        "✨ Anything",
        type="primary" if is_all_selected else "secondary",
        width="stretch",
        key="btn_brand_all",
        on_click=clear_brands,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    cols_per_row = 4
    for i in range(0, len(BRANDS), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(BRANDS):
                brand_str = BRANDS[i + j]
                with cols[j]:
                    # Image
                    img_path = BRAND_LOGO[brand_str]
                    img_html = get_img_html(img_path)
                    st.markdown(img_html, unsafe_allow_html=True)

                    # Button logic
                    is_selected = brand_str in st.session_state.q_brands

                    st.button(
                        label=f"{'✅' if is_selected else ''} {brand_str.upper()}",
                        key=f"btn_{brand_str}",
                        type="primary" if is_selected else "secondary",
                        width="stretch",
                        on_click=toggle_brand,
                        args=(brand_str,),
                    )


def render_user_input():
    st.markdown("---")

    # Q1: BRAND PREFERENCE
    render_brand_preference()

    # Q2: BUDGET
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q2. What is your budget limit?", "💰")

    st.slider(
        "Slide to set max price",
        min_value=0,
        max_value=8000,
        value=1500,
        step=100,
        format="$%d",
        key="q_budget",
    )

    # Q3: MAIN USAGE
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q3. What will you use it for?", "🎯")

    st.radio(
        "Select your primary activity:", USAGE_TYPES, horizontal=True, key="q_usage"
    )

    # Q4: PORTABILITY
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q4. How mobile are you?", "🪶")

    portability_map = {
        "Barely (Desktop replacement)": 0.25,
        "Sometimes (Coffee shop runs)": 0.5,
        "Often (Student/Commuter)": 0.75,
        "Very Often (Digital Nomad)": 1.0,
    }

    portability_label = st.select_slider(
        "Portability Level:",
        options=list(portability_map.keys()),
        value="Sometimes (Coffee shop runs)",
        key="q_portability_label",
    )
    # Store the actual float value
    st.session_state.q_portability_val = portability_map[portability_label]

    # Q5: SCREEN SIZE
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q5. Preferred Screen Size?", "🖥️")

    screen_options = list(SCREEN_SIZES.keys())
    st.pills(
        "Select one:",
        screen_options,
        selection_mode="single",
        default=screen_options[1],
        key="q_screen",
    )

    # Q6: EXTRAS
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q6. Must-have features?", "✨")

    st.pills("Select all that apply:", EXTRAS, selection_mode="multi", key="q_extras")

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Find My Laptop", type="primary", width="stretch"):
            run_recommendation()
