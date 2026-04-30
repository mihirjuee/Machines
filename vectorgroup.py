import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Transformer Vector Pro", layout="wide")
st.title("⚡ Transformer Vector Group & Terminal Analyzer")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔧 Configuration")
hv_type = st.sidebar.selectbox("High Voltage (HV)", ["D", "Y"])
lv_type = st.sidebar.selectbox("Low Voltage (LV)", ["d", "y", "z"])

def get_valid_clocks(hv, lv):
    if hv == lv.upper() or (hv == "D" and lv == "d") or (hv == "Y" and lv == "y"):
        return [0, 6]
    return [1, 11]

valid_clocks = get_valid_clocks(hv_type, lv_type)
clock = st.sidebar.selectbox("Clock Position", valid_clocks)
neutral = st.sidebar.checkbox("Show LV Neutral (n)", value=(lv_type != 'd'), disabled=(lv_type == 'd'))

vector_group = f"{hv_type}{lv_type}{'n' if neutral else ''}{clock}"
phase_shift = clock * 30

# ---------------- METRICS ----------------
m1, m2, m3 = st.columns(3)
m1.metric("Vector Group", vector_group)
m2.metric("Clock Number", f"{clock}")
m3.metric("Phase Shift", f"{phase_shift}°", "Leads" if clock > 6 else "Lags")

# ---------------- PHASOR PLOTTING FUNCTION ----------------
def draw_phasor_diagram(ax, title, type_code, clock_shift=0, is_lv=False):
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    
    # Base angles for A, B, C (0, 120, 240 degrees)
    base_angles = np.radians([0, 120, 240]) - np.radians(clock_shift)
    
    colors = ['#d62728', '#ff7f0e', '#1f77b4'] # Red, Yellow, Blue
    
    # Labels based on side
    labels_start = ["A2", "B2", "C2"] if not is_lv else ["a2", "b2", "c2"]
    labels_end = ["A1", "B1", "C1"] if not is_lv else ["a1", "b1", "c1"]
    
    # Draw Phasors
    for i, angle in enumerate(base_angles):
        # The vector itself represents the winding potential
        ax.annotate('', xy=(angle, 1.0), xytext=(0, 0),
                    arrowprops=dict(edgecolor=colors[i], lw=3, arrowstyle='->'))
        
        # Mark Terminals at center and tip
        ax.text(angle, 1.15, labels_end[i], weight='bold', color=colors[i], ha='center')
        ax.text(angle, 0.1, labels_start[i], weight='bold', color='black', ha='center')

    ax.set_title(title, pad=20, weight='bold')
    ax.set_yticklabels([])
    ax.set_xticklabels(['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

# ---------------- UI LAYOUT: PHASORS ----------------
st.subheader("📊 Detailed Side-by-Side Phasor Diagrams")
col_hv, col_lv = st.columns(2)

with col_hv:
    fig_hv, ax_hv = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    draw_phasor_diagram(ax_hv, f"HV Side ({hv_type}) - Reference", hv_type, is_lv=False)
    st.pyplot(fig_hv)

with col_lv:
    fig_lv, ax_lv = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    draw_phasor_diagram(ax_lv, f"LV Side ({lv_type}) - {clock} o'clock", lv_type, clock_shift=phase_shift, is_lv=True)
    st.pyplot(fig_lv)

# ---------------- DYNAMIC COIL SCHEMATIC ----------------
st.divider()
st.subheader("🧲 Physical Coil & Terminal Connections")

fig_sch, ax_sch = plt.subplots(figsize=(12, 5))

def draw_coil(x, y, n1, n2, color):
    xs = np.linspace(x, x+1.2, 100)
    ys = y + 0.15 * np.sin(2 * np.pi * 5 * (xs-x)/1.2)
    ax_sch.plot(xs, ys, color=color, lw=3)
    ax_sch.text(x-0.4, y, n1, fontsize=9, weight='bold')
    ax_sch.text(x+1.3, y, n2, fontsize=9, weight='bold')
    return (x, y), (x+1.2, y)

# Draw HV/LV sets
h_a, h_b, h_c = [draw_coil(1, y, f"{chr(65+i)}1", f"{chr(65+i)}2", "red") for i, y in enumerate([4, 2.5, 1])]
l_a, l_b, l_c = [draw_coil(8, y, f"{chr(97+i)}1", f"{chr(97+i)}2", "blue") for i, y in enumerate([4, 2.5, 1])]

# Star Connection Logic (Sample)
if hv_type == "Y":
    ax_sch.plot([h_a[1][0], h_a[1][0]+0.3, h_a[1][0]+0.3], [h_a[1][1], h_a[1][1], h_c[1][1]], color='gray', linestyle='--')
    ax_sch.text(h_b[1][0]+0.4, h_b[1][1], "Star Pt (N)", fontsize=8)

if lv_type == "y":
    ax_sch.plot([l_a[1][0], l_a[1][0]+0.3, l_a[1][0]+0.3], [l_a[1][1], l_a[1][1], l_c[1][1]], color='gray', linestyle='--')
    if neutral: ax_sch.text(l_b[1][0]+0.4, l_b[1][1], "n", color='blue', weight='bold')

ax_sch.set_xlim(0, 12); ax_sch.set_ylim(0, 6); ax_sch.axis('off')
st.pyplot(fig_sch)

# ---------------- NOTES ----------------
with st.expander("📚 Engineering Reference"):
    st.markdown(f"""
    - **Vector Group {vector_group}**: The primary HV phasor (A1-A2) is the reference at 12 o'clock.
    - **Terminal Marking**: Standard convention uses '1' for the start and '2' for the end of the winding.
    - **Delta ($D/d$)**: Windings are connected in series. 
    - **Star ($Y/y$)**: Terminals A2, B2, C2 are shorted to form the Neutral point.
    """)
