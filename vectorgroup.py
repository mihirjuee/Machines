import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Transformer Vector Group Pro",
    layout="wide"
)

st.title("⚡ Transformer Vector Group & Terminal Analyzer")

# ============================================================
# LOGIC ENGINE
# ============================================================
def get_valid_clocks(hv, lv):
    # Groups 0 & 6: Same connection types
    if (hv == lv.upper()):
        return [0, 6]
    # Groups 1 & 11: Mixed connection types
    return [1, 11]

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("🔧 Configuration")

hv_type = st.sidebar.selectbox("High Voltage (HV)", ["D", "Y"])
lv_type = st.sidebar.selectbox("Low Voltage (LV)", ["d", "y", "z"])

valid_clocks = get_valid_clocks(hv_type, lv_type)
clock = st.sidebar.selectbox("Clock Position", valid_clocks)

neutral = st.sidebar.checkbox("Show LV Neutral (n)", value=True if lv_type != 'd' else False, disabled=(lv_type == 'd'))

# Build Vector Group String
vector_group = f"{hv_type}{lv_type}{'n' if neutral else ''}{clock}"
phase_shift = clock * 30

# ============================================================
# UI LAYOUT: METRICS
# ============================================================
m1, m2, m3 = st.columns(3)
m1.metric("Vector Group", vector_group)
m2.metric("Clock Number", f"{clock} o'clock")
# Standard convention: 11 leads (+30), 1 lags (-30)
direction = "Leads" if clock > 6 else ("Lags" if 0 < clock < 6 else "In-Phase")
m3.metric("Phase Shift", f"{phase_shift}°", direction)

# ============================================================
# VISUALIZATION: PHASORS & CLOCK
# ============================================================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Phasor Diagram")
    fig_ph, ax_ph = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    
    # HV Reference (R-Y-B at 90, 330, 210)
    hv_angles = np.radians([90, 330, 210])
    labels_hv = ['A (R)', 'B (Y)', 'C (B)']
    for ang, lab in zip(hv_angles, labels_hv):
        ax_ph.annotate('', xy=(ang, 1.0), xytext=(0, 0), arrowprops=dict(edgecolor='red', lw=2))
        ax_ph.text(ang, 1.15, lab, fontweight='bold', color='red')

    # LV Adjusted by Clock
    lv_angles = hv_angles - np.radians(phase_shift)
    labels_lv = ['a (r)', 'b (y)', 'c (b)']
    for ang, lab in zip(lv_angles, labels_lv):
        ax_ph.annotate('', xy=(ang, 0.7), xytext=(0, 0), arrowprops=dict(edgecolor='blue', lw=2))
        ax_ph.text(ang, 0.85, lab, fontweight='bold', color='blue')
    
    ax_ph.set_yticklabels([])
    st.pyplot(fig_ph)

with col_b:
    st.subheader("🕒 Clock View")
    fig_cl, ax_cl = plt.subplots(figsize=(5, 5))
    circle = Circle((0, 0), 1, fill=False, lw=2, color='black')
    ax_cl.add_patch(circle)
    
    for i in range(12):
        angle = np.radians(90 - i*30)
        ax_cl.text(0.85*np.cos(angle), 0.85*np.sin(angle), str(12 if i==0 else i), ha='center', va='center')

    # HV Hand
    ax_cl.arrow(0, 0, 0, 0.7, head_width=0.05, color='red', label='HV')
    # LV Hand
    lv_a = np.radians(90 - clock*30)
    ax_cl.arrow(0, 0, 0.7*np.cos(lv_a), 0.7*np.sin(lv_a), head_width=0.05, color='blue', label='LV')
    
    ax_cl.set_xlim(-1.1, 1.1); ax_cl.set_ylim(-1.1, 1.1); ax_cl.axis('off')
    st.pyplot(fig_cl)

# ============================================================
# DYNAMIC COIL SCHEMATIC
# ============================================================
st.subheader("🧲 Physical Terminal Connections")

fig_sch, ax_sch = plt.subplots(figsize=(12, 6))

