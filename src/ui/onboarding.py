import streamlit as st


def render_onboarding():
    # st.title("💻 Findtech")
    st.markdown(
        "<h1 style='text-align: center;'>💻 Findtech 💻 <br> AI-based Laptop Finder</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style='background-color: #E8F1F2; padding: 20px; border-radius: 10px; margin-bottom: 25px;'>
        <p style='font-size: 18px; color: #4A4A4A;'>
            Welcome! Finding the perfect laptop shouldn't be rocket science. 
            Tell us a bit about your needs, budget, and preference, and Findtech 
            <b>Hybrid AI Engine</b> will find your perfect tech companion.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if "started" not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        if st.button("🚀 Start My Search", type="primary"):
            st.session_state.started = True
            st.rerun()
