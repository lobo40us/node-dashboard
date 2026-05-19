import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="NODE Thesis Dashboard", layout="wide")
st.title("🛰️ NODE Spatial Analysis Dashboard")

TARGET_FOLDER = '/content/drive/MyDrive/Node' if os.path.exists('/content/drive/MyDrive/Node') else '.'
grid_path = os.path.join(TARGET_FOLDER, "node_thesis_grid.csv")

@st.cache_data
def load_mesh_matrix():
    if os.path.exists(grid_path):
        return pd.read_csv(grid_path)
    if os.path.exists("node_thesis_grid.csv"):
        return pd.read_csv("node_thesis_grid.csv")
    return pd.DataFrame(columns=['lat', 'lon', 'ancient_sites', 'natural_radiation', 'nuclear_infrastructure'])

df = load_mesh_matrix()

if df.empty:
    st.error("Matrix data layer unavailable. Please ensure node_thesis_grid.csv is present.")
else:
    st.sidebar.header("Matrix Layer Selection")
    layer_choice = st.sidebar.selectbox(
        "Select Active Visualization Vector:",
        ["Ancient Sacred Sites", "Natural Background Radiation", "Anthropogenic Nuclear Infrastructure"]
    )
    
    column_mapping = {
        "Ancient Sacred Sites": "ancient_sites",
        "Natural Background Radiation": "natural_radiation",
        "Anthropogenic Nuclear Infrastructure": "nuclear_infrastructure"
    }
    active_column = column_mapping[layer_choice]
    filtered_df = df[df[active_column] > 0].copy()
    
    st.subheader(f"Global Density Surface: {layer_choice}")
    
    fig_map = px.density_mapbox(
        filtered_df, 
        lat='lat' if 'lat' in filtered_df.columns else filtered_df.columns[0], 
        lon='lon' if 'lon' in filtered_df.columns else filtered_df.columns[1], 
        z=active_column,
        radius=25,
        center={"lat": 20.0, "lon": 0.0}, 
        zoom=1.2,
        mapbox_style="carto-darkmatter",
        color_continuous_scale=px.colors.sequential.Plasma,
        opacity=0.75
    )
    
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
    st.plotly_chart(fig_map, use_container_width=True)
