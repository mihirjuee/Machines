# -*- coding: utf-8 -*-
"""
Animated 3-Phase Induction Motor Air-Gap Flux Waveform
UPGRADE:
✅ Positive flux = RED
✅ Negative flux = BLUE
✅ Zero flux = WHITE transition
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Flux Gradient Animation", layout="wide")

st.title("⚡ Colored Air-Gap Flux Density (Positive/Negative Gradient)")

# ============================================================
# SIDEBAR
# ============================================================
f = st.sidebar.slider("Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Bm (T)", 0.1, 3.0, 1.0)
speed = st.sidebar.slider("Speed", 1, 20, 5)
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
    # FLUX DISTRIBUTION (SIGNED FIELD)
    # ========================================================
    B = 1.5 * Bm * np.cos(p * theta - wt_rad)

    r_mean = 0.86
    scale = 0.10 * Bm

    R = r_mean + scale * np.cos(p * theta - wt_rad)

    X = R * np.cos(theta)
    Y = R * np.sin(theta)

    # ========================================================
    # COLOR MAPPING (KEY UPGRADE)
    # ========================================================
    norm = plt.Normalize(vmin=-1.5*Bm, vmax=1.5*Bm)
    cmap = plt.cm.coolwarm   # BLUE → WHITE → RED

    colors = cmap(norm(B))

    # ========================================================
    # FIGURE
    # ========================================================
    fig, ax = plt.subplots(figsize=(9, 9))

    # Rotor / stator
    ax.add_patch(Circle((0,0), 0.55, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), 1.18, fill=False, linewidth=3))

    # Zero reference circle
    ax.add_patch(Circle((0,0), r_mean, fill=False, linestyle='--', linewidth=2))

    # ========================================================
    # DRAW COLORED AIR-GAP WAVEFORM (SEGMENTED)
    # ========================================================
    for i in range(len(theta)-1):
        ax.plot(
            [X[i], X[i+1]],
            [Y[i], Y[i+1]],
            color=colors[i],
            linewidth=3
        )

    # ========================================================
    # FLUX ZERO LABEL
    # ========================================================
    ax.text(
        0,
        r_mean + 0.03,
        "Flux Zero Reference",
        ha='center',
        fontsize=11,
        fontweight='bold'
    )

    # Positive / Negative labels
    ax.text(0, r_mean + scale + 0.15, "🔴 Positive Flux", ha='center', fontweight='bold')
    ax.text(0, 0.55 + 0.1, "🔵 Negative Flux", ha='center', fontweight='bold')

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
            fontsize=16,
            fontweight='bold',
            ha='center'
        )

    # ========================================================
    # LABELS
    # ========================================================
    ax.text(0, 0, "ROTOR", ha='center', fontweight='bold')
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
        c3.metric("Peak Flux", f"{1.5*Bm:.2f}")
        c4.metric("Ns RPM", f"{Ns:.1f}")

    # ========================================================
    # UPDATE ANGLE
    # ========================================================
    wt = (wt + speed) % 360
    time.sleep(0.05)
