import streamlit as st
from utils.io import load_weather
from charts.charts import chart_dashboard, interactive_viz

st.set_page_config(page_title="Explore", layout="wide")
df = load_weather()

st.title("Interactive Exploratory View")
st.write("Use interaction to validate and extend the story—focus on one weather type, then zoom into a time window.")

st.altair_chart(chart_dashboard(df), use_container_width=True)

st.markdown("**Guided prompts:**")
st.write("- Filter to one weather type (e.g., `sun`, `rain`)—does the temperature distribution shift?")
st.write("- Brush a specific year—do extremes cluster in particular periods?")
st.write("- Compare histogram shape across weather types—what changes most: center, spread, or tails?")


st.title("Another Interactive Exploratory View")
st.write("Use interaction to understand the relationship between wind and average temperature (taken as an average of the min. and max. temperature for that day), and extend the focus to its relationship with weather-type.")

st.altair_chart(interactive_viz(df), use_container_width=True)

st.markdown("**Guided prompts:**")
st.write("- Brush over the extreme regions in the scatterplot — are certain regions of wind-temperature associated with a weather-type?")
st.caption("Takeaway: Higher wind and lower temperature days are associated with rain and fog weather types.")

