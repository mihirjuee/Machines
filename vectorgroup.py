# ============================================================
# ADVANCED THREE-PHASE TRANSFORMER VECTOR GROUP ANALYZER
# Streamlit App
# Features:
# ✅ Animated rotating phasors
# ✅ HV/LV vector group selector
# ✅ Clock notation visualizer
# ✅ Parallel compatibility checker
# ✅ Transformer application guide
# ✅ Dynamic phasor shift simulation
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Advanced Transformer Vector Group Analyzer", layout="wide")

st.title("⚡ Advanced 3-Phase Transformer Vector Group Analyzer")

st.markdown("""
### Visualize transformer vector groups dynamically:
- Animated phasor rotation
- Clock displacement
- Parallel compatibility
- Engineering applications
""")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Transformer Configuration")

hv_type = st.sidebar.selectbox("HV Winding", ["D", "Y", "Z"])
lv_type = st.sidebar.selectbox("LV Winding", ["d", "y", "z"])

neutral = st.sidebar.checkbox("LV Neutral (n)", value=True)

clock = st.sidebar.slider("Clock Number", 0, 11, 11)

speed = st.sidebar.slider("Animation Speed", 0.5, 5.0, 1.0)

# ---------------- VECTOR GROUP ----------------
vector_group = hv_type + lv_type
if neutral and lv_type in ["y", "z"]:
    vector_group += "n"

vector_group += str(clock)

phase_shift = clock * 30

# ---------------- HEADER DISPLAY ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vector Group", vector_group)

with col2:
    st.metric("Phase Shift", f"{phase_shift}°")

with col3:
    st.metric("Clock Position", f"{clock} o'clock")

# ---------------- ANIMATION ----------------
st.subheader("🎞️ Animated Phasor Rotation")

fig, ax = plt.subplots(figsize=(7,7), subplot_kw={'projection': 'polar'})

def update(frame):
    ax.clear()

    # Rotation angle
    base_angle = np.radians(frame * speed)

    # Primary phasors
    primary_angles = base_angle + np.radians([0, -120, 120])

    # Secondary phasors shifted
    secondary_angles = primary_angles - np.radians(phase_shift)

    # Plot HV phasors
    for angle, color, label in zip(primary_angles, ['r','g','b'], ['R','Y','B']):
        ax.arrow(angle, 0, 0, 1.0,
                 width=0.015, head_width=0.08, head_length=0.1,
                 length_includes_head=True)
        ax.text(angle, 1.15, label, fontsize=12)

    # Plot LV phasors
    for angle, color, label in zip(secondary_angles, ['r','g','b'], ['r','y','b']):
        ax.arrow(angle, 0, 0, 0.75,
                 width=0.01, head_width=0.06, head_length=0.08,
                 length_includes_head=True)
        ax.text(angle, 0.9, label, fontsize=11)

    ax.set_title(f"{vector_group} Dynamic Rotation")
    ax.set_rticks([])
    ax.grid(True)

# Create animation
ani = animation.FuncAnimation(fig, update, frames=360, interval=50)

# Save GIF to buffer
gif_path = "vector_group_animation.gif"
ani.save(gif_path, writer="pillow", fps=20)

# Display animation
st.image(gif_path)

# ---------------- CLOCK DIAL ----------------
st.subheader("🕒 Clock Representation")

fig2, ax2 = plt.subplots(figsize=(5,5))
clock_circle = Circle((0,0), 1, fill=False, linewidth=2)
ax2.add_patch(clock_circle)

# Draw clock positions
for i in range(12):
    angle = np.radians(90 - i*30)
    x = 0.85 * np.cos(angle)
    y = 0.85 * np.sin(angle)
    ax2.text(x, y, str(i if i != 0 else 12), ha='center', va='center')

# LV position
angle_lv = np.radians(90 - clock*30)
ax2.arrow(0, 0,
          0.7*np.cos(angle_lv),
          0.7*np.sin(angle_lv),
          head_width=0.08,
          length_includes_head=True)

# HV fixed at 12
ax2.arrow(0, 0, 0, 0.7,
          head_width=0.08,
          length_includes_head=True)

ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_aspect('equal')
ax2.axis('off')

st.pyplot(fig2)

# ---------------- PARALLEL CHECKER ----------------
st.subheader("🔗 Parallel Operation Checker")

vg2 = st.text_input("Enter second transformer vector group:")

if vg2:
    if vg2.lower() == vector_group.lower():
        st.success("✅ Compatible for parallel operation")
    else:
        st.error("❌ Not compatible due to vector group mismatch")

# ---------------- APPLICATION GUIDE ----------------
st.subheader("🏭 Practical Applications")

if "dyn11" in vector_group.lower():
    st.info("Dyn11: Widely used in distribution systems due to neutral and harmonic suppression.")
elif "dd0" in vector_group.lower():
    st.info("Dd0: Industrial heavy-load applications, no phase shift.")
elif "yd1" in vector_group.lower():
    st.info("Yd1: Motor and industrial systems.")
else:
    st.info("Specialized transformer application based on system requirements.")

# ---------------- HARMONIC NOTES ----------------
st.subheader("📚 Engineering Insights")

st.markdown("""
### Why vector groups matter:
✅ Synchronization  
✅ Parallel operation  
✅ Harmonic reduction  
✅ Grounding compatibility  
✅ Fault current behavior  

### Important:
**Clock notation determines LV phase displacement from HV reference.**
""")

st.warning("Incorrect vector group matching can cause severe circulating currents and equipment damage.")
