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
    # UNBROKEN GLOBAL GRID MATRIX LAYERS (Shared Uniform Structural Mesh Layout)
    # -----------------------------------------------------------------------------
    
    # 🌟 LAYER 1: Magnetic Anomalies (Emerald Outlines Mesh)
    if show_mag and 'mag' in df.columns:
        has_variance = df['mag'].nunique() > 1
        if has_variance:
            mag_marker = go.scattermapbox.Marker(
                size=4,
                color=df['mag'].fillna(0),
                colorscale=[[0.0, 'rgba(255, 255, 255, 0.05)'], [1.0, 'rgba(0, 255, 102, 0.75)']],
                showscale=False
            )
        else:
            mag_marker = go.scattermapbox.Marker(size=4, color='rgba(0, 255, 102, 0.15)')

        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers', marker=mag_marker,
            name="Magnetic Anomalies",
            text=[f"Mag Anomaly: {v:.1f} nT" if pd.notna(v) else "Mag: 0" for v in df['mag']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 2: Ancient Sacred Sites (Magenta Mesh)
    if show_anc and 'anc' in df.columns:
        has_variance = df['anc'].nunique() > 1
        if has_variance:
            anc_marker = go.scattermapbox.Marker(
                size=4,
                color=df['anc'].fillna(0),
                colorscale=[
                    [0.0, 'rgba(255, 255, 255, 0.12)'], 
                    [0.1, 'rgba(210, 0, 255, 0.3)'],   
                    [0.5, 'rgba(255, 0, 255, 0.6)'],   
                    [1.0, 'rgba(255, 0, 255, 0.95)']   
                ],
                showscale=False
            )
        else:
            anc_marker = go.scattermapbox.Marker(size=4, color='rgba(255, 0, 255, 0.15)')

        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers', marker=anc_marker,
            name="Ancient Sites Field",
            text=[f"Ancient Intensity: {v:.2f}" if pd.notna(v) else "Ancient: 0" for v in df['anc']],
            hoverinfo='text'
        ))
        
    # 🌟 LAYER 3: Nuclear Infrastructure (Cyan Mesh - Definitively Bypassing Plotly Bug)
    if show_nuc and 'nuc' in df.columns:
        has_variance = df['nuc'].nunique() > 1
        
        if has_variance:
            fig.add_trace(go.Scattermapbox(
                lat=df[lat_col], lon=df[lon_col], mode='markers',
                marker=go.scattermapbox.Marker(
                    size=4,
                    color=df['nuc'].fillna(0),
                    colorscale=[
                        [0.0, 'rgba(255, 255, 255, 0.05)'], 
                        [0.15, 'rgba(0, 255, 255, 0.3)'],  
                        [0.6, 'rgba(0, 255, 255, 0.6)'],   
                        [1.0, 'rgba(0, 255, 255, 0.95)']   
                    ],
                    showscale=True,
                    colorbar=dict(
                        title="Nuc Decay Contour", thickness=12, len=0.4, x=1.01,
                        tickfont=dict(color="white", size=9), titlefont=dict(color="white", size=10)
                    )
                ),
                name="Nuclear Decay Contours",
                text=[f"Decay Contour Score: {v:.3f}" if pd.notna(v) else "Decay: 0" for v in df['nuc']],
                hoverinfo='text'
            ))
        else:
            # Clean uniform fallback if data is flat zero: absolutely no colorbar or colorscale declarations to trigger crashes
            fig.add_trace(go.Scattermapbox(
                lat=df[lat_col], lon=df[lon_col], mode='markers',
                marker=go.scattermapbox.Marker(
                    size=4,
                    color='rgba(0, 255, 255, 0.15)'  # Safe, uniform structural mesh color placeholder
                ),
                name="Nuclear Decay Contours",
                text=["Decay: 0" for _ in range(len(df))],
                hoverinfo='text'
            ))

    # 🌟 LAYER 4: UAP Events (Electric Orange Mesh)
    if show_uap and 'uap' in df.columns:
        has_variance = df['uap'].nunique() > 1
        if has_variance:
            uap_marker = go.scattermapbox.Marker(
                size=4,
                color=df['uap'].fillna(0),
                colorscale=[
                    [0.0, 'rgba(255, 255, 255, 0.05)'], 
                    [0.2, 'rgba(255, 170, 0, 0.3)'],   
                    [0.6, 'rgba(255, 170, 0, 0.6)'],   
                    [1.0, 'rgba(255, 170, 0, 0.95)']   
                ],
                showscale=False
            )
        else:
            uap_marker = go.scattermapbox.Marker(size=4, color='rgba(255, 170, 0, 0.15)')

        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers', marker=uap_marker,
            name="UAP Sightings Field",
            text=[f"UAP Count: {int(v)}" if pd.notna(v) else "UAP: 0" for v in df['uap']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 5: USO Submerged Events (Deep Teal Blue Mesh)
    if show_uso and 'uso' in df.columns:
        has_variance = df['uso'].nunique() > 1
        if has_variance:
            uso_marker = go.scattermapbox.Marker(
                size=4,
                color=df['uso'].fillna(0),
                colorscale=[
                    [0.0, 'rgba(255, 255, 255, 0.05)'], 
                    [0.2, 'rgba(0, 204, 255, 0.3)'],   
                    [0.6, 'rgba(0, 204, 255, 0.6)'],   
                    [1.0, 'rgba(0, 204, 255, 0.95)']   
                ],
                showscale=False
            )
        else:
            uso_marker = go.scattermapbox.Marker(size=4, color='rgba(0, 204, 255, 0.15)')

        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers', marker=uso_marker,
            name="USO Events Field",
            text=[f"USO Count: {int(v)}" if pd.notna(v) else "USO: 0" for v in df['uso']],
            hoverinfo='text'
        ))

    # 📱 VIEWPORT CONFIGURATIONS
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center={"lat": 50.0, "lon": 10.0},  # Europe center
            zoom=3.2  
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=680,
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=0.01, xanchor="center", x=0.5,
            bgcolor="rgba(10,10,10,0.85)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
            font=dict(color="white", size=9)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
