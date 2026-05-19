import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="NODE Thesis Dashboard", layout="wide")
st.title("🛰️ NODE Multi-Layer Convergence Dashboard")

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
    st.sidebar.header("Layer Visibility Control")
    st.sidebar.write("Toggle layers to analyze spatial co-location:")
    
    # Independent checkboxes for true multi-layer stacking
    show_uap = st.sidebar.checkbox("🛸 UAP Events", value=True)
    show_uso = st.sidebar.checkbox("🌊 USO (Submerged) Events", value=False)
    show_anc = st.sidebar.checkbox("🏛️ Ancient Sacred Sites", value=True)
    show_nuc = st.sidebar.checkbox("⚛️ Nuclear Infrastructure", value=False)
    show_mag = st.sidebar.checkbox("🧲 Magnetic Anomalies", value=False)
    
    lon_col = 'lng' if 'lng' in df.columns else 'lon'
    lat_col = 'lat'
    
    # Initialize a clean Plotly Graph Object Map
    fig = go.Figure()
    
    # 🌟 LAYER 1: Ancient Sacred Sites (Magenta Glow)
    if show_anc and 'anc' in df.columns:
        anc_df = df[df['anc'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=anc_df[lat_col],
            lon=anc_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=anc_df['anc'].clamp(1, 15) + 2,
                color='#FF00FF',  # Neon Magenta
                opacity=0.6,
                name='Ancient Sites'
            ),
            name="Ancient Sites",
            text=[f"Ancient Sites Intensity: {v}" for v in anc_df['anc']],
            hoverinfo='text'
        ))
        
    # 🌟 LAYER 2: Nuclear Infrastructure (Cyan Glow)
    if show_nuc and 'nuc' in df.columns:
        nuc_df = df[df['nuc'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=nuc_df[lat_col],
            lon=nuc_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=nuc_df['nuc'].clamp(1, 15) + 3,
                color='#00FFFF',  # Neon Cyan
                opacity=0.7,
            ),
            name="Nuclear Infra",
            text=[f"Nuclear Node Weight: {v}" for v in nuc_df['nuc']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 3: UAP Events (Electric Yellow/Orange Core)
    if show_uap and 'uap' in df.columns:
        uap_df = df[df['uap'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=uap_df[lat_col],
            lon=uap_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=uap_df['uap'].clamp(1, 12),
                color='#FFAA00',  # Electric Orange
                opacity=0.75,
            ),
            name="UAP Sightings",
            text=[f"UAP Count: {v}" for v in uap_df['uap']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 4: USO Submerged Events (Deep Electric Blue)
    if show_uso and 'uso' in df.columns:
        uso_df = df[df['uso'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=uso_df[lat_col],
            lon=uso_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=uso_df['uso'].clamp(1, 12),
                color='#0088FF',  # Deep Blue
                opacity=0.75,
            ),
            name="USO Events",
            text=[f"USO Count: {v}" for v in uso_df['uso']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 5: Magnetic Anomalies (Emerald Outlines)
    if show_mag and 'mag' in df.columns:
        mag_df = df[df['mag'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=mag_df[lat_col],
            lon=mag_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=4,
                color='#00FF66',  # Emerald Green
                opacity=0.4,
            ),
            name="Magnetic Anomalies",
            text=[f"Mag Anomaly: {v}" for v in mag_df['mag']],
            hoverinfo='text'
        ))

    # Set up global dark matter viewport configs
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center={"lat": 20.0, "lon": 0.0},
            zoom=1.1
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=700,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(10,10,10,0.7)",
            font=dict(color="white")
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
