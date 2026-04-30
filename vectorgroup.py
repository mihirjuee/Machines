# ============================================================
# STATIC THREE-PHASE TRANSFORMER VECTOR GROUP ANALYZER
# FULL VERSION WITH:
# ✅ Valid clock numbers only
# ✅ Vector group analyzer
# ✅ Static phasor diagram
# ✅ Clock phase displacement
# ✅ Detailed 6-coil terminal diagram
# ✅ Physical coil arrangement around transformer core
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
### Learn visually:
✅ Vector Group  
✅ Phase Shift  
✅ Clock Notation  
✅ Terminal Connections  
✅ Physical Coil Arrangement  
✅ Parallel Compatibility  
""")

# ============================================================
# VALID CLOCKS
# ============================================================
def get_valid_clocks(hv, lv):
    if (hv == "D" and lv == "d") or \
       (hv == "Y" and lv == "y") or \
       (hv == "Z" and lv == "z"):
        return [0, 6]
    return [1, 11]

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("Transformer Configuration")

hv_type = st.sidebar.selectbox("HV Winding Type", ["D", "Y", "Z"])
lv_type = st.sidebar.selectbox("LV Winding Type", ["d", "y", "z"])

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
# PHASOR DIAGRAM
# ============================================================
st.subheader("📈 Static Phasor Diagram")

fig1, ax1 = plt.subplots(figsize=(8,8), subplot_kw={'projection': 'polar'})

angles_primary = np.radians([90, -30, 210])  # RYB
labels_primary = ["R", "Y", "B"]

angles_secondary = angles_primary - np.radians(phase_shift)
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
st.subheader("🕒 Clock Representation with Phase Displacement")

fig2, ax2 = plt.subplots(figsize=(7,7))

circle = Circle((0, 0), 1, fill=False, linewidth=2)
ax2.add_patch(circle)

# Clock numbers
for i in range(12):
    angle = np.radians(90 - i*30)
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

# HV hand
ax2.arrow(
    0, 0,
    0, 0.72,
    head_width=0.05,
    linewidth=3,
    length_includes_head=True
)

# LV hand
lv_angle = np.radians(90 - clock*30)

ax2.arrow(
    0, 0,
    0.72*np.cos(lv_angle),
    0.72*np.sin(lv_angle),
    head_width=0.05,
    linewidth=3,
    length_includes_head=True
)

ax2.text(0, 0.82, "HV", fontsize=12, fontweight='bold')

ax2.text(
    0.82*np.cos(lv_angle),
    0.82*np.sin(lv_angle),
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
# DETAILED TERMINAL CONNECTION DIAGRAM
# ============================================================
st.subheader("🧲 Detailed HV/LV Coil Terminal Connection Diagram")

fig3, ax3 = plt.subplots(figsize=(18,8))

def draw_horizontal_coil(ax, x, y, label1, label2):
    xs = np.linspace(x, x+1.2, 200)
    ys = y + 0.15*np.sin(8*np.pi*(xs-x)/1.2)

    ax.plot(xs, ys, linewidth=2)

    ax.plot(x, y, 'o')
    ax.plot(x+1.2, y, 'o')

    ax.text(x-0.2, y+0.3, label1, fontsize=10, fontweight='bold')
    ax.text(x+1.1, y+0.3, label2, fontsize=10, fontweight='bold')

    return (x, y), (x+1.2, y)

# HV
ax3.text(3, 7.2, f"HV SIDE ({hv_type})", fontsize=16, fontweight='bold')

A1, A2 = draw_horizontal_coil(ax3, 1, 6, "A1", "A2")
B1, B2 = draw_horizontal_coil(ax3, 1, 4, "B1", "B2")
C1, C2 = draw_horizontal_coil(ax3, 1, 2, "C1", "C2")

if hv_type == "Y":
    star_x, star_y = 4, 4
    for pt in [A2, B2, C2]:
        ax3.plot([pt[0], star_x], [pt[1], star_y], linewidth=2)
    ax3.text(star_x+0.2, star_y, "N", fontsize=12, fontweight='bold')

elif hv_type == "D":
    ax3.plot([A2[0], B1[0]], [A2[1], B1[1]], linewidth=2)
    ax3.plot([B2[0], C1[0]], [B2[1], C1[1]], linewidth=2)
    ax3.plot([C2[0], A1[0]], [C2[1], A1[1]], linewidth=2)

# Core
for x in [8.2, 8.8]:
    ax3.plot([x, x], [1, 7], linewidth=5)

ax3.text(8.5, 7.2, "CORE", ha='center', fontsize=14, fontweight='bold')

# LV
ax3.text(13, 7.2, f"LV SIDE ({lv_type.upper()})", fontsize=16, fontweight='bold')

a1, a2 = draw_horizontal_coil(ax3, 11, 6, "a1", "a2")
b1, b2 = draw_horizontal_coil(ax3, 11, 4, "b1", "b2")
c1, c2 = draw_horizontal_coil(ax3, 11, 2, "c1", "c2")

if lv_type == "y":
    star_x, star_y = 14, 4
    for pt in [a2, b2, c2]:
        ax3.plot([pt[0], star_x], [pt[1], star_y], linewidth=2)

    if neutral:
        ax3.plot([star_x, star_x], [star_y, 1], linewidth=2, linestyle='dashed')
        ax3.text(star_x+0.2, 1, "n", fontsize=12, fontweight='bold')

elif lv_type == "d":
    ax3.plot([a2[0], b1[0]], [a2[1], b1[1]], linewidth=2)
    ax3.plot([b2[0], c1[0]], [b2[1], c1[1]], linewidth=2)
    ax3.plot([c2[0], a1[0]], [c2[1], a1[1]], linewidth=2)

ax3.set_xlim(0, 17)
ax3.set_ylim(0, 8)
ax3.axis('off')

st.pyplot(fig3)

# ============================================================
# PHYSICAL COIL ARRANGEMENT
# ============================================================
st.subheader("⚙️ Physical Coil Arrangement Around Transformer Core")

fig4, ax4 = plt.subplots(figsize=(16,8))

def draw_vertical_coil(ax, x, y_bottom, height, turns, label):
    y = np.linspace(y_bottom, y_bottom + height, 400)
    x_wave = x + 0.18 * np.sin(turns * 2 * np.pi * (y - y_bottom) / height)

    ax.plot(x_wave, y, linewidth=2)

    ax.plot(x, y_bottom, 'o')
    ax.plot(x, y_bottom + height, 'o')

    ax.text(x - 0.35, y_bottom - 0.3, f"{label}1", fontsize=10, fontweight='bold')
    ax.text(x - 0.35, y_bottom + height + 0.15, f"{label}2", fontsize=10, fontweight='bold')

    return (x, y_bottom), (x, y_bottom + height)

# Core
ax4.plot([7.5, 7.5], [1, 7], linewidth=8)
ax4.plot([8.5, 8.5], [1, 7], linewidth=8)
ax4.plot([7.5, 8.5], [7, 7], linewidth=8)
ax4.plot([7.5, 8.5], [1, 1], linewidth=8)

ax4.text(8, 7.4, "Transformer Core", ha='center', fontsize=14, fontweight='bold')

# HV windings
ax4.text(3.5, 7.4, "HV WINDINGS", fontsize=14, fontweight='bold')

A1p, A2p = draw_vertical_coil(ax4, 3, 5, 1.5, 5, "A")
B1p, B2p = draw_vertical_coil(ax4, 4, 3.2, 1.5, 5, "B")
C1p, C2p = draw_vertical_coil(ax4, 5, 1.4, 1.5, 5, "C")

# LV windings
ax4.text(11, 7.4, "LV WINDINGS", fontsize=14, fontweight='bold')

a1p, a2p = draw_vertical_coil(ax4, 11, 5, 1.5, 4, "a")
b1p, b2p = draw_vertical_coil(ax4, 12, 3.2, 1.5, 4, "b")
c1p, c2p = draw_vertical_coil(ax4, 13, 1.4, 1.5, 4, "c")

ax4.set_xlim(1, 15)
ax4.set_ylim(0.5, 8)
ax4.axis('off')

st.pyplot(fig4)

# ============================================================
# PARALLEL CHECKER
# ============================================================
st.subheader("🔗 Parallel Operation Checker")

vg2 = st.text_input("Enter another vector group (e.g. Dyn11)")

if vg2:
    if vg2.lower() == vector_group.lower():
        st.success("✅ Compatible for parallel operation")
    else:
        st.error("❌ Not compatible — phase mismatch risk")

# ============================================================
# NOTES
# ============================================================
st.subheader("📘 Engineering Notes")

st.markdown("""
### Standard Clock Numbers:
✅ 0, 6 → Same family  
✅ 1, 11 → Practical Delta-Star / Star-Delta  

### Important:
- Vector group decides phase shift
- Wrong matching causes circulating current
- Neutral impacts grounding
- Delta suppresses third harmonics
""")

st.warning("Incorrect transformer paralleling may damage equipment.")
