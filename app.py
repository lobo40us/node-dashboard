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
    # BASE BACKGROUND MATRIX FIELDS (Unbroken Grid Structure)
    # -----------------------------------------------------------------------------
    
    # 🌟 LAYER 1: Magnetic Anomalies (Emerald Outlines - Baseline Field)
    if show_mag and 'mag' in df.columns:
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col],
            lon=df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=3,
                color=df['mag'].fillna(0),
                colorscale=[
                    [0.0, 'rgba(0, 255, 102, 0.0)'],
                    [1.0, 'rgba(0, 255, 102, 0.6)']
                ],
                showscale=False
            ),
            name="Magnetic Anomalies",
            text=[f"Mag Anomaly: {v:.1f} nT" if pd.notna(v) else "Mag: 0" for v in df['mag']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 2: Ancient Sacred Sites (Unbroken Grid Mesh)
    if show_anc and 'anc' in df.columns:
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col],
            lon=df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=4,  # Sharp uniform grid nodes
                color=df['anc'].fillna(0),
                colorscale=[
                    [0.0, 'rgba(255, 255, 255, 0.12)'], # Zero nodes show up as a faint white structural mesh point
                    [0.1, 'rgba(210, 0, 255, 0.3)'],   
                    [0.5, 'rgba(255, 0, 255, 0.6)'],   # Clear signal presence
                    [1.0, 'rgba(255, 0, 255, 0.95)']   # Maximum intensity node
                ],
                showscale=False
            ),
            name="Ancient Sites Field",
            text=[f"Ancient Intensity: {v:.2f}" if pd.notna(v) else "Ancient: 0" for v in df['anc']],
            hoverinfo='text'
        ))
        
    # 🌟 LAYER 3: Nuclear Infrastructure (Unbroken Decay Field)
    if show_nuc and 'nuc' in df.columns:
        # Verify if column contains actual valid computed variances to pass to colorbar
        has_variance = df['nuc'].nunique() > 1 if 'nuc' in df.columns else False
        
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col],
            lon=df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=4,
                color=df['nuc'].fillna(0),
                colorscale=[
                    [0.0, 'rgba(255, 255, 255, 0.05)'], 
                    [0.15, 'rgba(0, 255, 255, 0.3)'],  
                    [0.6, 'rgba(0, 255, 255, 0.6)'],   
                    [1.0, 'rgba(0, 255, 255, 0.95)']   
                ],
                showscale=True if has_variance else False,
                colorbar=dict(
                    title="Nuc Decay Contour",
                    thickness=12,
                    len=0.4,
                    x=1.01,
                    tickfont=dict(color="white", size=9),
                    titlefont=dict(color="white", size=10)
                ) if has_variance else None # Safe dynamic configuration to block runtime ValueError drops
            ),
            name="Nuclear Decay Contours",
            text=[f"Decay Contour Score: {v:.3f}" if pd.notna(v) else "Decay: 0" for v in df['nuc']],
            hoverinfo='text'
        ))

    # -----------------------------------------------------------------------------
    # PHENOMENA POINT OVERLAYS (Sharp Points Mounted Above the Grid)
    # -----------------------------------------------------------------------------

    # 🌟 LAYER 4: UAP Events (Electric Orange Sharp Points)
    if show_uap and 'uap' in df.columns:
        uap_df = df[df['uap'] > 0]
        fig.add_trace(go.Scattermapbox(
            lat=uap_df[lat_col],
            lon=uap_df[lon_col],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=uap_df['uap'].clip(4, 10),  
                color='#FFAA00',  
                opacity=0.95
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
                size=uso_df['uso'].clip(4, 10),
                color='#00CCFF',  
                opacity=0.95
            ),
            name="USO Events",
            text=[f"USO Count: {v}" for v in uso_df['uso']],
            hoverinfo='text'
        ))

    # 📱 VIEWPORT CENTERED DIRECTLY ON EUROPE FOR INSTANT LOADING
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center={"lat": 50.0, "lon": 10.0},  # Perfect default framing for your active matrix
            zoom=3.2  
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=680,
        showlegend=True,
        legend=dict(
            orientation="h",       
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
