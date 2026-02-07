import pandas as pd
import streamlit as st

from src import LaptopRecommender, SupabaseManager


@st.cache_resource(show_spinner="Loading Laptop Database...")
def load_recommender_engine():
    db = SupabaseManager()

    # Fetch Laptop data
    res = db.table("items").select("*").execute()
    raw_item_df = pd.DataFrame(res.data)

    # Fetch CPU Benchmarks
    res = db.fetch_all("cpu_benchmark")
    cpu_df = pd.DataFrame(res)[["cpu", "score"]]
    cpu_df = cpu_df.rename(columns={"score": "cpu_mark"})
    cpu_df["cpu"] = cpu_df.cpu.str.lower()

    # Fetch GPU Benchmarks
    res = db.fetch_all("gpu_benchmark")
    gpu_df = pd.DataFrame(res)[["gpu", "score"]]
    gpu_df = gpu_df.rename(columns={"score": "gpu_mark"})
    gpu_df["gpu"] = gpu_df.gpu.str.lower()

    # Initialize Recommender
    recom = LaptopRecommender(raw_item_df, cpu_df, gpu_df)

    # Pre-compute Embeddings
    laptop_emb = recom.generate_lookup_embedding()

    return recom, laptop_emb


def render_results():
    if not st.session_state.get("show_results", False):
        return

    st.divider()
    st.subheader("🏆 Top Recommendations")

    top_items = st.session_state.recommendations
    scores = st.session_state.scores

    for index, row in top_items.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])

            with col1:
                if row.get("image"):
                    st.image(row["image"], width="stretch")
                else:
                    st.markdown("🖼️ *No Image*")

            with col2:
                # Clickable Title & Price
                st.markdown(f"#### [{row['item_name']}]({row['url']})")
                st.caption(
                    f"**Price:** ${row['price']:,}  |  **Match Score:** {scores[index] * 100:.0f}%"
                )

            st.divider()

    # "Start Over" Button
    if st.button("🔄 Start New Search", type="secondary", width="stretch"):
        st.session_state.show_results = False
        st.session_state.started = False
        st.rerun()
