# ============================================================
# STATIC THREE-PHASE TRANSFORMER VECTOR GROUP ANALYZER
# UPDATED:
# ✅ Static phasor diagram (no animation)
# ✅ Only valid clock numbers shown based on winding combination
# ✅ Clean educational design
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Transformer Vector Group Analyzer", layout="wide")

st.title("⚡ Static 3-Phase Transformer Vector Group Analyzer")

# ---------------- VALID CLOCK LOGIC ----------------
def get_valid_clocks(hv, lv):
    # Same connection types → 0 or 6
    if (hv == "D" and lv == "d") or (hv == "Y" and lv == "y") or (hv == "Z" and lv == "z"):
        return [0, 6]

    # Delta-Star / Star-Delta / Zigzag combinations
    return [1, 5, 7, 11]

# ---------------- SIDEBAR ----------------
st.sidebar.header("Transformer Configuration")

hv_type = st.sidebar.selectbox("HV Winding", ["D", "Y", "Z"])
lv_type = st.sidebar.selectbox("LV Winding", ["d", "y", "z"])

neutral = st.sidebar.checkbox(
    "LV Neutral Available (n)",
    value=True,
    disabled=(lv_type == "d")
)

valid_clocks = get_valid_clocks(hv_type, lv_type)

clock = st.sidebar.selectbox(
    "Valid Clock Number",
    valid_clocks
)

# ---------------- VECTOR GROUP ----------------
vector_group = hv_type + lv_type

if neutral and lv_type in ["y", "z"]:
    vector_group += "n"

vector_group += str(clock)

phase_shift = clock * 30

# ---------------- DISPLAY ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vector Group", vector_group)

with col2:
    st.metric("Clock Number", clock)

with col3:
    st.metric("Phase Shift", f"{phase_shift}°")

# ---------------- STATIC PHASOR DIAGRAM ----------------
st.subheader("📈 Static Phasor Diagram")

fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection': 'polar'})

# HV Reference
angles_primary = np.radians([90, -30, 210])  # RYB
labels_primary = ['R', 'Y', 'B']

# LV Shift
angles_secondary = angles_primary - np.radians(phase_shift)
labels_secondary = ['r', 'y', 'b']

# Plot HV
for angle, label in zip(angles_primary, labels_primary):
    ax.annotate(
        '',
        xy=(angle, 1.0),
        xytext=(angle, 0),
        arrowprops=dict(width=2, headwidth=8)
    )
    ax.text(angle, 1.15, label, fontsize=12, fontweight='bold')

# Plot LV
for angle, label in zip(angles_secondary, labels_secondary):
    ax.annotate(
        '',
        xy=(angle, 0.75),
        xytext=(angle, 0),
        arrowprops=dict(width=1.5, headwidth=6)
    )
    ax.text(angle, 0.9, label, fontsize=11)

ax.set_title(f"{vector_group} Phasor Relationship", pad=20)
ax.set_rticks([])
ax.grid(True)

st.pyplot(fig)

# ---------------- CLOCK DIAL ----------------
st.subheader("🕒 Clock Representation")

fig2, ax2 = plt.subplots(figsize=(5,5))

# Clock circle
circle = Circle((0,0), 1, fill=False, linewidth=2)
ax2.add_patch(circle)

# Clock numbers
for i in range(12):
    angle = np.radians(90 - i*30)
    x = 0.88 * np.cos(angle)
    y = 0.88 * np.sin(angle)
    ax2.text(x, y, str(12 if i == 0 else i), ha='center', va='center')

# HV fixed at 12
ax2.arrow(0, 0, 0, 0.7,
          head_width=0.06,
          linewidth=2,
          length_includes_head=True)

# LV at selected clock
lv_angle = np.radians(90 - clock*30)

ax2.arrow(
    0, 0,
    0.7*np.cos(lv_angle),
    0.7*np.sin(lv_angle),
    head_width=0.06,
    linewidth=2,
    length_includes_head=True
)

ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_aspect('equal')
ax2.axis('off')

st.pyplot(fig2)

# ---------------- PARALLEL CHECKER ----------------
st.subheader("🔗 Parallel Operation Checker")

vg2 = st.text_input("Enter another vector group (e.g. Dyn11):")

if vg2:
    if vg2.lower() == vector_group.lower():
        st.success("✅ Compatible for parallel operation")
    else:
        st.error("❌ Not compatible — vector group mismatch")

# ---------------- APPLICATION GUIDE ----------------
st.subheader("🏭 Common Practical Uses")

if vector_group.lower() == "dyn11":
    st.info("Dyn11 → Most common for power distribution due to neutral + harmonic suppression.")
elif vector_group.lower() == "dd0":
    st.info("Dd0 → Industrial heavy-current applications.")
elif vector_group.lower() == "yd1":
    st.info("Yd1 → Industrial systems and motor loads.")
else:
    st.info("Application depends on grounding, harmonics, and system design.")

# ---------------- NOTES ----------------
st.subheader("📘 Engineering Notes")

st.markdown("""
### Valid clock numbers:
✅ **0, 6** → Same type displacement  
✅ **1, 5, 7, 11** → Delta-Star / Star-Delta displacement  

### Why vector groups matter:
- Parallel operation  
- Harmonic suppression  
- Neutral grounding  
- System compatibility  
""")

st.warning("Using invalid vector group combinations can cause phase mismatch and transformer damage.")
