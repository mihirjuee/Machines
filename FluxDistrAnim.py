# -*- coding: utf-8 -*-
"""
Lagging Field Coupling in Induction Motor RMF
NEW:
✅ Stator vs rotor rotating vectors
✅ Phase lag due to slip
✅ Coupling (torque-producing angle)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import time

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="Lagging Field Coupling", layout="wide")

st.title("⚡ Lagging Field Coupling in Induction Motor")

# ============================================================
# SIDEBAR
# ============================================================
f = st.sidebar.slider("Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Bm", 0.1, 3.0, 1.0)

slip = st.sidebar.slider("Slip", 0.0, 0.3, 0.05)
speed = st.sidebar.slider("Speed", 1, 20, 5)

run = st.sidebar.checkbox("Run", True)

# ============================================================
# CONSTANTS
# ============================================================
p = pole // 2
Ns = 120 * f / pole

angles = np.linspace(0, 2*np.pi, pole*6)

metric = st.empty()
plot = st.empty()

wt = 0

# ============================================================
# LOOP
# ============================================================
while run:

    wt_rad = np.radians(wt)

    fig, ax = plt.subplots(figsize=(9, 9))

    # machine geometry
    ax.add_patch(Circle((0,0), 0.55, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), 1.18, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), 0.86, fill=False, linestyle='--', linewidth=2))

    # ========================================================
    # STATOR FIELD (REFERENCE RMF)
    # ========================================================
    for th in angles:

        Bs = np.cos(p*th - wt_rad)

        x = np.cos(th)
        y = np.sin(th)

        ax.arrow(
            x*0.8,
            y*0.8,
            0.35*Bs*x,
            0.35*Bs*y,
            color="red",
            alpha=0.9,
            head_width=0.05
        )

    # ========================================================
    # ROTOR FIELD (LAGGING)
    # ========================================================
    rotor_wt = wt_rad * (1 - slip)

    for th in angles:

        Br = 0.9 * np.cos(p*th - rotor_wt)

        x = np.cos(th)
        y = np.sin(th)

        ax.arrow(
            x*0.6,
            y*0.6,
            0.30*Br*x,
            0.30*Br*y,
            color="blue",
            alpha=0.8,
            head_width=0.04
        )

    # ========================================================
    # COUPLING INDICATION (TORQUE ANGLE)
    # ========================================================
    delta = wt_rad - rotor_wt

    torque_indicator = np.sin(delta)

    ax.text(
        0,
        -1.35,
        f"Coupling Angle δ = {np.degrees(delta):.1f}° | Torque ∝ sin(δ) = {torque_indicator:.2f}",
        ha='center',
        fontsize=11,
        fontweight='bold'
    )

    # ========================================================
    # LABELS
    # ========================================================
    ax.text(0, 0, "ROTOR", ha='center', fontweight='bold')
    ax.text(0, 1.48, "STATOR", ha='center', fontweight='bold')

    ax.text(
        0,
        0.95,
        "Red = Stator RMF | Blue = Rotor Induced Field (Lagging)",
        ha='center',
        fontsize=10,
        fontweight='bold'
    )

    # ========================================================
    # POLES
    # ========================================================
    for k in range(pole):
        ang = (2*np.pi/pole)*k + wt_rad/p
        label = "N" if k % 2 == 0 else "S"

        ax.text(
            1.25*np.cos(ang),
            1.25*np.sin(ang),
            label,
            fontsize=14,
            fontweight='bold',
            ha='center'
        )

    # format
    ax.set_aspect('equal')
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis('off')

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

    # update time
    wt = (wt + speed) % 360
    time.sleep(0.05)
