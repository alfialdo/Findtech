import streamlit as st

from src.ui.config import THEME


def apply_custom_styles():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #FAFAFA;
        }}
        
        .css-1r6slb0, .stMarkdown, .stButton {{
            font-family: 'Helvetica Neue', sans-serif;
        }}

        div.stSlider > div[data-baseweb = "slider"] > div > div {{
            background-color: {THEME["primary"]} !important;
        }}
        
        div[data-testid="stMultiSelect"] span {{
            background-color: {THEME["secondary"]};
            color: #333;
            border-radius: 12px;
        }}
        
        h1, h2, h3 {{
            color: {THEME["text"]};
            font-weight: 700;
        }}
        
        .question-box {{
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border-left: 5px solid {THEME["primary"]};
        }}
        </style>
    """,
        unsafe_allow_html=True,
    )


def question_header(title, icon="🔹"):
    st.markdown(
        f"""
        <div class="question-box">
            <h3>{icon} {title}</h3>
        </div>
    """,
        unsafe_allow_html=True,
    )
