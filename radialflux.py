import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="RMF Air-Gap Distribution",
    layout="wide"
)

st.title("⚡ Interactive Rotating Magnetic Field")
st.markdown("""
This tool visualizes how 3-phase currents create a constant-magnitude rotating magnetic field (RMF) 
and how that field is distributed across the air-gap.
""")

# =========================================================
# SIDEBAR CONTROLS
# =========================================================
st.sidebar.header("Simulation Settings")
speed = st.sidebar.slider("Animation Speed", 0.05, 0.5, 0.1)
resolution = st.sidebar.slider("Flux Arrow Density", 24, 72, 48)

if "run_animation" not in st.session_state:
    st.session_state.run_animation = False

# =========================================================
# CORE DRAWING FUNCTIONS
# =========================================================

def draw_rmf_frame(angle_deg, arrow_density=48):
    """
    Combines the physical stator view and the circular flux distribution.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    theta_rad = np.radians(angle_deg)

    # --- LEFT: Physical Stator & Resultant Vector ---
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    
    # Stator & Rotor Circles
    ax1.add_patch(patches.Circle((0, 0), 1.0, fill=False, lw=3, color='#333333'))
    ax1.add_patch(patches.Circle((0, 0), 0.4, fill=True, color='#f0f0f0'))
    
    # Resultant RMF Vector
    ax1.arrow(0, 0, 0.85 * np.cos(theta_rad), 0.85 * np.sin(theta_rad),
              width=0.04, head_width=0.15, head_length=0.15, color='red', label="Resultant B")
    
    # N-S Labels
    ax1.text(1.2 * np.cos(theta_rad), 1.2 * np.sin(theta_rad), "N", 
             fontsize=20, weight='bold', color='red', ha='center', va='center')
    ax1.text(1.2 * np.cos(theta_rad + np.pi), 1.2 * np.sin(theta_rad + np.pi), "S", 
             fontsize=20, weight='bold', color='blue', ha='center', va='center')
    
    ax1.set_title(f"Space Vector Position (θ = {angle_deg % 360}°)", fontsize=14)
    ax1.axis('off')

    # --- RIGHT: Air-Gap Flux Distribution ---
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    
    # Air Gap boundaries
    ax2.add_patch(patches.Circle((0, 0), 1.0, fill=False, lw=2))
    ax2.add_patch(patches.Circle((0, 0), 0.6, fill=False, lw=2))
    
    angles = np.linspace(0, 360, arrow_density)
    for ang in angles:
        a_rad = np.radians(ang)
        # B = Bmax * cos(theta - omega*t)
        B = np.cos(a_rad - theta_rad)
        
        # Color mapping: Red for Outward (N), Blue for Inward (S)
        color = 'red' if B > 0 else 'blue'
        
        # Scale arrows
        r_start = 0.8
        dx = B * 0.3 * np.cos(a_rad)
        dy = B * 0.3 * np.sin(a_rad)
        
        ax2.arrow(r_start * np.cos(a_rad), r_start * np.sin(a_rad), dx, dy,
                  width=0.005, head_width=0.04, head_length=0.05, 
                  fc=color, ec=color, alpha=abs(B))

    ax2.set_title("Air-Gap Flux Density Distribution", fontsize=14)
    ax2.axis('off')
    
    return fig

# =========================================================
# MAIN INTERFACE
# =========================================================

col_btn1, col_btn2, _ = st.columns([1, 1, 3])

with col_btn1:
    if st.button("▶ Start Animation"):
        st.session_state.run_animation = True
with col_btn2:
    if st.button("⏹ Stop Animation"):
        st.session_state.run_animation = False

plot_spot = st.empty()

# =========================================================
# EXECUTION LOGIC
# =========================================================

if st.session_state.run_animation:
    # Loop for animation
    while st.session_state.run_animation:
        for angle in range(0, 360, 10):
            if not st.session_state.run_animation:
                break
            
            fig = draw_rmf_frame(angle, resolution)
            plot_spot.pyplot(fig)
            plt.close(fig)
            time.sleep(speed)
else:
    # Static view (Snapshot)
    fig = draw_rmf_frame(0, resolution)
    plot_spot.pyplot(fig)
    plt.close(fig)

# =========================================================
# TECHNICAL EXPLANATION
# =========================================================
with st.expander("Show Mathematical Details"):
    st.latex(r"B(\theta, t) = B_{max} \cos(\theta - \omega t)")
    st.markdown("""
    - **Red Arrows:** Represent the North pole region where flux lines leave the stator.
    - **Blue Arrows:** Represent the South pole region where flux lines enter the stator.
    - As time ($t$) progresses, the peak of the sinusoidal distribution shifts around the periphery at **synchronous speed**.
    """)
