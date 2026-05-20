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
    # HELPER FUNCTION: Native Discrete Color Mapper (Bypasses Plotly Shading Bug)
    # -----------------------------------------------------------------------------
    def calculate_discrete_colors(series, base_rgba, peak_rgba_list, thresholds):
        """
        Maps numerical values directly to explicit RGBA strings.
        This forces Plotly to render standalone markers without interpolating across ocean gaps.
        """
        filled = series.fillna(0)
        color_list = []
        for val in filled:
            if val <= 0:
                color_list.append(base_rgba)
            elif val <= thresholds[0]:
                color_list.append(peak_rgba_list[0])
            elif val <= thresholds[1]:
                color_list.append(peak_rgba_list[1])
            else:
                color_list.append(peak_rgba_list[2])
        return color_list

    # -----------------------------------------------------------------------------
    # UNBROKEN GLOBAL GRID MATRIX LAYERS (Using Explicit Pre-Computed Color Arrays)
    # -----------------------------------------------------------------------------
    
    # 🌟 LAYER 1: Magnetic Anomalies (Emerald Outlines Mesh)
    if show_mag and 'mag' in df.columns:
        mag_colors = calculate_discrete_colors(
            df['mag'], 
            'rgba(255, 255, 255, 0.05)', 
            ['rgba(0, 255, 102, 0.3)', 'rgba(0, 255, 102, 0.6)', 'rgba(0, 255, 102, 0.9)'],
            [2.0, 5.0]
        )
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=4, color=mag_colors),
            name="Magnetic Anomalies",
            text=[f"Mag Anomaly: {v:.1f} nT" if pd.notna(v) else "Mag: 0" for v in df['mag']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 2: Ancient Sacred Sites (Purple/Magenta Mesh)
    if show_anc and 'anc' in df.columns:
        anc_colors = calculate_discrete_colors(
            df['anc'], 
            'rgba(255, 255, 255, 0.12)', 
            ['rgba(210, 0, 255, 0.3)', 'rgba(255, 0, 255, 0.6)', 'rgba(255, 0, 255, 0.95)'],
            [1.0, 5.0]
        )
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=4, color=anc_colors),
            name="Ancient Sites Field",
            text=[f"Ancient Intensity: {v:.2f}" if pd.notna(v) else "Ancient: 0" for v in df['anc']],
            hoverinfo='text'
        ))
        
    # 🌟 LAYER 3: Nuclear Infrastructure (Cyan Mesh)
    if show_nuc and 'nuc' in df.columns:
        nuc_colors = calculate_discrete_colors(
            df['nuc'], 
            'rgba(255, 255, 255, 0.05)', 
            ['rgba(0, 255, 255, 0.3)', 'rgba(0, 255, 255, 0.6)', 'rgba(0, 255, 255, 0.95)'],
            [0.1, 0.5]
        )
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=4, color=nuc_colors),
            name="Nuclear Decay Contours",
            text=[f"Decay Contour Score: {v:.3f}" if pd.notna(v) else "Decay: 0" for v in df['nuc']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 4: UAP Events (Electric Orange Mesh - Discrete Array Transition)
    if show_uap and 'uap' in df.columns:
        uap_colors = calculate_discrete_colors(
            df['uap'], 
            'rgba(255, 255, 255, 0.05)', # Zero baseline points stay crisp light skeleton dots
            ['rgba(255, 170, 0, 0.35)', 'rgba(255, 170, 0, 0.65)', 'rgba(255, 170, 0, 0.95)'], # Discrete heat tiers
            [1.0, 3.0] # Sighting thresholds
        )
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=4, color=uap_colors),
            name="UAP Sightings Field",
            text=[f"UAP Count: {int(v)}" if pd.notna(v) else "UAP: 0" for v in df['uap']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 5: USO Submerged Events (Deep Teal Blue Mesh)
    if show_uso and 'uso' in df.columns:
        uso_colors = calculate_discrete_colors(
            df['uso'], 
            'rgba(255, 255, 255, 0.05)', 
            ['rgba(0, 204, 255, 0.3)', 'rgba(0, 204, 255, 0.6)', 'rgba(0, 204, 255, 0.95)'],
            [1.0, 2.0]
        )
        fig.add_trace(go.Scattermapbox(
            lat=df[lat_col], lon=df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=4, color=uso_colors),
            name="USO Events Field",
            text=[f"USO Count: {int(v)}" if pd.notna(v) else "USO: 0" for v in df['uso']],
            hoverinfo='text'
        ))

    # 📱 VIEWPORT CONFIGURATIONS
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center={"lat": 50.0, "lon": 10.0}, 
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
