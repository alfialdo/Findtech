import streamlit as st

from src.ui.config import BRANDS, EXTRAS, SCREEN_SIZES, USAGE_TYPES
from src.ui.styles import question_header


def render_user_input():
    if not st.session_state.get("started", False):
        return

    st.markdown("---")

    # Q1: BRAND PREFERENCE
    question_header("Q1. Any favorite brands?", "🏆")
    selected_brands = st.pills(
        "Select brands (Leave empty for all)",
        BRANDS,
        selection_mode="multi",
        key="q_brands",
    )

    # Q2: BUDGET
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q2. What is your budget limit?", "💰")

    budget = st.slider(
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

    usage = st.radio(
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

    screen_size = st.pills(
        "Select one:",
        SCREEN_SIZES,
        selection_mode="single",
        default=SCREEN_SIZES[1],
        key="q_screen",
    )

    # Q6: EXTRAS
    st.markdown("<br>", unsafe_allow_html=True)
    question_header("Q6. Must-have features?", "✨")

    extras = st.pills(
        "Select all that apply:", EXTRAS, selection_mode="multi", key="q_extras"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Find My Laptop", type="primary", use_container_width=True):
            save_and_process()


def save_and_process():
    # This is where you would call your ML Backend
    user_data = {
        "brands": st.session_state.q_brands,
        "budget": st.session_state.q_budget,
        "usage": st.session_state.q_usage,
        "portability": st.session_state.q_portability_val,
        "screen": st.session_state.q_screen,
        "extras": st.session_state.q_extras,
    }

    st.success("Preferences Saved! Calculating recommendations...")
    st.json(user_data)
