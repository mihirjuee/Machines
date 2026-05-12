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
- Rotating magnetic field visualization
- N/S pole movement
- Time phase animation
- Flux wave distribution
- Stator magnetic field direction
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

    # Outer stator
    outer = patches.Circle(
        (0, 0),
        1.0,
        fill=False,
        linewidth=3
    )

    ax.add_patch(outer)

    # Inner stator
    inner = patches.Circle(
        (0, 0),
        0.25,
        fill=False,
        linewidth=2
    )

    ax.add_patch(inner)

    # Slots
    for ang in np.linspace(0, 2*np.pi, 12, endpoint=False):

        x1 = 0.75 * np.cos(ang)
        y1 = 0.75 * np.sin(ang)

        x2 = 1.0 * np.cos(ang)
        y2 = 1.0 * np.sin(ang)

        ax.plot([x1, x2], [y1, y2], color='black')

    # Rotating magnetic field arrow
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

    # N Pole
    ax.text(
        0.95*np.cos(theta),
        0.95*np.sin(theta),
        "N",
        fontsize=18,
        weight='bold',
        color='red',
        ha='center'
    )

    # S Pole
    ax.text(
        -0.95*np.cos(theta),
        -0.95*np.sin(theta),
        "S",
        fontsize=18,
        weight='bold',
        color='blue',
        ha='center'
    )

    ax.set_title(f"Field Angle = {angle_deg}°")

    ax.axis('off')

# =========================================================
# DRAW FLUX WAVE
# =========================================================

def draw_flux_wave(ax, phase_deg):

    x = np.linspace(0, 360, 1000)

    y = np.sin(np.radians(x - phase_deg))

    ax.plot(x, y, linewidth=3)

    ax.axhline(0, color='black')

    # Vertical phase lines
    for v in [0, 90, 180, 270, 360]:

        ax.axvline(v, color='gray')

    # Fill positive and negative
    ax.fill_between(
        x,
        y,
        where=(y >= 0),
        alpha=0.3
    )

    ax.fill_between(
        x,
        y,
        where=(y <= 0),
        alpha=0.3
    )

    # Add N/S labels
    for deg in [45, 225]:

        val = np.sin(np.radians(deg - phase_deg))

        if val > 0:
            label = "N"
        else:
            label = "S"

        ax.text(
            deg,
            val*0.7,
            label,
            fontsize=22,
            weight='bold',
            ha='center'
        )

    for deg in [135, 315]:

        val = np.sin(np.radians(deg - phase_deg))

        if val > 0:
            label = "N"
        else:
            label = "S"

        ax.text(
            deg,
            val*0.7,
            label,
            fontsize=22,
            weight='bold',
            ha='center'
        )

    ax.set_xlim(0, 360)
    ax.set_ylim(-1.2, 1.2)

    ax.set_xticks([0, 90, 180, 270, 360])

    ax.set_xticklabels(
        ["0°", "90°", "180°", "270°", "360°"]
    )

    ax.set_yticks([])

    ax.set_title("Flux Density Distribution")

# =========================================================
# DRAW COMPLETE FIGURE
# =========================================================

def draw_frame(angle):

    fig = plt.figure(figsize=(12, 8))

    # Left stator diagrams
    ax1 = fig.add_axes([0.05, 0.68, 0.25, 0.25])
    ax2 = fig.add_axes([0.05, 0.38, 0.25, 0.25])
    ax3 = fig.add_axes([0.05, 0.08, 0.25, 0.25])

    draw_stator(ax1, angle)
    draw_stator(ax2, angle + 90)
    draw_stator(ax3, angle + 180)

    # Right waveforms
    ax4 = fig.add_axes([0.35, 0.68, 0.6, 0.22])
    ax5 = fig.add_axes([0.35, 0.38, 0.6, 0.22])
    ax6 = fig.add_axes([0.35, 0.08, 0.6, 0.22])

    draw_flux_wave(ax4, angle)
    draw_flux_wave(ax5, angle + 90)
    draw_flux_wave(ax6, angle + 180)

    # Time labels
    fig.text(0.95, 0.79, "0", fontsize=16)
    fig.text(0.94, 0.49, "T/4", fontsize=16)
    fig.text(0.94, 0.19, "T/2", fontsize=16)

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
