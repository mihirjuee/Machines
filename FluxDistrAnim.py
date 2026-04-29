# -*- coding: utf-8 -*-
"""
Animated 3-Phase Induction Motor Air-Gap Flux Waveform
FIXED:
✅ Flux Zero Reference = dotted mean air-gap circle
✅ Positive Flux = outside dotted circle
✅ Negative Flux = inside dotted circle
✅ True rotating sinusoidal waveform
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Animated Air-Gap Flux Waveform",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Animated 3-Phase Induction Motor Air-Gap Flux")
st.markdown("### Rotating sinusoidal magnetic field with correct flux zero reference")

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density Bm", 0.1, 3.0, 1.0, 0.1)

speed = st.sidebar.slider("Animation Speed", 1, 20, 5)

run = st.sidebar.checkbox("▶️ Run Animation", True)

# ============================================================
# CONSTANTS
# ============================================================
p = pole // 2                      # Pole pairs
Ns = 120 * f / pole               # Synchronous speed

theta_mech_deg = np.linspace(0, 360, 4000)
theta_mech = np.radians(theta_mech_deg)

# ============================================================
# STREAMLIT PLACEHOLDERS
# ============================================================
metric_placeholder = st.empty()
plot_placeholder = st.empty()
graph_placeholder = st.empty()

# ============================================================
# ANIMATION LOOP
# ============================================================
wt_deg = 0

while run:

    wt = np.radians(wt_deg)

    # ========================================================
    # RESULTANT FLUX DENSITY
    # ========================================================
    B = 1.5 * Bm * np.cos(p * theta_mech - wt)

    # ========================================================
    # AIR-GAP WAVEFORM
    # ========================================================
    r_mean = 0.86              # Zero reference circle
    scale = 0.10 * Bm          # Flux amplitude scaling

    R_wave = r_mean + scale * np.cos(p * theta_mech - wt)

    X_wave = R_wave * np.cos(theta_mech)
    Y_wave = R_wave * np.sin(theta_mech)

    # ========================================================
    # METRICS
    # ========================================================
    with metric_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Bm", f"{Bm:.2f} T")
        col2.metric("Poles", f"{pole}")
        col3.metric("Peak Flux", f"{1.5 * Bm:.2f}")
        col4.metric("Synchronous Speed", f"{Ns:.1f} RPM")

    # ========================================================
    # AIR-GAP ANIMATION FIGURE
    # ========================================================
    fig, ax = plt.subplots(figsize=(9, 9))

    # Geometry
    r_rotor = 0.55
    r_stator = 1.18
    r_axis = r_mean

    # Rotor / stator
    rotor = Circle((0, 0), r_rotor, fill=False, linewidth=3)
    stator = Circle((0, 0), r_stator, fill=False, linewidth=3)

    # Dotted zero-flux reference circle
    axis_circle = Circle(
        (0, 0),
        r_axis,
        fill=False,
        linestyle='--',
        linewidth=2
    )

    ax.add_patch(rotor)
    ax.add_patch(stator)
    ax.add_patch(axis_circle)

    # Main axes
    ax.plot([-r_stator, r_stator], [0, 0], linestyle='--', linewidth=1)
    ax.plot([0, 0], [-r_stator, r_stator], linestyle='--', linewidth=1)

    # ========================================================
    # ROTATING FLUX WAVEFORM
    # ========================================================
    ax.plot(X_wave, Y_wave, linewidth=4)

    # ========================================================
    # FLUX REFERENCE LABELS
    # ========================================================
    # Dotted circle = zero reference
    ax.text(
        0,
        r_axis + 0.03,
        "Flux Zero Reference",
        fontsize=11,
        fontweight='bold',
        ha='center',
        va='bottom'
    )

    # Positive flux = waveform expands outside zero circle
    ax.text(
        0,
        r_mean + scale + 0.18,
        "+ Positive Flux",
        fontsize=11,
        fontweight='bold',
        ha='center'
    )

    # Negative flux = waveform contracts inside zero circle
    ax.text(
        0,
        r_rotor + 0.12,
        "- Negative Flux",
        fontsize=11,
        fontweight='bold',
        ha='center'
    )

    # ========================================================
    # N / S POLE LABELS
    # ========================================================
    for k in range(pole):

        angle = (2 * np.pi / pole) * k + wt / p

        label = "N" if k % 2 == 0 else "S"

        ax.text(
            1.28 * np.cos(angle),
            1.28 * np.sin(angle),
            label,
            fontsize=16,
            fontweight='bold',
            ha='center',
            va='center'
        )

    # ========================================================
    # DEGREE MARKINGS
    # ========================================================
    for ang in np.arange(0, 360, 360 / pole):

        a = np.radians(ang)

        ax.text(
            1.38 * np.cos(a),
            1.38 * np.sin(a),
            f"{int(ang)}°",
            fontsize=10,
            ha='center'
        )

    # ========================================================
    # LABELS
    # ========================================================
    ax.text(
        0,
        0,
        "ROTOR",
        ha='center',
        va='center',
        fontsize=14,
        fontweight='bold'
    )

    ax.text(
        0,
        1.48,
        "STATOR",
        ha='center',
        fontsize=15,
        fontweight='bold'
    )

    ax.text(
        0,
        -1.48,
        f"{pole}-Pole Rotating Air-Gap Flux",
        ha='center',
        fontsize=12
    )

    # ========================================================
    # FORMATTING
    # ========================================================
    ax.set_aspect('equal')
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
    ax.axis('off')

    plot_placeholder.pyplot(fig)
    plt.close(fig)

    # ========================================================
    # LINEAR FLUX DISTRIBUTION
    # ========================================================
    fig2, ax2 = plt.subplots(figsize=(14, 5))

    ax2.plot(
        theta_mech_deg,
        B,
        linewidth=4,
        label="Resultant Flux Density"
    )

    # Zero reference line
    ax2.axhline(0, linestyle='--', linewidth=2)

    # Zero reference text
    ax2.text(
        355,
        0.02 * np.max(B),
        "Flux Zero Reference",
        fontsize=11,
        fontweight='bold',
        ha='right',
        va='bottom'
    )

    # Pole divisions
    for k in range(pole + 1):
        ax2.axvline(k * 360 / pole, linestyle=':', linewidth=1)

    # Peak labels
    ax2.text(
        15,
        np.max(B),
        "+Peak Flux",
        fontsize=10,
        fontweight='bold',
        va='bottom'
    )

    ax2.text(
        15,
        np.min(B),
        "-Peak Flux",
        fontsize=10,
        fontweight='bold',
        va='top'
    )

    ax2.set_title(f"{pole}-Pole Resultant Flux Density")
    ax2.set_xlabel("Mechanical Space Angle (degrees)")
    ax2.set_ylabel("Flux Density B(θ)")
    ax2.set_xticks(np.arange(0, 361, 360 / pole))
    ax2.grid(True)
    ax2.legend()

    graph_placeholder.pyplot(fig2)
    plt.close(fig2)

    # ========================================================
    # ANIMATION STEP
    # ========================================================
    wt_deg = (wt_deg + speed) % 360

    time.sleep(0.05)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success(
    "⚡ The dotted circle represents zero air-gap flux reference. "
    "Wave expansion outside it is positive flux, and contraction inside it is negative flux."
)
