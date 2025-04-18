
import os
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

# Ensure the 'assets' folder exists and load the logo
logo_path = os.path.join(os.path.dirname(__file__), "assets", "mrslab.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    logo = None  # Prevents app crash if file is missing

# Streamlit Page Config
st.set_page_config(page_title="Polarization Visualizer", layout="wide")

# Sidebar Layout
st.sidebar.header(" ")
if logo:
    st.sidebar.image(logo)
st.sidebar.markdown("---")

# User Inputs
amplitude_h = st.sidebar.slider("Amplitude (H)", 0.0, 2.0, 1.0)
amplitude_v = st.sidebar.slider("Amplitude (V)", 0.0, 2.0, 1.0)
phase_diff = st.sidebar.slider("Phase Difference (δ in degrees)", -180, 180, 0)

# Compute wave properties
t = np.linspace(0, 2 * np.pi, 300)
Ex = amplitude_h * np.cos(t)
Ey = amplitude_v * np.cos(t + np.radians(phase_diff))

# Compute polarization parameters
alpha = np.arctan2(amplitude_v, amplitude_h)
ellipticity = 0.5 * np.arcsin((2 * amplitude_h * amplitude_v * np.sin(np.radians(phase_diff))) /
                              (amplitude_h ** 2 + amplitude_v ** 2))
orientation = 0.5 * np.arctan2(2 * amplitude_h * amplitude_v * np.cos(np.radians(phase_diff)),
                               (amplitude_h ** 2 - amplitude_v ** 2))

# Create a styled plot with fixed axes
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(Ex, Ey, color="#0072B2", linewidth=2)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.axvline(0, color='gray', linestyle='--', linewidth=1)

# Fixed Axis Labels for Static Reference
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_yticks([-2, -1, 0, 1, 2])

ax.set_xlabel("Horizontal Component (H)", fontsize=12)
ax.set_ylabel("Vertical Component (V)", fontsize=12)
ax.set_title("Polarization Visualization", fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)

# Layout for better readability
col1, col2 = st.columns([4, 3])

with col1:
    st.pyplot(fig)

with col2:
    st.markdown("### Wave Parameters")
    st.metric(label="Absolute Phase (α)", value=f"{np.degrees(alpha):.2f}°")
    st.metric(label="Ellipticity Angle", value=f"{np.degrees(ellipticity):.2f}°")
    st.metric(label="Orientation Angle", value=f"{np.degrees(orientation):.2f}°")

# Sidebar Footer
st.sidebar.markdown("---")
