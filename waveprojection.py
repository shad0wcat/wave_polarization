import streamlit as st
import numpy as np
import plotly.graph_objs as go
from PIL import Image
import io
import os

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="3D Polarization Wave", layout="wide")

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------
st.sidebar.header(" ")

# Load logo
logo_path = os.path.join(os.path.dirname(__file__), "assets", "mrslab.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    logo = None  # Prevents app crash if file is missing
st.sidebar.image(logo, use_column_width=True)
st.sidebar.markdown("---")

# User Inputs
orientation_deg = st.sidebar.slider("Orientation Angle (°)", 0, 180, 45, step=1)
phase_deg = st.sidebar.slider("Phase Difference δ (°)", -180, 180, 0, step=1)

st.sidebar.markdown("---")


# ----------------------------------------------------------
# CAMERA & WAVE DEFINITIONS
# ----------------------------------------------------------
def compute_eye(azimuth_deg, elevation_deg, radius):
    az = np.radians(azimuth_deg)
    el = np.radians(elevation_deg)
    x = radius * np.cos(el) * np.cos(az)
    y = radius * np.cos(el) * np.sin(az)
    z = radius * np.sin(el)
    return dict(x=x, y=y, z=z)

az = 165
el = 30
r = 2.75

camera = dict(
    eye=compute_eye(az, el, r),
    up=dict(x=0, y=1, z=0)
)

# --- Wave Parameters ---
num_cycles = 7
wavelength = 1.5
L = num_cycles * wavelength
z = np.linspace(0, L, 1000)

orientation_rad = np.radians(orientation_deg)
delta = np.radians(phase_deg)     # <<--- DIRECT PHASE DIFFERENCE INPUT

# Field components
Ax = np.cos(orientation_rad)
Ay = np.sin(orientation_rad)

omega = 2 * np.pi / wavelength
Ex = Ax * np.cos(omega * z)
Ey = Ay * np.cos(omega * z + delta)


# ----------------------------------------------------------
# 3D WALLS & WAVE
# ----------------------------------------------------------
wall_offset = -2.5

# YZ Wall
y_vals = np.linspace(-1.5, 1.5, 2)
z_vals = np.linspace(0, L, 2)
floor = go.Surface(
    x=np.full((2, 2), -(wall_offset)),
    y=np.outer(y_vals, np.ones_like(z_vals)),
    z=np.outer(np.ones_like(y_vals), z_vals),
    colorscale=[[0, 'lightgray'], [1, 'lightgray']],
    showscale=False,
    opacity=0.5
)

# XZ Wall
x_vals = np.linspace(-1.5, 1.5, 2)
back_wall = go.Surface(
    x=np.outer(x_vals, np.ones_like(z_vals)),
    y=np.full((2, 2), wall_offset),
    z=np.outer(np.ones_like(x_vals), z_vals),
    colorscale=[[0, 'lightgray'], [1, 'lightgray']],
    showscale=False,
    opacity=0.5
)

# Main wave
wave = go.Scatter3d(
    x=Ex,
    y=Ey,
    z=z,
    mode='lines',
    line=dict(color='rgb(191, 0, 0)', width=7),
)

# Projection on XZ
proj_xz = go.Scatter3d(
    x=Ex,
    y=np.full_like(z, wall_offset),
    z=z,
    mode='lines',
    line=dict(color='red', width=3)
)

# Projection on YZ
proj_yz = go.Scatter3d(
    x=np.full_like(z, -wall_offset),
    y=Ey,
    z=z,
    mode='lines',
    line=dict(color='green', width=3)
)

layout = go.Layout(
    scene=dict(
        xaxis=dict(showgrid=True, range=[-2.6, 2.6]),
        yaxis=dict(showgrid=True, range=[-2.6, 2.6]),
        zaxis=dict(showgrid=True, range=[0, L]),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=2.5),
        camera=camera
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=800,
    width=1400
)

fig = go.Figure(
    data=[floor, back_wall, wave, proj_xz, proj_yz],
    layout=layout
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


# ----------------------------------------------------------
# MAIN LAYOUT
# ----------------------------------------------------------
col1, col2 = st.columns([4, 3])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Wave Parameters")
    st.metric("Orientation Angle", f"{orientation_deg}°")
    st.metric("Phase Difference δ", f"{phase_deg}°")




