# -*- coding: utf-8 -*-
"""
Induction Motor Air-Gap Flux Visualization
FINAL UPGRADE:
✅ Stator flux (red)
✅ Rotor flux (green)
✅ Resultant flux (blue)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="3-Flux Motor Model", layout="wide")

st.title("⚡ Stator, Rotor & Resultant Flux Distribution")

# ============================================================
# SIDEBAR
# ============================================================
f = st.sidebar.slider("Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Bm (T)", 0.1, 3.0, 1.0)

slip = st.sidebar.slider("Slip (s)", 0.0, 0.3, 0.05)
speed = st.sidebar.slider("Animation Speed", 1, 20, 5)

run = st.sidebar.checkbox("Run", True)

# ============================================================
# CONSTANTS
# ============================================================
p = pole // 2
Ns = 120 * f / pole

theta = np.linspace(0, 2*np.pi, 2500)

metric = st.empty()
plot = st.empty()

wt = 0

# ============================================================
# ANIMATION LOOP
# ============================================================
while run:

    wt_rad = np.radians(wt)

    # ========================================================
    # STATOR FLUX (RMF)
    # ========================================================
    B_stator = 1.5 * Bm * np.cos(p * theta - wt_rad)

    # ========================================================
    # ROTOR FLUX (LAGGING DUE TO SLIP)
    # ========================================================
    rotor_wt = wt_rad * (1 - slip)
    B_rotor = 1.2 * Bm * np.cos(p * theta - rotor_wt)

    # ========================================================
    # RESULTANT FLUX
    # ========================================================
    B_res = B_stator + B_rotor

    # ========================================================
    # AIR-GAP GEOMETRY (for visualization)
    # ========================================================
    r_mean = 0.86
    scale = 0.10 * Bm

    R = r_mean + scale * np.cos(p * theta - wt_rad)

    X = R * np.cos(theta)
    Y = R * np.sin(theta)

    # ========================================================
    # FIGURE
    # ========================================================
    fig, ax = plt.subplots(figsize=(9, 9))

    # Machine geometry
    ax.add_patch(Circle((0,0), 0.55, fill=False, linewidth=3))   # rotor
    ax.add_patch(Circle((0,0), 1.18, fill=False, linewidth=3))   # stator
    ax.add_patch(Circle((0,0), r_mean, fill=False, linestyle='--', linewidth=2))  # flux zero

    # ========================================================
    # STATOR FLUX (RED)
    # ========================================================
    R_s = r_mean + 0.10 * np.cos(p * theta - wt_rad)
    Xs = R_s * np.cos(theta)
    Ys = R_s * np.sin(theta)
    ax.plot(Xs, Ys, color="red", linewidth=2.5, label="Stator Flux")

    # ========================================================
    # ROTOR FLUX (GREEN - LAGGING)
    # ========================================================
    R_r = (r_mean - 0.12) + 0.08 * np.cos(p * theta - rotor_wt)
    Xr = R_r * np.cos(theta)
    Yr = R_r * np.sin(theta)
    ax.plot(Xr, Yr, color="green", linewidth=2.5, label="Rotor Flux")

    # ========================================================
    # RESULTANT FLUX (BLUE - SUPERPOSITION)
    # ========================================================
    R_res = r_mean + 0.10 * np.cos(p * theta - wt_rad) + 0.08 * np.cos(p * theta - rotor_wt)
    Xres = R_res * np.cos(theta)
    Yres = R_res * np.sin(theta)
    ax.plot(Xres, Yres, color="blue", linewidth=3.5, label="Resultant Flux")

    # ========================================================
    # LABELS
    # ========================================================
    ax.text(0, 0, "ROTOR CORE", ha='center', fontweight='bold')
    ax.text(0, 1.48, "STATOR", ha='center', fontweight='bold')

    ax.text(
        0,
        -1.35,
        "Red = Stator | Green = Rotor (Lag) | Blue = Resultant Field",
        ha='center',
        fontsize=11,
        fontweight='bold'
    )

    ax.text(0, r_mean + 0.03, "Flux Zero Reference (Mean Air-Gap)", ha='center')

    # ========================================================
    # POLES
    # ========================================================
    for k in range(pole):
        ang = (2*np.pi/pole)*k + wt_rad/p
        label = "N" if k % 2 == 0 else "S"

        ax.text(
            1.28*np.cos(ang),
            1.28*np.sin(ang),
            label,
            fontsize=14,
            fontweight='bold',
            ha='center'
        )

    # ========================================================
    # FINAL FORMAT
    # ========================================================
    ax.set_aspect('equal')
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
    ax.axis('off')
    ax.legend(loc="upper right")

    plot.pyplot(fig)
    plt.close(fig)

    # ========================================================
    # METRICS
    # ========================================================
    with metric.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Bm", f"{Bm:.2f}")
        c2.metric("Poles", pole)
        c3.metric("Slip", f"{slip:.2f}")
        c4.metric("Ns RPM", f"{Ns:.1f}")

    # ========================================================
    # UPDATE ANGLE
    # ========================================================
    wt = (wt + speed) % 360
    time.sleep(0.05)
