import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Rotating Magnetic Field Simulation",
    layout="wide"
)

st.title("⚡ Rotating Magnetic Field (RMF) Simulation")

st.markdown("""
### Features
- Rotating magnetic field
- Air-gap flux density distribution
- Rotating N-S poles
- Flux arrows
- 0, T/4, T/2 conditions
""")

# =========================================================
# SESSION STATE
# =========================================================

if "run_animation" not in st.session_state:
    st.session_state.run_animation = False

# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Play Animation"):
        st.session_state.run_animation = True

with col2:
    if st.button("⏹ Stop Animation"):
        st.session_state.run_animation = False

placeholder = st.empty()

# =========================================================
# DRAW STATOR
# =========================================================

def draw_stator(ax, angle_deg):

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # -----------------------------------------------------
    # OUTER STATOR
    # -----------------------------------------------------

    outer = patches.Circle(
        (0, 0),
        1.0,
        fill=False,
        linewidth=3
    )

    ax.add_patch(outer)

    # -----------------------------------------------------
    # INNER ROTOR
    # -----------------------------------------------------

    inner = patches.Circle(
        (0, 0),
        0.25,
        fill=False,
        linewidth=2
    )

    ax.add_patch(inner)

    # -----------------------------------------------------
    # STATOR SLOTS
    # -----------------------------------------------------

    for ang in np.linspace(0, 2*np.pi, 12, endpoint=False):

        x1 = 0.75 * np.cos(ang)
        y1 = 0.75 * np.sin(ang)

        x2 = 1.0 * np.cos(ang)
        y2 = 1.0 * np.sin(ang)

        ax.plot(
            [x1, x2],
            [y1, y2],
            color='black'
        )

    # -----------------------------------------------------
    # RMF ARROW
    # -----------------------------------------------------

    theta = np.radians(angle_deg)

    x = 0.8 * np.cos(theta)
    y = 0.8 * np.sin(theta)

    ax.arrow(
        0,
        0,
        x,
        y,
        width=0.03,
        head_width=0.12,
        head_length=0.12,
        color='red'
    )

    # -----------------------------------------------------
    # N POLE
    # -----------------------------------------------------

    ax.text(
        0.95*np.cos(theta),
        0.95*np.sin(theta),
        "N",
        fontsize=18,
        weight='bold',
        color='red',
        ha='center'
    )

    # -----------------------------------------------------
    # S POLE
    # -----------------------------------------------------

    ax.text(
        -0.95*np.cos(theta),
        -0.95*np.sin(theta),
        "S",
        fontsize=18,
        weight='bold',
        color='blue',
        ha='center'
    )

    ax.set_title(
        f"Field Angle = {angle_deg}°",
        fontsize=12
    )

    ax.axis('off')

# =========================================================
# DRAW AIR-GAP FLUX DENSITY DISTRIBUTION
# =========================================================

def draw_flux_wave(ax, phase_deg):

    x = np.linspace(0, 360, 1000)

    # Air-gap flux density wave
    y = np.sin(np.radians(x - phase_deg))

    # -----------------------------------------------------
    # MAIN CURVE
    # -----------------------------------------------------

    ax.plot(
        x,
        y,
        linewidth=3,
        color='black'
    )

    # -----------------------------------------------------
    # ZERO AXIS
    # -----------------------------------------------------

    ax.axhline(
        0,
        color='black',
        linewidth=1
    )

    # -----------------------------------------------------
    # ANGULAR DIVISIONS
    # -----------------------------------------------------

    for v in [0, 90, 180, 270, 360]:

        ax.axvline(
            v,
            color='gray',
            linewidth=0.8
        )

    # -----------------------------------------------------
    # FLUX ARROWS
    # -----------------------------------------------------

    arrow_positions = np.linspace(0, 360, 60)

    for pos in arrow_positions:

        val = np.sin(np.radians(pos - phase_deg))

        ax.arrow(
            pos,
            0,
            0,
            val * 0.9,
            width=0.4,
            head_width=3,
            head_length=0.08,
            fc='black',
            ec='black',
            length_includes_head=True
        )

    # -----------------------------------------------------
    # N AND S REGIONS
    # -----------------------------------------------------

    regions = [

        (45, "N"),
        (135, "S"),
        (225, "N"),
        (315, "S")

    ]

    for deg, label in regions:

        val = np.sin(np.radians(deg - phase_deg))

        ax.text(
            deg,
            val * 0.65,
            label,
            fontsize=28,
            weight='bold',
            ha='center',
            color='dimgray'
        )

    # -----------------------------------------------------
    # AXIS SETTINGS
    # -----------------------------------------------------

    ax.set_xlim(0, 360)
    ax.set_ylim(-1.2, 1.2)

    ax.set_xticks([0, 90, 180, 270, 360])

    ax.set_xticklabels(
        ["0°", "90°", "180°", "270°", "360°"]
    )

    ax.set_yticks([])

    ax.set_title(
        "Air-Gap Flux Density Distribution",
        fontsize=12,
        weight='bold'
    )

# =========================================================
# DRAW COMPLETE FIGURE
# =========================================================

def draw_frame(angle):

    fig = plt.figure(figsize=(14, 9))

    # -----------------------------------------------------
    # LEFT STATOR FIGURES
    # -----------------------------------------------------

    ax1 = fig.add_axes([0.05, 0.68, 0.22, 0.22])
    ax2 = fig.add_axes([0.05, 0.38, 0.22, 0.22])
    ax3 = fig.add_axes([0.05, 0.08, 0.22, 0.22])

    draw_stator(ax1, angle)
    draw_stator(ax2, angle + 90)
    draw_stator(ax3, angle + 180)

    # -----------------------------------------------------
    # RIGHT AIR-GAP DISTRIBUTIONS
    # -----------------------------------------------------

    ax4 = fig.add_axes([0.32, 0.68, 0.63, 0.22])
    ax5 = fig.add_axes([0.32, 0.38, 0.63, 0.22])
    ax6 = fig.add_axes([0.32, 0.08, 0.63, 0.22])

    draw_flux_wave(ax4, angle)
    draw_flux_wave(ax5, angle + 90)
    draw_flux_wave(ax6, angle + 180)

    # -----------------------------------------------------
    # TIME LABELS
    # -----------------------------------------------------

    fig.text(0.96, 0.78, "0", fontsize=16)
    fig.text(0.95, 0.48, "T/4", fontsize=16)
    fig.text(0.95, 0.18, "T/2", fontsize=16)

    return fig

# =========================================================
# STATIC VIEW
# =========================================================

def draw_static():

    fig = draw_frame(0)

    placeholder.pyplot(fig)

    plt.close(fig)

# =========================================================
# ANIMATION
# =========================================================

if st.session_state.run_animation:

    for angle in range(0, 360, 10):

        if not st.session_state.run_animation:
            break

        fig = draw_frame(angle)

        placeholder.pyplot(fig)

        plt.close(fig)

        time.sleep(0.15)

else:

    draw_static()
