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
ellipticity_deg = st.sidebar.slider("Ellipticity Angle (°)", -45, 45, 0, step=1)
orientation_deg = st.sidebar.slider("Orientation Angle (°)", 0, 180, 45, step=1)


st.sidebar.markdown("---")


def compute_eye(azimuth_deg, elevation_deg, radius):
    az = np.radians(azimuth_deg)
    el = np.radians(elevation_deg)
    x = radius * np.cos(el) * np.cos(az)
    y = radius * np.cos(el) * np.sin(az)
    z = radius * np.sin(el)
    return dict(x=x, y=y, z=z)
# az = st.slider("Azimuth", 0, 360, 45)
# el = st.slider("Elevation", -90, 90, 30)
# r = st.slider("Distance", 1.0, 5.0, 2.0)

az = 165
el = 30
r = 2.75

camera = dict(
    eye=compute_eye(az, el, r),
    up=dict(x=0, y=1, z=0)
)


# --- Wave parameters ---
num_cycles = 7
wavelength = 1.5
L = num_cycles * wavelength  # Total wave length
z = np.linspace(0, L, 1000)
num_points = 1000
z = np.linspace(0, L, num_points)
# --- Sliders for orientation and ellipticity ---
# ellipticity_deg = st.slider("Ellipticity Angle (°)", -45, 45, 0, step=1)
# orientation_deg = st.slider("Orientation Angle (°)", 0, 180, 45, step=1)

# --- Derived parameters ---
orientation_rad = np.radians(orientation_deg)
#delta = 2 * np.radians(ellipticity_deg)  # Left/right handedness

epsilon = 1e-6
delta = np.arctan( np.tan(2 * np.radians(ellipticity_deg)) / (np.sin(2 * np.radians(orientation_deg)) + epsilon) )

st.markdown(f"**Phase Difference (δ)**: {2*ellipticity_deg:.3f} degrees")

Ax = np.cos(orientation_rad)
Ay = np.sin(orientation_rad)

# Time array
omega = 2 * np.pi / wavelength
Ex = Ax * np.cos(omega * z)
Ey = Ay * np.cos(omega * z + delta)

# --- Wall offsets ---
wall_offset = -2.5  # both walls at -1.5

# --- Floor wall (YZ) at x = -1.5
y_vals = np.linspace(-1.5, 1.5, 2)
z_vals = np.linspace(0, L, 2)
floor = go.Surface(
    x=np.full((2, 2), -(wall_offset)),  # X = -1.5
    y=np.outer(y_vals, np.ones_like(z_vals)),
    z=np.outer(np.ones_like(y_vals), z_vals),
    colorscale=[[0, 'lightgray'], [1, 'lightgray']],
    showscale=False,
    opacity=0.5,
    name='YZ Floor Wall'
)

# --- Back wall (XZ) at y = -1.5
x_vals = np.linspace(-1.5, 1.5, 2)
back_wall = go.Surface(
    x=np.outer(x_vals, np.ones_like(z_vals)),
    y=np.full((2, 2), wall_offset),  # Y = -1.5
    z=np.outer(np.ones_like(x_vals), z_vals),
    colorscale=[[0, 'lightgray'], [1, 'lightgray']],
    showscale=False,
    opacity=0.5,
    name='XZ Back Wall'
)

# --- Main 3D wave
wave = go.Scatter3d(
    x=Ex,
    y=Ey,
    z=z,
    mode='lines',
    line=dict(color='rgb(191, 0, 0)', width=7),  # maroon in RGB
    name='Circular Wave'
)
#
# --- Projection on XZ wall (X component), y = -1.5
proj_xz = go.Scatter3d(
    x=Ex,
    y=np.full_like(z, (wall_offset)),  # push to back wall
    z=z,
    mode='lines',
    line=dict(color='red', width=2),
    name='X Component'
)

# --- Projection on YZ wall (Y component), x = -1.5
proj_yz = go.Scatter3d(
    x=np.full_like(z, -(wall_offset)),  # push to floor wall
    y=Ey,
    z=z,
    mode='lines',
    line=dict(color='green', width=2),
    name='Y Component'
)

# --- Camera: view from front-right
# camera = dict(
#     eye=camera_eye(angle_y_deg=30, angle_z_deg=45),
#     up=dict(x=0, y=1, z=0),
#     center=dict(x=0, y=0, z=0)
# )
layout = go.Layout(
    scene=dict(
        xaxis=dict(showgrid=True,  zeroline=True,showticklabels=True, range=[-2.6, 2.6]),
        yaxis=dict(showgrid=True, zeroline=True, showticklabels=True, range=[-2.6, 2.6]),
        zaxis=dict(showgrid=True, zeroline=True, showticklabels=True, range=[0, L]),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=2.5),  # or 3.0 for even more width
        camera=camera  # Your custom default view
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=800,  #  Explicit vertical size
    width=1400  #  Explicit horizontal size
)
fig = go.Figure(
    #data=[ wave],
    data=[floor, back_wall, wave, proj_xz, proj_yz],
    layout=layout
)
st.plotly_chart(fig)


# Make background transparent
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis=dict(backgroundcolor='rgba(0,0,0,0)'),
        yaxis=dict(backgroundcolor='rgba(0,0,0,0)'),
        zaxis=dict(backgroundcolor='rgba(0,0,0,0)')
    )
)







