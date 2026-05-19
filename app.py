import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

st.set_page_config(page_title="NODE Thesis Dashboard", layout="wide")
st.title("🛰️ NODE Spatial Analysis Dashboard")

grid_path = "node_thesis_grid.csv"

@st.cache_data
def load_mesh_matrix():
    if os.path.exists(grid_path):
        return pd.read_csv(grid_path)
    return pd.DataFrame()

df = load_mesh_matrix()

if df.empty:
    st.error("Matrix data layer unavailable.")
else:
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
    
    column_mapping = {
        "UAP Events": "uap",
        "USO (Submerged) Events": "uso",
        "Ancient Sacred Sites": "anc",
        "Anthropogenic Nuclear Infrastructure": "nuc",
        "Magnetic Anomalies": "mag",
        "Population Density": "pop"
    }
    active_column = column_mapping[layer_choice]
    
    lon_col = 'lng' if 'lng' in df.columns else 'lon'
    lat_col = 'lat'
    
    # Filter out absolute zeros
    filtered_df = df[df[active_column] > 0].copy()
    
    # Apply a gentle logarithmic smoothing scaling factor to prevent massive blowouts
    filtered_df['scaled_intensity'] = np.log1p(filtered_df[active_column])
    
    st.subheader(f"Global Density Surface: {layer_choice}")
    
    # High-precision density configuration
    fig_map = px.density_mapbox(
        filtered_df, 
        lat=lat_col, 
        lon=lon_col, 
        z='scaled_intensity',
        radius=6,                   # Tightened to prevent massive continental bleeding
        center={"lat": 20.0, "lon": 0.0}, 
        zoom=1.2,
        mapbox_style="carto-darkmatter",
        color_continuous_scale=px.colors.sequential.Inferno, # Elegant dark-mode gradient
        opacity=0.65,               # Lowered slightly to allow underlying map text visibility
        hover_data={lat_col: False, lon_col: False, 'scaled_intensity': False, active_column: True}
    )
    
    fig_map.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, 
        height=650,
        coloraxis_showscale=False   # Clears the heavy colorbar for a cleaner mobile layout
    )
    st.plotly_chart(fig_map, use_container_width=True)
