import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Circular Air-Gap Flux Distribution",
    layout="wide"
)

st.title("⚡ Rotating Magnetic Field - Circular Air Gap Flux Distribution")

st.markdown("""
### Features
- Circular air-gap flux density distribution
- Rotating magnetic field
- N-S pole rotation
- Flux arrow distribution
- Animated RMF
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
    # ROTATING FIELD VECTOR
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
    # N-S POLES
    # -----------------------------------------------------

    ax.text(
        1.1*np.cos(theta),
        1.1*np.sin(theta),
        "N",
        fontsize=18,
        weight='bold',
        color='red',
        ha='center'
    )

    ax.text(
        -1.1*np.cos(theta),
        -1.1*np.sin(theta),
        "S",
        fontsize=18,
        weight='bold',
        color='blue',
        ha='center'
    )

    ax.set_title(
        f"RMF Angle = {angle_deg}°",
        fontsize=12
    )

    ax.axis('off')

# =========================================================
# DRAW CIRCULAR AIR-GAP DISTRIBUTION
# =========================================================

def draw_circular_distribution(ax, phase_deg):

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # -----------------------------------------------------
    # OUTER AIR GAP
    # -----------------------------------------------------

    outer = patches.Circle(
        (0, 0),
        1.0,
        fill=False,
        linewidth=3
    )

    ax.add_patch(outer)

    # -----------------------------------------------------
    # INNER AIR GAP
    # -----------------------------------------------------

    inner = patches.Circle(
        (0, 0),
        0.55,
        fill=False,
        linewidth=2
    )

    ax.add_patch(inner)

    # -----------------------------------------------------
    # FLUX ARROWS DISTRIBUTION
    # -----------------------------------------------------

    angles = np.linspace(0, 360, 48)

    for ang in angles:

        theta = np.radians(ang)

        # Sinusoidal flux distribution
        B = np.sin(np.radians(ang - phase_deg))

        # Arrow start
        r1 = 0.6

        x1 = r1 * np.cos(theta)
        y1 = r1 * np.sin(theta)

        # Arrow direction
        dx = B * 0.35 * np.cos(theta)
        dy = B * 0.35 * np.sin(theta)

        ax.arrow(
            x1,
            y1,
            dx,
            dy,
            width=0.01,
            head_width=0.05,
            head_length=0.06,
            fc='black',
            ec='black',
            length_includes_head=True
        )

    # -----------------------------------------------------
    # N-S REGIONS
    # -----------------------------------------------------

    theta_n = np.radians(phase_deg)

    theta_s = np.radians(phase_deg + 180)

    ax.text(
        1.15*np.cos(theta_n),
        1.15*np.sin(theta_n),
        "N",
        fontsize=26,
        weight='bold',
        color='red',
        ha='center'
    )

    ax.text(
        1.15*np.cos(theta_s),
        1.15*np.sin(theta_s),
        "S",
        fontsize=26,
        weight='bold',
        color='blue',
        ha='center'
    )

    # -----------------------------------------------------
    # DEGREE MARKS
    # -----------------------------------------------------

    for ang in [0, 90, 180, 270]:

        theta = np.radians(ang)

        ax.text(
            1.35*np.cos(theta),
            1.35*np.sin(theta),
            f"{ang}°",
            fontsize=10,
            ha='center'
        )

    ax.set_title(
        "Circular Air-Gap Flux Density Distribution",
        fontsize=12,
        weight='bold'
    )

    ax.axis('off')

# =========================================================
# DRAW COMPLETE FRAME
# =========================================================

def draw_frame(angle):

    fig = plt.figure(figsize=(14, 10))

    # -----------------------------------------------------
    # LEFT SIDE - RMF
    # -----------------------------------------------------

    ax1 = fig.add_axes([0.05, 0.68, 0.28, 0.25])
    ax2 = fig.add_axes([0.05, 0.38, 0.28, 0.25])
    ax3 = fig.add_axes([0.05, 0.08, 0.28, 0.25])

    draw_stator(ax1, angle)
    draw_stator(ax2, angle + 90)
    draw_stator(ax3, angle + 180)

    # -----------------------------------------------------
    # RIGHT SIDE - CIRCULAR DISTRIBUTION
    # -----------------------------------------------------

    ax4 = fig.add_axes([0.42, 0.68, 0.5, 0.25])
    ax5 = fig.add_axes([0.42, 0.38, 0.5, 0.25])
    ax6 = fig.add_axes([0.42, 0.08, 0.5, 0.25])

    draw_circular_distribution(ax4, angle)
    draw_circular_distribution(ax5, angle + 90)
    draw_circular_distribution(ax6, angle + 180)

    # -----------------------------------------------------
    # TIME LABELS
    # -----------------------------------------------------

    fig.text(0.93, 0.78, "0", fontsize=16)
    fig.text(0.92, 0.48, "T/4", fontsize=16)
    fig.text(0.92, 0.18, "T/2", fontsize=16)

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
