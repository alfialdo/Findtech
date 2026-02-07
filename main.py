import streamlit as st

from src.ui import (
    apply_custom_styles,
    load_recommender_engine,
    render_onboarding,
    render_results,
    render_user_input,
)

# Page Config
st.set_page_config(page_title="Findtech", page_icon="💻", layout="centered")


def main():
    # Apply Design Styles
    apply_custom_styles()

    # Cached model and lookup table
    load_recommender_engine()

    # Render Onboarding
    render_onboarding()

    # Render User Input
    if st.session_state.get("started", False):
        render_user_input()

    if "recommendations" in st.session_state:
        render_results()


if __name__ == "__main__":
    main()
