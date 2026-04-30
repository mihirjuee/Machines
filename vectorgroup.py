import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG & STYLING ----------------
st.set_page_config(page_title="IIT Madras Vector Group Analyzer", layout="wide")
st.title("⚡ Polyphase Transformer Vector Group Analyzer")
st.caption("Based on IIT Madras Electrical Machines I: Prof. Vasudevan, Prof. Rao & Prof. Rao")

# ---------------- IITM VECTOR GROUP LOGIC ----------------
# Group I: 0° displacement (12 o'clock)
# Group II: 180° displacement (6 o'clock)
# Group III: 30° lag (1 o'clock)
# Group IV: 30° lead (11 o'clock)

groups = {
    "Group I (0°)": {"clocks": [0], "desc": "Zero phase displacement"},
    "Group II (180°)": {"clocks": [6], "desc": "180° phase displacement"},
    "Group III (-30°)": {"clocks": [1], "desc": "30° lag phase displacement of secondary"},
    "Group IV (+30°)": {"clocks": [11], "desc": "30° lead phase displacement of secondary"}
}

# ---------------- SIDEBAR CONFIGURATION ----------------
st.sidebar.header("Transformer Parameters")
selected_group = st.sidebar.selectbox("Select IITM Vector Group", list(groups.keys()))
hv_conn = st.sidebar.selectbox("HV Winding (Capital Letters)", ["Y (Star)", "D (Mesh)", "Z (Zig-zag)"])
lv_conn = st.sidebar.selectbox("LV Winding (Small Letters)", ["y (star)", "d (mesh)", "z (zig-zag)"])

clock = groups[selected_group]["clocks"][0]
phase_shift = clock * 30

# Construction of vector group string (e.g., Yy0, Dy11)[cite: 1]
vg_str = f"{hv_conn[0]}{lv_conn[0]}{clock}"

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Vector Group", vg_str)
with col2:
    st.metric("Phase Shift", f"{phase_shift}°")
with col3:
    st.info(groups[selected_group]["desc"])

# ---------------- PHASOR DIAGRAM (EMF VECTOR) ----------------
# Standard convention: EMF rises from 1 to 2[cite: 1]
st.subheader("📊 E.M.F. Vector Diagrams")
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# Primary (HV) - Reference
angles_hv = np.radians([0, 120, 240])
labels_hv = ['$A_2$', '$B_2$', '$C_2$']
for i, angle in enumerate(angles_hv):
    ax.annotate('', xy=(angle, 1.0), xytext=(0, 0),
                arrowprops=dict(edgecolor='red', lw=3, arrowstyle='->'))
    ax.text(angle, 1.1, labels_hv[i], weight='bold', color='red')

# Secondary (LV) - Shifted
angles_lv = angles_hv + np.radians(phase_shift if clock == 11 else -phase_shift)
labels_lv = ['$a_2$', '$b_2$', '$c_2$']
for i, angle in enumerate(angles_lv):
    ax.annotate('', xy=(angle, 0.7), xytext=(0, 0),
                arrowprops=dict(edgecolor='blue', lw=2, linestyle='--', arrowstyle='->'))
    ax.text(angle, 0.8, labels_lv[i], weight='bold', color='blue')

ax.set_yticklabels([])
ax.set_xticklabels(['12 (0°)', '1', '2', '3', '4', '5', '6 (180°)', '7', '8', '9', '10', '11'])
st.pyplot(fig)

# ---------------- TECHNICAL CONSIDERATIONS[cite: 1] ----------------
st.divider()
st.subheader("📘 Technical and Economic Considerations")

# Dynamic notes based on selections[cite: 1]
if "Y" in hv_conn and "y" in lv_conn:
    st.write("**Star/Star (Yy0, Yy6):** Economical for small high voltage transformers. Reduces insulation costs significantly. May require a tertiary mesh winding to stabilize oscillating neutral[cite: 1].")
elif "D" in hv_conn and "d" in lv_conn:
    st.write("**Mesh/Mesh (Dd0, Dd6):** Economical for large low voltage transformers. Handles unbalanced loads well and attenuates triplen harmonics[cite: 1].")
elif "Z" in hv_conn or "z" in lv_conn:
    st.write("**Zig-zag (Z):** Interconnection of phases that eliminates oscillating neutral problems. Requires 15% more turns for the same voltage, increasing cost[cite: 1].")

st.markdown("""
### IIT Madras Standard Conventions[cite: 1]:
* **Terminal Designations**: Each winding has ends designated **1** and **2**. 
* **EMF Polarity**: If induced emf rises from $A_1$ to $A_2$ on the HV side, it rises from $a_1$ to $a_2$ on the LV side.
* **Notation**: HV uses Capital letters ($D, Y, Z$); LV uses small letters ($d, y, z$).
* **Parallel Operation**: These vector groups are critical when connecting two or more transformers in parallel to ensure phase compatibility.
""")
