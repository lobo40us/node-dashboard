# 🛰️ STREAMLIT DASHBOARD: MAIN APP FRAMEWORK (app.py)
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import os

st.set_page_config(layout="wide", page_title="Node Thesis Dashboard", page_icon="🛰️")

# Title & Headings linked to OSF pre-registration metadata
st.title("🛰️ The Node Thesis Dashboard")
st.caption("Empirical Spatial Analysis of Global Anomalous Phenomena | Kok & Kok — 2026")
st.markdown("[OSF Pre-Registration: a9w4k/ove](https://osf.io/a9w4k/ove)")

# 📥 Load Data Pipeline (Handles both Colab Local and Streamlit Cloud environments)
@st.cache_data
def load_grid_data():
    if os.path.exists("node_thesis_grid.csv"):
        file_path = "node_thesis_grid.csv"
    else:
        file_path = "/content/drive/MyDrive/Node/node_thesis_grid.csv"
        
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Failed to load master dataset: {e}")
        return None

df_raw = load_grid_data()

if df_raw is not None:
    df = df_raw.copy()
    
    # 🎛️ SIDEBAR CONTROLS
    st.sidebar.header("📊 Analytical Controls")
    
    # Toggle 1: Normalization Method
    data_mode = st.sidebar.radio(
        "Normalization Matrix:",
        ["Raw Incident Counts", "Population-Corrected Signals"]
    )
    
    # Track status of newly engineered columns to prevent runtime KeyErrors
    has_corrected_cols = 'uap_corrected' in df.columns and 'uso_corrected' in df.columns
    has_gradient_col = 'mag_gradient' in df.columns
    
    # Assign mapping columns based on toggle selection with defensive fallbacks
    if data_mode == "Population-Corrected Signals":
        if has_corrected_cols:
            uap_col, uso_col = 'uap_corrected', 'uso_corrected'
            uap_active = df[uap_col] > df[uap_col].quantile(0.85)
            uso_active = df[uso_col] > df[uso_col].quantile(0.95)
        else:
            st.sidebar.warning("⚠️ Corrected attributes missing from the current CSV. Falling back to Raw Counts.")
            uap_col, uso_col = 'uap', 'uso'
            uap_active = df[uap_col] > 0
            uso_active = df[uso_col] > 0
    else:
        uap_col, uso_col = 'uap', 'uso'
        uap_active = df[uap_col] > 0
        uso_active = df[uso_col] > 0

    # Toggle 2: Environmental Layers
    st.sidebar.subheader("🌐 Biophysical Layers")
    show_nuc = st.sidebar.checkbox("Nuclear Proximity Zones (≥ 0.5)", value=True)
    show_anc = st.sidebar.checkbox("Ancient Sacred Sites", value=True)
    show_grad = st.sidebar.checkbox("Geomagnetic Gradient Edges", value=True)

    # 🗺️ MAP ENGINE SETUP
    st.sidebar.subheader("🗺️ Rendering Viewports")
    view_mode = st.sidebar.selectbox("Select Viewport Focus:", ["Global Overview", "Regional Zoom (MT/WY)"])
    
    if view_mode == "Global Overview":
        initial_view = pdk.ViewState(latitude=20.0, longitude=0.0, zoom=1.3, pitch=30)
        map_data = df.sample(n=min(15000, len(df)), random_state=42)
    else:
        initial_view = pdk.ViewState(latitude=45.5, longitude=-108.5, zoom=5.5, pitch=45)
        map_data = df[(df['lat'].between(41.0, 49.0)) & (df['lng'].between(-112.0, -104.0))]

    # 🎨 Layer Construction Matrix
    layers = []

    # 1. Nuclear Layer (Purple)
    if show_nuc:
        nuc_cells = map_data[map_data['nuc'].fillna(0) >= 0.5]
        layers.append(pdk.Layer(
            "ScatterplotLayer", nuc_cells,
            get_position=["lng", "lat"], get_color=[147, 51, 234, 140],
            get_radius=28000 if view_mode == "Global Overview" else 8000,
            pickable=True
        ))

    # 2. Ancient Sacred Sites Layer (Emerald)
    if show_anc:
        anc_cells = map_data[map_data['anc'].fillna(0) > 0]
        layers.append(pdk.Layer(
            "ScatterplotLayer", anc_cells,
            get_position=["lng", "lat"], get_color=[16, 185, 129, 140],
            get_radius=25000 if view_mode == "Global Overview" else 7500,
            pickable=True
        ))

    # 3. Geomagnetic Gradient Vector Contour Layer (Hot Orange)
    if show_grad:
        if has_gradient_col:
            grad_cells = map_data[map_data['mag_gradient'] >= 10.0]
            layers.append(pdk.Layer(
                "ScatterplotLayer", grad_cells,
                get_position=["lng", "lat"], get_color=[249, 115, 22, 120],
                get_radius=22000 if view_mode == "Global Overview" else 6500,
                pickable=True
            ))
        else:
            st.sidebar.warning("⚠️ 'mag_gradient' column missing from data file. Push updated CSV to GitHub.")

    # 4. Active Incident Clusters (Teal Rings)
    incident_cells = map_data[uap_active | uso_active]
    layers.append(pdk.Layer(
        "ScatterplotLayer", incident_cells,
        get_position=["lng", "lat"], get_color=[6, 182, 212, 225],
        get_radius=35000 if view_mode == "Global Overview" else 10000,
        stroked=True, filled=False, lw=3, pickable=True
    ))

    # Render DeckGL Object
    tooltip_text = "Lat: {lat}\nLng: {lng}" + ("\nMag Gradient: {mag_gradient:.2f}" if has_gradient_col else "")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v11",
        initial_view_state=initial_view,
        layers=layers,
        tooltip={"text": tooltip_text}
    ))

    # 📊 LIVE METRIC COUNTERS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Selected Grid Nodes", value=f"{len(map_data):,}")
    with col2:
        st.metric(label="Active Sighting Vectors", value=f"{(uap_active | uso_active).sum():,}")
    with col3:
        high_convergence_count = ((df['mag'].fillna(0) >= 68.84) & 
                                  (df['nuc'].fillna(0) >= 0.5) & 
                                  (df['anc'].fillna(0) > 0)).sum()
        st.metric(label="True 3+ Layer High Convergence Nodes", value=f"{high_convergence_count:,}")
