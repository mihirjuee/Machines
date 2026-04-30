import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Transformer & Electromagnetism Lab", layout="wide")

st.title("⚡ Transformer Vector Groups & Electromagnetism")
st.markdown("""
This tool visualizes the magnetic interaction between conductors and the vector group configurations 
of polyphase transformers as discussed in **[source: 1]**.
""")

# ---------------- SIDEBAR: NAVIGATION ----------------
mode = st.sidebar.radio("Select Module", ["3D Parallel Conductors", "Transformer Vector Groups"])

# ==========================================================
# MODULE 1: 3D PARALLEL CONDUCTORS
# ==========================================================
if mode == "3D Parallel Conductors":
    st.header("🔗 3D Diagram: Two Parallel Current-Carrying Conductors")
    
    # Inputs
    I1 = st.sidebar.slider("Current I₁ (A)", 1.0, 100.0, 20.0)
    I2 = st.sidebar.slider("Current I₂ (A)", 1.0, 100.0, 20.0)
    d = st.sidebar.slider("Distance (m)", 0.5, 5.0, 2.0)
    direction = st.sidebar.radio("Direction", ["Same Direction", "Opposite Direction"])
    
    interaction = "Attraction" if direction == "Same Direction" else "Repulsion"

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    x1, y1, x2, y2 = -d/2, 0, d/2, 0
    z_range = np.linspace(-5, 5, 100)
    dir1, dir2 = 1, (1 if interaction == "Attraction" else -1)

    # Draw Conductors
    ax.plot([x1]*100, [y1]*100, z_range, color='gray', linewidth=5)
    ax.plot([x2]*100, [y2]*100, z_range, color='gray', linewidth=5)

    def draw_flux(xc, yc, curr_dir, color):
        theta = np.linspace(0, 2*np.pi, 200)
        if curr_dir == -1: theta = np.flip(theta)
        for zpos in [-3, 0, 3]:
            r = 0.7
            ax.plot(xc + r*np.cos(theta), yc + r*np.sin(theta), [zpos]*200, '--', color=color, alpha=0.6)
            # Embedded Arrow
            idx = 50
            px, py = xc + r*np.cos(theta[idx]), yc + r*np.sin(theta[idx])
            dx, dy = (xc + r*np.cos(theta[idx+1])) - px, (yc + r*np.sin(theta[idx+1])) - py
            ax.quiver(px, py, zpos, dx, dy, 0, color=color, pivot='tip', arrow_length_ratio=0.5)

    draw_flux(x1, y1, dir1, "royalblue")
    draw_flux(x2, y2, dir2, "crimson")

    # Force Arrows
    f_vec = 1.2 if interaction == "Attraction" else -1.2
    ax.quiver(x1, 0, 0, f_vec, 0, 0, color='green', linewidth=3)
    ax.quiver(x2, 0, 0, -f_vec, 0, 0, color='green', linewidth=3)

    ax.set_zlabel("Wire Length", labelpad=10)
    ax.view_init(elev=20, azim=45)
    st.pyplot(fig)
    
    st.latex(r"\frac{F}{L}=\frac{\mu_0 I_1 I_2}{2\pi d}")

# ==========================================================
# MODULE 2: TRANSFORMER VECTOR GROUPS
# ==========================================================
else:
    st.header("🕒 Transformer Vector Group Visualizer")
    
    group_opt = st.selectbox(
        "Select Vector Group [source: 1]",
        ["Group I: 0° (Yy0, Dd0)", "Group II: 180° (Yy6, Dd6)", 
         "Group III: -30° Lag (Dy1, Yd1)", "Group IV: +30° Lead (Dy11, Yd11)"]
    )
    
    shifts = {"Group I: 0° (Yy0, Dd0)": 0, "Group II: 180° (Yy6, Dd6)": 180, 
              "Group III: -30° Lag (Dy1, Yd1)": -30, "Group IV: +30° Lead (Dy11, Yd11)": 30}
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Phasor Diagram
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        off = np.radians(shifts[group_opt])
        p_angs = np.radians([90, 210, 330]) # A, B, C at 12, 4, 8 o'clock
        s_angs = p_angs - off
        
        for i, ang in enumerate(p_angs):
            ax.annotate('', xy=(ang, 1), xytext=(0,0), arrowprops=dict(color='blue', lw=2))
            ax.text(ang, 1.2, ['A','B','C'][i], color='blue', fontweight='bold')
        for i, ang in enumerate(s_angs):
            ax.annotate('', xy=(ang, 0.7), xytext=(0,0), arrowprops=dict(color='red', lw=2, ls='--'))
            ax.text(ang, 0.85, ['a','b','c'][i], color='red')
            
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.arange(0, 360, 30), labels=[12,1,2,3,4,5,6,7,8,9,10,11])
        st.pyplot(fig)

    with col2:
        # Winding Connection Logic [source: 1]
        st.subheader("Physical Coil Connection")
        if "Y" in group_opt:
            st.info("Star (Y): 1-terminals joined to form Neutral")
            st.code("Line A -> A2 | Line B -> B2 | Line C -> C2\nNeutral <- (A1 + B1 + C1)")
        else:
            st.info("Delta (D): Mesh connection to attenuate harmonics")
            st.code("A2-B1 | B2-C1 | C2-A1")
            
        st.write("**Key Principles from [source: 1]:**")
        st.markdown(f"""
        * HV terminals: Capital letters **A, B, C**.
        * LV terminals: Small letters **a, b, c**.
        * End designation: Terminals 1 and 2 define EMF polarity.
        """)

st.sidebar.markdown("---")
st.sidebar.caption("Based on technical documentation: Electrical Machines I [source: 1]")
