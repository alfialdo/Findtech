import streamlit as st

from src.ui import apply_custom_styles, render_onboarding, render_user_input

# Page Config
st.set_page_config(page_title="Findtech", page_icon="💻", layout="centered")


def main():
    # 1. Apply Design
    apply_custom_styles()

    # 2. Render Onboarding
    render_onboarding()

    # 3. Render User Input
    render_user_input()


if __name__ == "__main__":
    main()
