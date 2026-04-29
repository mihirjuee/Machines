# -*- coding: utf-8 -*-
"""
RMF Vector Field Animation (3-Phase Induction Motor)
NEW:
✅ Rotating magnetic field arrows (vector field)
✅ True RMF visualization
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import time

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="RMF Vector Field", layout="wide")

st.title("⚡ Rotating Magnetic Field (Vector Animation)")

# ============================================================
# SIDEBAR
# ============================================================
f = st.sidebar.slider("Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Bm (T)", 0.1, 3.0, 1.0)

slip = st.sidebar.slider("Slip (optional)", 0.0, 0.3, 0.05)
speed = st.sidebar.slider("Animation Speed", 1, 20, 5)

run = st.sidebar.checkbox("Run", True)

# ============================================================
# CONSTANTS
# ============================================================
p = pole // 2
Ns = 120 * f / pole

# Vector positions in air-gap
n_vectors = pole * 6
angles = np.linspace(0, 2*np.pi, n_vectors, endpoint=False)

metric = st.empty()
plot = st.empty()

wt = 0

# ============================================================
# ANIMATION LOOP
# ============================================================
while run:

    wt_rad = np.radians(wt)

    # ========================================================
    # FIGURE
    # ========================================================
    fig, ax = plt.subplots(figsize=(9, 9))

    # Machine geometry
    ax.add_patch(Circle((0,0), 0.55, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), 1.18, fill=False, linewidth=3))
    ax.add_patch(Circle((0,0), 0.86, fill=False, linestyle='--', linewidth=2))

    # ========================================================
    # ROTATING MAGNETIC FIELD (VECTOR FIELD)
    # ========================================================
    for th in angles:

        # spatial + time variation (RMF)
        B = Bm * np.cos(p * th - wt_rad)

        # vector direction (radial for visualization)
        x = np.cos(th)
        y = np.sin(th)

        # arrow length scaled by flux
        dx = 0.35 * B * x
        dy = 0.35 * B * y

        ax.arrow(
            x*0.8,
            y*0.8,
            dx,
            dy,
            head_width=0.05,
            head_length=0.07,
            color="purple" if B >= 0 else "orange",
            alpha=0.9
        )

    # ========================================================
    # LABELS
    # ========================================================
    ax.text(0, 0, "ROTOR", ha='center', fontweight='bold')
    ax.text(0, 1.48, "STATOR", ha='center', fontweight='bold')

    ax.text(
        0,
        -1.35,
        "Purple = Positive RMF | Orange = Negative RMF (instantaneous direction)",
        ha='center',
        fontsize=10,
        fontweight='bold'
    )

    ax.text(
        0,
        0.95,
        "Rotating Magnetic Field (RMF)",
        ha='center',
        fontsize=12,
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

    # ========================================================
    # FORMAT
    # ========================================================
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

    # ========================================================
    # UPDATE ANGLE
    # ========================================================
    wt = (wt + speed) % 360
    time.sleep(0.05)
