# ============================================================
# STATIC THREE-PHASE TRANSFORMER VECTOR GROUP ANALYZER
# FULL VERSION
# Features:
# ✅ Valid clock numbers only (0,6 / 1,11)
# ✅ Vector group generation
# ✅ Static phasor diagram
# ✅ Clock notation with phase displacement
# ✅ HV/LV coil connection diagram
# ✅ Parallel compatibility checker
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Transformer Vector Group Analyzer",
    layout="wide"
)

st.title("⚡ Three-Phase Transformer Vector Group Analyzer")
st.markdown("""
Understand transformer vector groups visually:
- Winding connections
- Clock notation
- Phase displacement
- Coil arrangement
- Parallel compatibility
""")

# ---------------- VALID CLOCK LOGIC ----------------
def get_valid_clocks(hv, lv):
    # Same family groups
    if (hv == "D" and lv == "d") or \
       (hv == "Y" and lv == "y") or \
       (hv == "Z" and lv == "z"):
        return [0, 6]

    # Practical transformer phase-shift groups
    return [1, 11]

# ---------------- SIDEBAR ----------------
st.sidebar.header("Transformer Configuration")

hv_type = st.sidebar.selectbox(
    "HV Winding Type",
    ["D", "Y", "Z"]
)

lv_type = st.sidebar.selectbox(
    "LV Winding Type",
    ["d", "y", "z"]
)

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

# ---------------- HEADER METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vector Group", vector_group)

with col2:
    st.metric("Clock Number", clock)

with col3:
    st.metric("Phase Shift", f"{phase_shift}°")

# ============================================================
# STATIC PHASOR DIAGRAM
# ============================================================
st.subheader("📈 Static Phasor Diagram")

fig1, ax1 = plt.subplots(
    figsize=(8,8),
    subplot_kw={'projection': 'polar'}
)

# HV reference phasors
angles_primary = np.radians([90, -30, 210])  # RYB
labels_primary = ["R", "Y", "B"]

# LV shifted phasors
angles_secondary = angles_primary - np.radians(phase_shift)
labels_secondary = ["r", "y", "b"]

# Plot HV
for angle, label in zip(angles_primary, labels_primary):
    ax1.annotate(
        '',
        xy=(angle, 1.0),
        xytext=(angle, 0),
        arrowprops=dict(
            width=2,
            headwidth=8
        )
    )
    ax1.text(
        angle,
        1.12,
        label,
        fontsize=12,
        fontweight='bold'
    )

# Plot LV
for angle, label in zip(angles_secondary, labels_secondary):
    ax1.annotate(
        '',
        xy=(angle, 0.75),
        xytext=(angle, 0),
        arrowprops=dict(
            width=1.5,
            headwidth=6
        )
    )
    ax1.text(
        angle,
        0.87,
        label,
        fontsize=11
    )

ax1.set_title(f"{vector_group} Phasor Relationship", pad=20)
ax1.set_rticks([])
ax1.grid(True)

st.pyplot(fig1)

# ============================================================
# CLOCK REPRESENTATION
# ============================================================
st.subheader("🕒 Clock Representation with Phase Displacement")

fig2, ax2 = plt.subplots(figsize=(7,7))

# Clock outer circle
circle = Circle((0, 0), 1, fill=False, linewidth=2)
ax2.add_patch(circle)

# Clock numbers
for i in range(12):
    angle = np.radians(90 - i * 30)
    x = 0.88 * np.cos(angle)
    y = 0.88 * np.sin(angle)

    ax2.text(
        x,
        y,
        str(12 if i == 0 else i),
        ha='center',
        va='center',
        fontsize=11,
        fontweight='bold'
    )

# HV hand
ax2.arrow(
    0, 0,
    0, 0.72,
    head_width=0.05,
    linewidth=3,
    length_includes_head=True
)

# LV hand
lv_angle = np.radians(90 - clock * 30)

ax2.arrow(
    0, 0,
    0.72 * np.cos(lv_angle),
    0.72 * np.sin(lv_angle),
    head_width=0.05,
    linewidth=3,
    length_includes_head=True
)

# Labels
ax2.text(0, 0.82, "HV", fontsize=12, fontweight='bold')

ax2.text(
    0.82 * np.cos(lv_angle),
    0.82 * np.sin(lv_angle),
    "LV",
    fontsize=12,
    fontweight='bold'
)

# Phase displacement explanation
if clock == 11:
    disp_text = f"{clock} × 30° = 330° (LV lags HV by 30°)"