def draw_coil(x, y, name1, name2, color):
    # Sine wave for coil look
    xs = np.linspace(x, x+1.5, 100)
    ys = y + 0.2 * np.sin(2 * np.pi * 5 * (xs-x)/1.5)
    ax_sch.plot(xs, ys, color=color, lw=3)
    ax_sch.text(x-0.4, y, name1, fontsize=10, weight='bold')
    ax_sch.text(x+1.6, y, name2, fontsize=10, weight='bold')
    return (x, y), (x+1.5, y)

# HV Coils
H_A1, H_A2 = draw_coil(1, 5, "A1", "A2", "red")
H_B1, H_B2 = draw_coil(1, 3, "B1", "B2", "red")
H_C1, H_C2 = draw_coil(1, 1, "C1", "C2", "red")

# LV Coils
L_a1, L_a2 = draw_coil(8, 5, "a1", "a2", "blue")
L_b1, L_b2 = draw_coil(8, 3, "b1", "b2", "blue")
L_c1, L_c2 = draw_coil(8, 1, "c1", "c2", "blue")

# --- HV CONNECTION LOGIC ---
if hv_type == "Y":
    # Star point at A2, B2, C2
    ax_sch.plot([H_A2[0], H_A2[0]+0.5, H_A2[0]+0.5], [H_A2[1], H_A2[1], H_C2[1]], color='black')
    ax_sch.plot([H_B2[0], H_B2[0]+0.5], [H_B2[1], H_B2[1]], color='black')
    ax_sch.text(H_B2[0]+0.6, H_B2[1], "N", color='red')
else: # Delta
    # A2-B1, B2-C1, C2-A1
    ax_sch.plot([H_A2[0], H_B1[0]-0.5, H_B1[0]-0.5, H_B1[0]], [H_A2[1], H_A2[1], H_B1[1], H_B1[1]], color='black')
    ax_sch.plot([H_B2[0], H_C1[0]-0.5, H_C1[0]-0.5, H_C1[0]], [H_B2[1], H_B2[1], H_C1[1], H_C1[1]], color='black')
    ax_sch.plot([H_C2[0], H_C2[0]+0.3, H_C2[0]+0.3, H_A1[0]-0.7, H_A1[0]-0.7, H_A1[0]], 
                [H_C2[1], H_C2[1]-0.5, 6, 6, H_A1[1], H_A1[1]], color='black')

# --- LV CONNECTION LOGIC ---
if lv_type == "y":
    # Star point
    ax_sch.plot([L_a2[0], L_a2[0]+0.5, L_a2[0]+0.5], [L_a2[1], L_a2[1], L_c2[1]], color='black')
    ax_sch.plot([L_b2[0], L_b2[0]+0.5], [L_b2[1], L_b2[1]], color='black')
    if neutral: ax_sch.text(L_b2[0]+0.6, L_b2[1], "n", color='blue')
elif lv_type == "d":
    # d11 or d1 logic
    ax_sch.plot([L_a2[0], L_b1[0]-0.5, L_b1[0]-0.5, L_b1[0]], [L_a2[1], L_a2[1], L_b1[1], L_b1[1]], color='black')
    ax_sch.plot([L_b2[0], L_c1[0]-0.5, L_c1[0]-0.5, L_c1[0]], [L_b2[1], L_b2[1], L_c1[1], L_c1[1]], color='black')

ax_sch.set_xlim(0, 12); ax_sch.set_ylim(0, 7); ax_sch.axis('off')
st.pyplot(fig_sch)

# ============================================================
# COMPATIBILITY CHECKER
# ============================================================
st.divider()
st.subheader("🔗 Parallel Operation Checker")
target_vg = st.text_input("Enter a Vector Group to check against (e.g., Dyn11, Yy0):").strip()

if target_vg:
    # Basic logic: Clock and connection must match
    if target_vg.lower() == vector_group.lower():
        st.success(f"✅ {vector_group} and {target_vg} are compatible for parallel operation.")
    else:
        st.error(f"❌ Incompatible. Ensure the clock number and phase sequence match to avoid short circuits.")

st.info("Note: For parallel operation, voltage ratios and impedance voltages must also be matched.")
