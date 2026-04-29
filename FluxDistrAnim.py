# -*- coding: utf-8 -*-
"""
Animated 3-Phase Induction Motor Air-Gap Flux Waveform
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Animated Air-Gap Flux Waveform", layout="wide")

st.title("⚡ Animated 3-Phase Induction Motor Air-Gap Flux")
st.markdown("### Real-time rotating sinusoidal magnetic field")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density Bm", 0.1, 3.0, 1.0, 0.1)

speed = st.sidebar.slider("Animation Speed", 1, 20, 5)

run = st.sidebar.checkbox("▶️ Run Animation", True)

# Pole pairs
p = pole // 2

# Mechanical angle
theta_mech_deg = np.linspace(0, 360, 4000)
theta_mech = np.radians(theta_mech_deg)

# Synchronous speed
Ns = 120 * f / pole

# ---------------- PLACEHOLDERS ----------------
plot_placeholder = st.empty()
graph_placeholder = st.empty()
metric_placeholder = st.empty()

# ---------------- ANIMATION LOOP ----------------
wt_deg = 0

while run:

    wt = np.radians(wt_deg)

    # Resultant flux
    B = 1.5 * Bm * np.cos(p * theta_mech - wt)

    # Air-gap waveform
    r_mean = 0.86
    scale = 0.10 * Bm

    R_wave = r_mean + scale * np.cos(p * theta_mech - wt)

    X_wave = R_wave * np.cos(theta_mech)
    Y_wave = R_wave * np.sin(theta_mech)

    # ============================================================
    # METRICS
    # ============================================================
    with metric_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Bm", f"{Bm:.2f} T")
        col2.metric("Poles", f"{pole}")
        col3.metric("Peak Flux", f"{1.5*Bm:.2f}")
        col4.metric("Synchronous Speed", f"{Ns:.1f} RPM")

    # ============================================================
    # POLAR AIR-GAP PLOT
    # ============================================================
    fig, ax = plt.subplots(figsize=(8,8))

    r_rotor = 0.55
    r_stator = 1.18
    r_axis = r_mean

    rotor = Circle((0,0), r_rotor, fill=False, linewidth=3)
    stator = Circle((0,0), r_stator, fill=False, linewidth=3)
    axis_circle = Circle((0,0), r_axis, fill=False, linestyle='--', linewidth=1)

    ax.add_patch(rotor)
    ax.add_patch(stator)
    ax.add_patch(axis_circle)

    # Axes
    ax.plot([-r_stator, r_stator], [0,0], linestyle='--', linewidth=1)
    ax.plot([0,0], [-r_stator, r_stator], linestyle='--', linewidth=1)

    # Flux waveform
    ax.plot(X_wave, Y_wave, linewidth=4)

    # Pole labels
    for k in range(pole):
        angle = (2*np.pi/pole) * k + wt/p
        label = "N" if k % 2 == 0 else "S"

        ax.text(
            1.28*np.cos(angle),
            1.28*np.sin(angle),
            label,
            fontsize=16,
            fontweight='bold',
            ha='center',
            va='center'
        )

    # Degree labels
    for ang in np.arange(0, 360, 360/pole):
        a = np.radians(ang)
        ax.text(
            1.38*np.cos(a),
            1.38*np.sin(a),
            f"{int(ang)}°",
            fontsize=10,
            ha='center'
        )

    ax.text(0, 0, "ROTOR", ha='center', va='center',
            fontsize=14, fontweight='bold')

    ax.text(0, -1.48,
            f"{pole}-Pole Rotating Flux",
            ha='center', fontsize=12)

    ax.set_aspect('equal')
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
    ax.axis('off')

    plot_placeholder.pyplot(fig)
    plt.close(fig)

    # ============================================================
    # LINEAR GRAPH
    # ============================================================
    fig2, ax2 = plt.subplots(figsize=(12,4))

    ax2.plot(theta_mech_deg, B, linewidth=3)

    ax2.axhline(0, linestyle='--', linewidth=1)

    for k in range(pole + 1):
        ax2.axvline(k * 360/pole, linestyle=':', linewidth=1)

    ax2.set_title(f"{pole}-Pole Resultant Flux Density")
    ax2.set_xlabel("Mechanical Space Angle (degrees)")
    ax2.set_ylabel("Flux Density B(θ)")
    ax2.set_xticks(np.arange(0, 361, 360/pole))
    ax2.grid(True)

    graph_placeholder.pyplot(fig2)
    plt.close(fig2)

    # Update animation angle
    wt_deg = (wt_deg + speed) % 360

    time.sleep(0.05)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ Distributed 3-phase currents create a continuously rotating sinusoidal magnetic field.")
