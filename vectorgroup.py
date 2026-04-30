# ============================================================
# STATIC THREE-PHASE TRANSFORMER VECTOR GROUP ANALYZER
# FULL UPDATED VERSION
# Features:
# ✅ Valid clock numbers only
# ✅ Dynamic vector group generation
# ✅ Static phasor diagram
# ✅ Clock notation + phase displacement
# ✅ Fully updating HV/LV terminal connection diagram
# ✅ Physical transformer winding arrangement
# ✅ Parallel compatibility checker
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Transformer Vector Group Analyzer",
    layout="wide"
)

st.title("⚡ Three-Phase Transformer Vector Group Analyzer")

st.markdown("""
### Visual Learning Dashboard:
✅ Vector Group  
✅ Clock Notation  
✅ Phase Shift  
✅ Terminal Connection Logic  
✅ Physical Coil Arrangement  
✅ Parallel Compatibility  
""")

# ============================================================
# VALID CLOCK LOGIC
# ============================================================
def get_valid_clocks(hv, lv):
    # Same family practical groups
    if (hv == "D" and lv == "d") or \
       (hv == "Y" and lv == "y") or \
       (hv == "Z" and lv == "z"):
        return [0, 6]

    # Practical phase displacement groups
    return [1, 11]

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("⚙️ Transformer Configuration")

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

# ============================================================
# VECTOR GROUP
# ============================================================
vector_group = hv_type + lv_type

if neutral and lv_type in ["y", "z"]:
    vector_group += "n"

vector_group += str(clock)

phase_shift = clock * 30

# ============================================================
# METRICS
# ============================================================
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

angles_primary = np.radians([90, -30, 210])  # RYB
angles_secondary = angles_primary - np.radians(phase_shift)

labels_primary = ["R", "Y", "B"]
labels_secondary = ["r", "y", "b"]

# HV
for angle, label in zip(angles_primary, labels_primary):
    ax1.annotate(
        '',
        xy=(angle, 1.0),
        xytext=(angle, 0),
        arrowprops=dict(width=2, headwidth=8)
    )
    ax1.text(angle, 1.12, label, fontsize=12, fontweight='bold')

# LV
for angle, label in zip(angles_secondary, labels_secondary):
    ax1.annotate(
        '',
        xy=(angle, 0.75),
        xytext=(angle, 0),
        arrowprops=dict(width=1.5, headwidth=6)
    )
    ax1.text(angle, 0.87, label, fontsize=11)

ax1.set_title(f"{vector_group} Phasor Relationship", pad=20)
ax1.set_rticks([])
ax1.grid(True)

st.pyplot(fig1)

# ============================================================
# CLOCK REPRESENTATION
# ============================================================
st.subheader("🕒 Clock Representation")

fig2, ax2 = plt.subplots(figsize=(7,7))

circle = Circle((0, 0), 1, fill=False, linewidth=2)
ax2.add_patch(circle)

# Clock Numbers
for i in range(12):
    angle = np.radians(90 - i * 30)
    x = 0.88 * np.cos(angle)
    y = 0.88 * np.sin(angle)

    ax2.text(
        x, y,
        str(12 if i == 0 else i),
        ha='center',
        va='center',
        fontsize=11,
        fontweight='bold'
    )

# HV Hand
ax2.arrow(
    0, 0,
    0, 0.72,
    head_width=0.05,
    linewidth=3,
    length_includes_head=True
)

# LV Hand
lv_angle = np.radians(90 - clock * 30)

ax2.arrow(
    0, 0,
    0.72 * np.cos(lv_angle),
    0.72 * np.sin(lv_angle),
    head_width=0.05,
    linewidth=3,
    length_includes_head=True
)

ax2.text(0, 0.82, "HV", fontsize=12, fontweight='bold')

ax2.text(
    0.82 * np.cos(lv_angle),
    0.82 * np.sin(lv_angle),
    "LV",
    fontsize=12,
    fontweight='bold'
)

if clock == 11:
    disp_text = "LV lags HV by 30°"
elif clock == 1:
    disp_text = "LV leads HV by 30°"
elif clock == 6:
    disp_text = "180° displacement"
else:
    disp_text = "0° displacement"

