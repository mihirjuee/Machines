import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Multi-Pole RMF Visualization",
    layout="wide"
)

st.title("⚡ Multi-Pole Rotating Magnetic Field")
st.markdown("""
Adjust the number of poles to see how the magnetic sectors multiply and rotate. 
In a multi-pole machine, the magnetic field rotates **mechanically** slower for the same electrical frequency.
""")

# =========================================================
# SIDEBAR CONTROLS
# =========================================================
st.sidebar.header("Machine Parameters")
# Pole count must be even
poles = st.sidebar.select_slider("Number of Poles (P)", options=[2, 4, 6, 8], value=2)
speed = st.sidebar.slider("Animation Speed", 0.01, 0.5, 0.1)
arrow_density = st.sidebar.slider("Flux Arrow Density", 48, 120, 72)

if "run_animation" not in st.session_state:
    st.session_state.run_animation = False

# =========================================================
# DRAWING FUNCTION
# =========================================================

def draw_multipole_frame(electrical_angle_deg, P):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    
    # Constants
    elec_rad = np.radians(electrical_angle_deg)
    pole_pairs = P / 2
    
    # Draw Stator and Rotor Boundaries
    stator_outer = patches.Circle((0, 0), 1.1, fill=False, lw=4, color='#333333')
    stator_inner = patches.Circle((0, 0), 0.9, fill=False, lw=1, color='#666666')
    rotor_outer = patches.Circle((0, 0), 0.5, fill=True, color='#e0e0e0', zorder=0)
    ax.add_patch(stator_outer)
    ax.add_patch(stator_inner)
    ax.add_patch(rotor_outer)

    # Generate Flux Arrows
    angles = np.linspace(0, 360, arrow_density, endpoint=False)
    
    for ang in angles:
        mech_rad = np.radians(ang)
        
        # B = cos( P/2 * theta_mech - theta_electrical )
        B = np.cos(pole_pairs * mech_rad - elec_rad)
        
        color = 'red' if B > 0 else 'blue'
        
        # Arrow placement (in the air gap)
        r_mid = 0.7
        # Scale arrow length by flux density
        length = B * 0.25
        
        dx = length * np.cos(mech_rad)
        dy = length * np.sin(mech_rad)
        
        ax.arrow(
            r_mid * np.cos(mech_rad), r_mid * np.sin(mech_rad),
            dx, dy,
            width=0.01, head_width=0.04, head_length=0.05,
            fc=color, ec=color, alpha=max(0.2, abs(B))
        )

    # Label Poles (N and S)
    # Find peaks of the cosine wave
    for i in range(int(P)):
        # Peaks occur where (P/2 * mech - elec) = n * PI
        peak_mech_rad = (elec_rad + i * np.pi) / pole_pairs
        label = "N" if i % 2 == 0 else "S"
        l_color = "red" if label == "N" else "blue"
        
        ax.text(
            1.25 * np.cos(peak_mech_rad), 1.25 * np.sin(peak_mech_rad),
            label, fontsize=16, weight='bold', color=l_color,
            ha='center', va='center'
        )

    ax.set_title(f"{P}-Pole System | Electrical Angle: {electrical_angle_deg % 360}°", fontsize=14)
    ax.axis('off')
    return fig

# =========================================================
# MAIN INTERFACE
# =========================================================

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Animation"):
        st.session_state.run_animation = True
with col2:
    if st.button("⏹ Stop Animation"):
        st.session_state.run_animation = False

placeholder = st.empty()

# Animation Logic
if st.session_state.run_animation:
    while st.session_state.run_animation:
        for angle in range(0, 360, 5):
            if not st.session_state.run_animation:
                break
            fig = draw_multipole_frame(angle, poles)
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(speed)
else:
    fig = draw_multipole_frame(0, poles)
    placeholder.pyplot(fig)
    plt.close(fig)

# =========================================================
# INFO SECTION
# =========================================================
with st.expander("Understanding Multi-Pole Rotation"):
    st.markdown(f"""
    For a **{poles}-pole** machine:
    *   There are **{poles // 2}** pairs of North and South poles.
    *   One electrical cycle ($360^\circ$ electrical) results in only **{360 / (poles/2):.1f}^\circ$** of mechanical rotation.
    *   The mechanical speed $n_m$ is related to the electrical frequency $f$ by:
    """)
    st.latex(r"n_m = \frac{120 f}{P} \text{ RPM}")
    st.info("Notice how the red (N) and blue (S) zones stay closer together as you increase the number of poles!")