elif clock == 1:
    disp_text = f"{clock} × 30° = 30° (LV leads HV by 30°)"
else:
    disp_text = f"{clock} × 30° = {phase_shift}°"

ax2.text(
    0,
    -1.25,
    f"Phase Displacement: {disp_text}",
    ha='center',
    fontsize=12,
    fontweight='bold'
)

ax2.set_xlim(-1.4, 1.4)
ax2.set_ylim(-1.4, 1.4)
ax2.set_aspect('equal')
ax2.axis('off')

st.pyplot(fig2)

# ============================================================
# COIL CONNECTION DIAGRAM
# ============================================================
st.subheader("🧲 Transformer Coil Connection Diagram")

fig3, ax3 = plt.subplots(figsize=(14,6))

# ---------------- HV SIDE ----------------
ax3.text(
    2,
    5,
    f"HV Side ({hv_type})",
    fontsize=14,
    fontweight='bold'
)

if hv_type == "D":
    pts = np.array([[1,3],[2,1],[3,3],[1,3]])
    ax3.plot(pts[:,0], pts[:,1], linewidth=3)

elif hv_type == "Y":
    center = (2,2)
    for pt in [(1,3),(3,3),(2,1)]:
        ax3.plot(
            [center[0], pt[0]],
            [center[1], pt[1]],
            linewidth=3
        )

elif hv_type == "Z":
    ax3.plot([1,2,1.5],[3,2,1], linewidth=3)
    ax3.plot([3,2,2.5],[3,2,1], linewidth=3)

# ---------------- CORE ----------------
for x in [6.3, 6.9]:
    ax3.plot([x, x], [0.5, 4.5], linewidth=4)

ax3.text(
    6.6,
    4.8,
    "Transformer Core",
    ha='center',
    fontsize=12,
    fontweight='bold'
)

# ---------------- LV SIDE ----------------
ax3.text(
    11,
    5,
    f"LV Side ({lv_type.upper()})",
    fontsize=14,
    fontweight='bold'
)

if lv_type == "d":
    pts = np.array([[10,3],[11,1],[12,3],[10,3]])
    ax3.plot(pts[:,0], pts[:,1], linewidth=3)

elif lv_type == "y":
    center = (11,2)
    for pt in [(10,3),(12,3),(11,1)]:
        ax3.plot(
            [center[0], pt[0]],
            [center[1], pt[1]],
            linewidth=3
        )

    if neutral:
        ax3.plot(
            [11,11],
            [2,0.3],
            linewidth=2,
            linestyle='dashed'
        )

        ax3.text(
            11.2,
            0.15,
            "N",
            fontsize=12,
            fontweight='bold'
        )

elif lv_type == "z":
    ax3.plot([10,11,10.5],[3,2,1], linewidth=3)
    ax3.plot([12,11,11.5],[3,2,1], linewidth=3)

ax3.set_xlim(0, 13)
ax3.set_ylim(0, 5.5)
ax3.axis('off')

st.pyplot(fig3)

# ============================================================
# PARALLEL CHECKER
# ============================================================
st.subheader("🔗 Parallel Operation Checker")

vg2 = st.text_input(
    "Enter another vector group (e.g. Dyn11)"
)

if vg2:
    if vg2.lower() == vector_group.lower():
        st.success(
            "✅ Compatible for parallel operation"
        )
    else:
        st.error(
            "❌ Not compatible — vector group mismatch may cause circulating current"
        )

# ============================================================
# APPLICATION GUIDE
# ============================================================
st.subheader("🏭 Common Applications")

if vector_group.lower() == "dyn11":
    st.info("Dyn11 → Most common distribution transformer.")
elif vector_group.lower() == "dd0":
    st.info("Dd0 → Industrial heavy-load systems.")
elif vector_group.lower() == "yd1":
    st.info("Yd1 → Industrial motor applications.")
else:
    st.info("Application depends on grounding, harmonics, and system needs.")

# ============================================================
# NOTES
# ============================================================
st.subheader("📘 Engineering Notes")

st.markdown("""
### Standard Valid Clock Numbers:
✅ **0, 6** → Same family (Dd, Yy, Zz)  
✅ **1, 11** → Delta-Star / Star-Delta practical groups  

### Why Vector Groups Matter:
- Parallel operation
- Harmonic suppression
- Grounding
- Neutral availability
- Phase compatibility
""")

st.warning(
    "Incorrect vector group matching can cause transformer damage due to phase mismatch."
)
