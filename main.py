import streamlit as st
import asyncio
from parallel import app   

st.set_page_config(
    page_title="🎬 Movie Recommendation",
    page_icon="🎥",
    layout="wide"
)

# ---------------------- CSS ----------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#312e81);
}

.title{
    text-align:center;
    color:white;
    font-size:45px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#dddddd;
    font-size:18px;
}

.card{
    background:white;
    color:black;
    border-radius:15px;
    padding:20px;
    margin-top:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,.3);
}

.bigcard{
    background:linear-gradient(90deg,#ff512f,#dd2476);
    color:white;
    border-radius:20px;
    padding:25px;
    margin-top:20px;
    box-shadow:0px 5px 20px rgba(0,0,0,.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------

st.markdown("<div class='title'>🎬 AI Movie Recommendation System</div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Find your next favorite movie instantly</div>", unsafe_allow_html=True)

st.write("")

movie = st.text_input(
    "Enter Movie Name",
    placeholder="Interstellar"
)

search = st.button("🎥 Recommend Movies")

# ---------------------- RUN ----------------------

if search:

    if movie.strip() == "":
        st.warning("Please enter a movie name.")

    else:

        workflow = {
            "User_input": movie
        }

        with st.spinner("Finding the best recommendations..."):

            result = asyncio.run(app.ainvoke(workflow))

        st.success("Recommendations Ready!")

        details = result["Movie_details"]

        st.markdown("## 🎬 Movie Details")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("⭐ IMDb", details["IMDB Rating"])
        c2.metric("🎭 Genre", details["Genre"])
        c3.metric("📅 Year", details["Release Year"])
        c4.metric("⏱ Runtime", details["Runtime"])

        with st.expander("Movie Information"):

            st.write(f"**Title:** {details['Title']}")
            st.write(f"**Director:** {details['Director']}")
            st.write(f"**Cast:** {details['Cast']}")
            st.write(f"**Language:** {details['Language']}")
            st.write(f"**Plot:** {details['Plot']}")

        st.markdown("---")

        st.markdown("## 🏆 Top Recommended Movies")

        st.markdown(
            f"""
            <div class='bigcard'>
            {result["Recommendation"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("## 📺 OTT Availability")

        st.markdown(
            f"""
            <div class='card'>
            {result["OTT_checker"]}
            </div>
            """,
            unsafe_allow_html=True
        )