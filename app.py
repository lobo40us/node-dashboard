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
    
    # 📱 Mobile Viewport Optimization Control
    st.sidebar.markdown("---")
    st.sidebar.subheader("📱 Performance Engine")
    view_scale = st.sidebar.radio("Map Zoom Scale:", ["🌍 Global View (Optimized)", "🔍 Regional Zoom (100% Detail)"], index=0)
    
    st.sidebar.markdown("---")
    # Independent checkboxes for true multi-layer stacking
    show_uap = st.sidebar.checkbox("🛸 UAP Events", value=True)
    show_uso = st.sidebar.checkbox("🌊 USO (Submerged) Events", value=False)
    show_anc = st.sidebar.checkbox("🏛️ Ancient Sacred Sites", value=True)
    show_nuc = st.sidebar.checkbox("⚛️ Nuclear Infrastructure", value=False)
    show_mag = st.sidebar.checkbox("🧲 Magnetic Anomalies", value=False)
    show_conv = st.sidebar.checkbox("🔴 High Convergence (3+ Layers)", value=True)
    
    # Stochastic Downsampling to preserve spatial integrity without grid striping
    if view_scale == "🌍 Global View (Optimized)":
        render_df = df.sample(frac=0.33, random_state=42).copy().reset_index(drop=True)
        current_zoom = 1.8
        marker_size = 3
    else:
        render_df = df.copy()
        current_zoom = 3.5
        marker_size = 4

    lon_col = 'lng' if 'lng' in render_df.columns else 'lon'
    lat_col = 'lat'
    
    fig = go.Figure()
    
    # -----------------------------------------------------------------------------
    # HELPER FUNCTION: Native Discrete Color Mapper (Bypasses Plotly Shading Bug)
    # -----------------------------------------------------------------------------
    def calculate_discrete_colors(series, base_rgba, peak_rgba_list, thresholds):
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
    # UNBROKEN GLOBAL GRID MATRIX LAYERS (Discrete Color Framework)
    # -----------------------------------------------------------------------------
    
    # 🌟 LAYER 1: Magnetic Anomalies (EMAG2v3 Calibrated Metrics)
    if show_mag and 'mag' in render_df.columns:
        mag_thresholds = [68.84, 200.0]  # Q75 and ~Q90 distribution boundaries
        mag_colors = calculate_discrete_colors(
            render_df['mag'], 'rgba(255, 255, 255, 0.04)', 
            ['rgba(0, 255, 102, 0.3)', 'rgba(0, 255, 102, 0.6)', 'rgba(0, 255, 102, 0.9)'], 
            mag_thresholds
        )
        fig.add_trace(go.Scattermapbox(
            lat=render_df[lat_col], lon=render_df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=marker_size, color=mag_colors),
            name="Magnetic Anomalies",
            text=[f"Mag: {v:.1f} nT" if pd.notna(v) else "Mag: 0" for v in render_df['mag']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 2: Ancient Sacred Sites (Purple/Magenta Mesh)
    if show_anc and 'anc' in render_df.columns:
        anc_colors = calculate_discrete_colors(
            render_df['anc'], 'rgba(255, 255, 255, 0.08)', 
            ['rgba(210, 0, 255, 0.3)', 'rgba(255, 0, 255, 0.6)', 'rgba(255, 0, 255, 0.95)'], 
            [1.0, 5.0]
        )
        fig.add_trace(go.Scattermapbox(
            lat=render_df[lat_col], lon=render_df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=marker_size, color=anc_colors),
            name="Ancient Sites Field",
            text=[f"Ancient Intensity: {v:.2f}" if pd.notna(v) else "Ancient: 0" for v in render_df['anc']],
            hoverinfo='text'
        ))
        
    # 🌟 LAYER 3: Nuclear Infrastructure (Facility Cluster Calibrated Metrics)
    if show_nuc and 'nuc' in render_df.columns:
        nuc_thresholds = [0.5, 2.0]  # Isolated boundaries vs dense industrial clusters
        nuc_colors = calculate_discrete_colors(
            render_df['nuc'], 'rgba(255, 255, 255, 0.04)', 
            ['rgba(0, 255, 255, 0.3)', 'rgba(0, 255, 255, 0.6)', 'rgba(0, 255, 255, 0.95)'], 
            nuc_thresholds
        )
        fig.add_trace(go.Scattermapbox(
            lat=render_df[lat_col], lon=render_df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=marker_size, color=nuc_colors),
            name="Nuclear Decay Contours",
            text=[f"Decay Score: {v:.3f}" if pd.notna(v) else "Decay: 0" for v in render_df['nuc']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 4: UAP Events (Electric Orange Mesh)
    if show_uap and 'uap' in render_df.columns:
        uap_colors = calculate_discrete_colors(
            render_df['uap'], 'rgba(255, 255, 255, 0.04)', 
            ['rgba(255, 170, 0, 0.35)', 'rgba(255, 170, 0, 0.65)', 'rgba(255, 170, 0, 0.95)'], 
            [1.0, 3.0]
        )
        fig.add_trace(go.Scattermapbox(
            lat=render_df[lat_col], lon=render_df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=marker_size, color=uap_colors),
            name="UAP Sightings Field",
            text=[f"UAP Count: {int(v)}" if pd.notna(v) else "UAP: 0" for v in render_df['uap']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 5: USO Submerged Events (Deep Teal Blue Mesh)
    if show_uso and 'uso' in render_df.columns:
        uso_colors = calculate_discrete_colors(
            render_df['uso'], 'rgba(255, 255, 255, 0.04)', 
            ['rgba(0, 204, 255, 0.3)', 'rgba(0, 204, 255, 0.6)', 'rgba(0, 204, 255, 0.95)'], 
            [1.0, 2.0]
        )
        fig.add_trace(go.Scattermapbox(
            lat=render_df[lat_col], lon=render_df[lon_col], mode='markers',
            marker=go.scattermapbox.Marker(size=marker_size, color=uso_colors),
            name="USO Events Field",
            text=[f"USO Count: {int(v)}" if pd.notna(v) else "USO: 0" for v in render_df['uso']],
            hoverinfo='text'
        ))

    # 🌟 LAYER 6: CORE SPATIAL SYNTHESIS (High Convergence Multi-Layer Intersection)
    if show_conv and 'layers' in render_df.columns:
        conv_df = render_df[render_df['layers'] >= 3].copy().reset_index(drop=True)
        if not conv_df.empty:
            fig.add_trace(go.Scattermapbox(
                lat=conv_df[lat_col], lon=conv_df[lon_col], mode='markers',
                marker=go.scattermapbox.Marker(
                    size=7,
                    color=['rgba(255, 50, 50, 0.9)' if v >= 4 else 'rgba(255, 170, 0, 0.85)'
                           for v in conv_df['layers']]
                ),
                name="High Convergence Nodes",
                text=[f"Convergence: {int(v)}/5 layers" for v in conv_df['layers']],
                hoverinfo='text'
            ))

    # 📱 VIEWPORT CONFIGURATIONS
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center={"lat": 40.0, "lon": -20.0} if view_scale == "🌍 Global View (Optimized)" else {"lat": 50.0, "lon": 10.0},
            zoom=current_zoom  
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

    # 🏛️ ACADEMIC RECORD PROVENANCE
    st.sidebar.markdown("---")
    st.sidebar.caption("Pre-registered research\nosf.io/a9w4k/ove\nKok & Kok — 2026")
