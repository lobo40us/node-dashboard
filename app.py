import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="NODE Thesis Dashboard", layout="wide")
st.title("🛰️ NODE Spatial Analysis Dashboard")

# Read local file from repo workspace
grid_path = "node_thesis_grid.csv"

@st.cache_data
def load_mesh_matrix():
    if os.path.exists(grid_path):
        return pd.read_csv(grid_path)
    return pd.DataFrame()

df = load_mesh_matrix()

if df.empty:
    st.error("Matrix data layer unavailable. Please ensure node_thesis_grid.csv is present in the repository.")
else:
    # Sidebar selection panel mapping to your exact short column names
    st.sidebar.header("Visualization Layer")
    layer_choice = st.sidebar.selectbox(
        "Select Active Vector Layer:",
        [
            "UAP Events", 
            "USO (Submerged) Events",
            "Ancient Sacred Sites", 
            "Anthropogenic Nuclear Infrastructure",
            "Magnetic Anomalies",
            "Population Density"
        ]
    )
    
    # Aligned key dictionary matching your exact CSV headers
    column_mapping = {
        "UAP Events": "uap",
        "USO (Submerged) Events": "uso",
        "Ancient Sacred Sites": "anc",
        "Anthropogenic Nuclear Infrastructure": "nuc",
        "Magnetic Anomalies": "mag",
        "Population Density": "pop"
    }
    active_column = column_mapping[layer_choice]
    
    # Identify longitudinal layout keys ('lng' vs 'lon')
    lon_col = 'lng' if 'lng' in df.columns else 'lon'
    lat_col = 'lat'
    
    # Clean zeros to keep rendering tight and crisp on mobile
    filtered_df = df[df[active_column] > 0].copy()
    
    st.subheader(f"Global Density Surface: {layer_choice}")
    
    # Render using the smooth density mapbox engine
    fig_map = px.density_mapbox(
        filtered_df, 
        lat=lat_col, 
        lon=lon_col, 
        z=active_column,
        radius=15,          # Dense blending radius for continuous global layout
        center={"lat": 20.0, "lon": 0.0}, 
        zoom=1.2,
        mapbox_style="carto-darkmatter",
        color_continuous_scale=px.colors.sequential.Plasma,
        opacity=0.80
    )
    
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
    st.plotly_chart(fig_map, use_container_width=True)
