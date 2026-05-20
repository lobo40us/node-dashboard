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
    
    # -----------------------------------------------------------------------------
    # BASE BACKGROUND MATRIX FIELDS (Plotted first so they sit underneath phenomena)
    # -----------------------------------------------------------------------------
    
    # 🌟 LAYER 1: Magnetic Anomalies (Emerald Outlines - Baseline Field)
    if show_mag and 'mag' in df.columns:
        mag_df = df[df['mag'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=mag_df[lat_col],
            lon=mag_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=3,
                color='#00FF66',  # Emerald Green
                opacity=0.35
            ),
            name="Magnetic Anomalies",
            text=[f"Mag Anomaly: {v:.1f} nT" for v in mag_df['mag']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 2: Ancient Sacred Sites (Continuous Matrix Layer via Opacity Scaling)
    if show_anc and 'anc' in df.columns:
        anc_df = df[df['anc'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=anc_df[lat_col],
            lon=anc_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=4,  # Small uniform size isolates individual 1x1 degree cells
                color=anc_df['anc'],
                colorscale=[
                    [0.0, 'rgba(255, 0, 255, 0.0)'],   # Zero neighbor weight = transparent
                    [0.2, 'rgba(255, 0, 255, 0.2)'],   # Low background presence
                    [0.6, 'rgba(255, 0, 255, 0.5)'],   # Medium field concentration
                    [1.0, 'rgba(255, 0, 255, 0.95)']   # Core sacred site node proximity
                ],
                showscale=False
            ),
            name="Ancient Sites Field",
            text=[f"Ancient Intensity: {v:.2f}" for v in anc_df['anc']],
            hoverinfo='text'
        ))
        
    # 🌟 LAYER 3: Nuclear Infrastructure (Exponential Decay Field via Opacity Scaling)
    if show_nuc and 'nuc' in df.columns:
        nuc_df = df[df['nuc'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=nuc_df[lat_col],
            lon=nuc_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=4,  # Lock size small to stop continental color-bleeding completely
                color=nuc_df['nuc'],
                colorscale=[
                    [0.0, 'rgba(0, 255, 255, 0.0)'],   # Faded peripheral edge
                    [0.15, 'rgba(0, 255, 255, 0.25)'], # Falling contour field
                    [0.5, 'rgba(0, 255, 255, 0.55)'],  # Ascending proximity field
                    [1.0, 'rgba(0, 255, 255, 0.95)']   # Solid active reactor core node
                ],
                showscale=True,
                colorbar=dict(
                    title="Nuc Decay Contour",
                    thickness=12,
                    len=0.4,
                    x=1.01,
                    tickfont=dict(color="white", size=9),
                    titlefont=dict(color="white", size=10)
                )
            ),
            name="Nuclear Decay Contours",
            text=[f"Decay Contour Score: {v:.3f}" for v in nuc_df['nuc']],
            hoverinfo='text'
        ))

    # -----------------------------------------------------------------------------
    # PHENOMENA POINT OVERLAYS (Plotted last to pierce sharply through base grids)
    # -----------------------------------------------------------------------------

    # 🌟 LAYER 4: UAP Events (Electric Orange Sharp Points)
    if show_uap and 'uap' in df.columns:
        uap_df = df[df['uap'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=uap_df[lat_col],
            lon=uap_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=uap_df['uap'].clip(3, 10),  # Scaled safely to remain legible
                color='#FFAA00',  # Solid High-Contrast Electric Orange
                opacity=0.9
            ),
            name="UAP Sightings",
            text=[f"UAP Count: {v}" for v in uap_df['uap']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 5: USO Submerged Events (Deep Teal Blue Marine Points)
    if show_uso and 'uso' in df.columns:
        uso_df = df[df['uso'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=uso_df[lat_col],
            lon=uso_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=uso_df['uso'].clip(3, 10),
                color='#00CCFF',  # Electric Sea Teal
                opacity=0.9
            ),
            name="USO Events",
            text=[f"USO Count: {v}" for v in uso_df['uso']],
            hoverinfo='text'
        ))

    # 📱 OPTIMIZED VIEWPORT DESIGN FOR MOBILE DEPLOYMENT
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center={"lat": 38.0, "lon": -95.0},  # Centered cleanly on North America matrix
            zoom=2.3  # Tailored default starting scale for tablet/phone screens
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=680,
        showlegend=True,
        legend=dict(
            orientation="h",       # Horizontal orientation stacks flawlessly on small screens
            yanchor="bottom",
            y=0.01,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(10,10,10,0.85)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(color="white", size=9)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
