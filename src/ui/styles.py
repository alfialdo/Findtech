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

        /* Headers */
        h1, h2, h3 {{
            color: {THEME["text"]};
            font-weight: 700;
        }}

        div[data-testid="stColumn"] button {{
            font-size: 15px !important;
            font-weight: 600 !important;
            padding: 0.5rem 0.5rem !important;
            min-height: 45px;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            transition: all 0.2s;
        }} 
        
        div[data-testid="stColumn"] button:hover {{
            border-color: {THEME["primary"]};
            transform: translateY(-2px);
        }}

        div[data-testid="stImage"] img {{
            height: 90px !important; 
            object-fit: contain !important;
            margin-bottom: 8px;
            filter: grayscale(100%);
            transition: filter 0.3s ease;
        }}

        div[data-testid="stImage"] img:hover {{
            filter: grayscale(0%);
        }}


        label[data-testid="stWidgetLabel"] p {{
            font-size: 18px !important; 
            font-weight: 600;
            color: #444;
            margin-bottom: 5px;
        }}

        div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] {{
            font-size: 15px !important;
            font-weight: 500;
        }}

        div[data-testid="stSliderThumbValue"] {{
            font-size: 16px !important;
            font-weight: bold;
        }}
        
        div.stSlider > div[data-baseweb = "slider"] > div > div {{
            background-color: {THEME["primary"]} !important;
        }}

        div[role="radiogroup"] p {{
            font-size: 16px !important; 
            font-weight: 500;
            color: #333;
        }}
        
        div[role="radiogroup"] {{
            gap: 15px; 
        }}

        div[data-testid="stMultiSelect"] span {{
            background-color: {THEME["secondary"]};
            color: #222;
            border-radius: 8px;
            font-size: 16px !important; 
            padding: 4px 10px;
        }}
        
        div[data-baseweb="select"] ul li {{
            font-size: 16px !important;
        }}

        button[data-testid="stBaseButton-pills"] {{
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0 !important;
            color: #444444;
            padding: 10px 24px !important;
            border-radius: 12px;
            transition: background-color 0.2s, border-color 0.2s;
        }}

        button[data-testid="stBaseButton-pills"] p {{
            font-size: 16px !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
        }}

        button[data-testid="stBaseButton-pills"][aria-selected="true"] p {{
            font-weight: 600 !important;
            font-size: 16px !important;
            color: #222222 !important;
        }}

        button[data-testid="stBaseButton-pills"][aria-selected="true"] {{
            background-color: {THEME["secondary"]} !important;
            border-color: {THEME["secondary"]} !important;
            color: #222222 !important;
        }}

        button[data-testid="stBaseButton-pills"]:hover {{
            border-color: {THEME["primary"]} !important;
            background-color: #FAFAFA;
        }}

        .question-box {{
            background-color: white;
            padding: 25px; 
            border-radius: 20px; 
            box-shadow: 0 8px 20px rgba(0,0,0,0.06); 
            margin-bottom: 25px;
            border-left: 6px solid {THEME["primary"]};
        }}
        
        .question-box:hover {{
            box-shadow: 0 12px 25px rgba(0,0,0,0.08);
            transform: translateY(-1px);
            transition: all 0.3s ease;
        }}
        </style>
    """,
        unsafe_allow_html=True,
    )


def question_header(title, icon="🔹"):
    st.markdown(
        f"""
        <div class="question-box">
            <h3 style='margin-bottom: 0px;'>{icon} {title}</h3>
        </div>
    """,
        unsafe_allow_html=True,
    )