ax2.text(
    0,
    -1.25,
    f"Phase Shift: {phase_shift}° ({disp_text})",
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
# DETAILED HV/LV TERMINAL CONNECTION DIAGRAM
# ============================================================
st.subheader("🧲 Detailed HV/LV Coil Terminal Connection Diagram")

fig3, ax3 = plt.subplots(figsize=(18,8))

def draw_horizontal_coil(ax, x, y, label1, label2):
    xs = np.linspace(x, x + 1.4, 300)
    ys = y + 0.18 * np.sin(8 * np.pi * (xs - x) / 1.4)

    ax.plot(xs, ys, linewidth=2)

    ax.plot(x, y, 'o')
    ax.plot(x + 1.4, y, 'o')

    ax.text(x - 0.25, y + 0.35, label1, fontsize=10, fontweight='bold')
    ax.text(x + 1.15, y + 0.35, label2, fontsize=10, fontweight='bold')

    return (x, y), (x + 1.4, y)

# ---------------- HV ----------------
ax3.text(3, 7.3, f"HV SIDE ({hv_type})", fontsize=16, fontweight='bold')

A1, A2 = draw_horizontal_coil(ax3, 1.0, 6.0, "A1", "A2")
B1, B2 = draw_horizontal_coil(ax3, 1.0, 4.0, "B1", "B2")
C1, C2 = draw_horizontal_coil(ax3, 1.0, 2.0, "C1", "C2")

ax3.text(0.3, 6.0, "R", fontsize=12, fontweight='bold')
ax3.text(0.3, 4.0, "Y", fontsize=12, fontweight='bold')
ax3.text(0.3, 2.0, "B", fontsize=12, fontweight='bold')

if hv_type == "Y":
    star_x, star_y = 4.8, 4.0
    for pt in [A2, B2, C2]:
        ax3.plot([pt[0], star_x], [pt[1], star_y], linewidth=2)
    ax3.text(star_x + 0.2, star_y, "N", fontsize=12, fontweight='bold')

elif hv_type == "D":
    ax3.plot([A2[0], B1[0]], [A2[1], B1[1]], linewidth=2)
    ax3.plot([B2[0], C1[0]], [B2[1], C1[1]], linewidth=2)
    ax3.plot([C2[0], A1[0]], [C2[1], A1[1]], linewidth=2)

elif hv_type == "Z":
    midx = 4.3
    ax3.plot([A2[0], midx], [A2[1], 5], linewidth=2)
    ax3.plot([B1[0], midx], [B1[1], 5], linewidth=2)
    ax3.plot([B2[0], midx], [B2[1], 3], linewidth=2)
    ax3.plot([C1[0], midx], [C1[1], 3], linewidth=2)

# ---------------- CORE ----------------
for x in [8.3, 8.9]:
    ax3.plot([x, x], [1, 7], linewidth=5)

ax3.text(8.6, 7.3, "TRANSFORMER CORE", ha='center', fontsize=14, fontweight='bold')

# ---------------- LV ----------------
ax3.text(13, 7.3, f"LV SIDE ({lv_type.upper()})", fontsize=16, fontweight='bold')

a1, a2 = draw_horizontal_coil(ax3, 11.0, 6.0, "a1", "a2")
b1, b2 = draw_horizontal_coil(ax3, 11.0, 4.0, "b1", "b2")
c1, c2 = draw_horizontal_coil(ax3, 11.0, 2.0, "c1", "c2")

ax3.text(15.2, 6.0, "r", fontsize=12, fontweight='bold')
ax3.text(15.2, 4.0, "y", fontsize=12, fontweight='bold')
ax3.text(15.2, 2.0, "b", fontsize=12, fontweight='bold')

if lv_type == "y":
    star_x, star_y = 14.8, 4.0
    for pt in [a2, b2, c2]:
        ax3.plot([pt[0], star_x], [pt[1], star_y], linewidth=2)

    if neutral:
        ax3.plot([star_x, star_x], [star_y, 1], linewidth=2, linestyle='dashed')
        ax3.text(star_x + 0.2, 1, "n", fontsize=12, fontweight='bold')

elif lv_type == "d":
    ax3.plot([a2[0], b1[0]], [a2[1], b1[1]], linewidth=2)
    ax3.plot([b2[0], c1[0]], [b2[1], c1[1]], linewidth=2)
    ax3.plot([c2[0], a1[0]], [c2[1], a1[1]], linewidth=2)

elif lv_type == "z":
    midx = 14.5
    ax3.plot([a2[0], midx], [a2[1], 5], linewidth=2)
    ax3.plot([b1[0], midx], [b1[1], 5], linewidth=2)
    ax3.plot([b2[0], midx], [b2[1], 3], linewidth=2)
    ax3.plot([c1[0], midx], [c1[1], 3], linewidth=2)

ax3.text(
    8.6,
    0.4,
    f"Vector Group: {vector_group} | Clock: {clock} | Phase Shift: {phase_shift}°",
    ha='center',
    fontsize=12,
    fontweight='bold'
)

ax3.set_xlim(0, 17)
ax3.set_ylim(0, 8)
ax3.axis('off')

st.pyplot(fig3)

# ============================================================
# PARALLEL CHECKER
# ============================================================
st.subheader("🔗 Parallel Operation Checker")

vg2 = st.text_input("Enter another vector group (Example: Dyn11)")

if vg2:
    if vg2.lower() == vector_group.lower():
        st.success("✅ Compatible for parallel operation")
    else:
        st.error("❌ Not compatible — vector mismatch may cause circulating current")

# ============================================================
# NOTES
# ============================================================
st.subheader("📘 Engineering Notes")

st.markdown("""
### Standard Practical Clock Numbers:
✅ 0, 6 → Same family  
✅ 1, 11 → Delta-Star / Star-Delta  

### Why It Matters:
- Determines phase displacement
- Essential for parallel operation
- Affects grounding
- Controls harmonics
- Prevents circulating current
""")

st.warning("Incorrect vector group matching can damage transformers.")
