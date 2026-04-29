# -*- coding: utf-8 -*-
"""
Induction Motor Air-Gap Flux with Slip Effect
NEW:
✅ Rotor lag animation
✅ Slip control
✅ Stator vs rotor field separation
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Slip Effect Motor Animation", layout="wide")

st.title("⚡ Induction Motor Air-Gap Flux with Slip Effect")

# ============================================================
# SIDEBAR
# ============================================================
f = st.sidebar.slider("Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Bm (T)", 0.1, 3.0, 1.0)

slip = st.sidebar.slider("Slip (s)", 0.0, 0.3, 0.05, 0.01)
speed = st.sidebar.slider("Animation Speed", 1, 20, 5)

run = st.sidebar.checkbox("Run", True)

# ============================================================
# CONSTANTS
# ============================================================
p = pole // 2
Ns = 120 * f / pole

theta = np.linspace(0, 2*np.pi, 2000)

metric = st.empty()
plot = st.empty()

wt = 0

# ============================================================
# ANIMATION LOOP
# ============================================================
while run:

    wt_rad = np.radians(wt)

    # ========================================================
    # STATOR FIELD (SYNCHRONOUS SPEED)
    # ========================================================
    B_stator = 1.5 * Bm * np.cos(p * theta - wt_rad)

    # ========================================================
    # ROTOR FIELD (SLOWER DUE TO SLIP)
    # Rotor speed = (1 - slip)
    # ========================================================
    rotor_wt = wt_rad * (1 - slip)
    B_rotor = 1.2 * Bm * np.cos(p * theta - rotor_wt)

    # ========================================================
    # AIR-GAP SHAPE (STATOR BASED)
    # ========================================================
    r_mean = 0.86
    scale = 0.10 * Bm

    R = r_mean + scale * np.cos(p * theta - wt_rad)

    X = R * np.cos(theta)
    Y = R * np.sin(theta)

    # ========================================================
    # COLOR MAP FOR STATOR FIELD
    # ========================================================
    norm = plt.Normalize(-1.5*Bm, 1.5*Bm)
    cmap = plt.cm.coolwarm

    colors = cmap(norm(B_stator))

    # ========================================================
    # FIGURE
    # ========================================================
    fig, ax = plt.subplots(figsize=(9, 9))

    # Rotor / stator geometry
    ax.add_patch(Circle((0,0), 0.55, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), 1.18, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), r_mean, fill=False, linestyle='--', linewidth=2))

    # ========================================================
    # STATOR FLUX (RED-BLUE COLORED)
    # ========================================================
    for i in range(len(theta)-1):
        ax.plot(
            [X[i], X[i+1]],
            [Y[i], Y[i+1]],
            color=colors[i],
            linewidth=3
        )

    # ========================================================
    # ROTOR FLUX (GREEN LAGGING FIELD)
    # ========================================================
    Rr = (r_mean - 0.12) + 0.08 * np.cos(p * theta - rotor_wt)
    Xr = Rr * np.cos(theta)
    Yr = Rr * np.sin(theta)

    ax.plot(Xr, Yr, color="green", linewidth=2.5, alpha=0.9)

    # ========================================================
    # SLIP VISUAL LABEL
    # ========================================================
    ax.text(
        0,
        -1.35,
        f"Slip s = {slip:.2f} → Rotor lags stator field",
        ha='center',
        fontsize=12,
        fontweight='bold'
    )

    # ========================================================
    # ZERO REFERENCE
    # ========================================================
    ax.text(0, r_mean + 0.03, "Flux Zero Reference", ha='center', fontweight='bold')

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
    # LABELS
    # ========================================================
    ax.text(0, 0, "ROTOR CORE", ha='center', fontweight='bold')
    ax.text(0, 1.48, "STATOR", ha='center', fontweight='bold')

    ax.set_aspect('equal')
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
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

    # ========================================================
    # UPDATE TIME
    # ========================================================
    wt = (wt + speed) % 360
    time.sleep(0.05)
