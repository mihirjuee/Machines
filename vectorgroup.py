import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- IITM VECTOR GROUP DEFINITIONS ----------------
# Group I: 0° displacement
# Group II: 180° displacement 
# Group III: 30° lag (-30°)
# Group IV: 30° lead (+30°)

groups = {
    "Group I (0°)": {"clock": 0, "label": "0° Displacement"},
    "Group II (180°)": {"clock": 6, "label": "180° Displacement"},
    "Group III (30° lag)": {"clock": 1, "label": "-30° Displacement"},
    "Group IV (30° lead)": {"clock": 11, "label": "+30° Displacement"}
}

# ---------------- SIDEBAR ----------------
st.sidebar.header("IITM Standard Config")
selected_grp = st.sidebar.selectbox("Select Vector Group", list(groups.keys()))
hv_type = st.sidebar.selectbox("HV Side (Capitals)", ["Y", "D", "Z"])
lv_type = st.sidebar.selectbox("LV Side (Small)", ["y", "d", "z"])

clock = groups[selected_grp]["clock"]
vg_name = f"{hv_type}{lv_type}{clock}"

# ---------------- VECTOR DIAGRAMS ----------------
st.subheader(f"📈 E.M.F. Vector Diagrams for {vg_name}")

def create_phasor_plot(title, angles, labels, color, is_secondary=False):
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1) # Clockwise
    
    # Draw the three phases
    for i, angle in enumerate(angles):
        # EMF rises from center (1) to tip (2)
        ax.annotate('', xy=(angle, 1.0), xytext=(0, 0),
                    arrowprops=dict(edgecolor=color, lw=2.5, arrowstyle='->'))
        # Label terminals
        ax.text(angle, 1.2, labels[i], weight='bold', color=color, ha='center')
        ax.text(0, 0.1, "1", weight='bold', color='black', ha='center') # Neutral/Common point

    ax.set_title(title, pad=20, weight='bold')
    ax.set_yticklabels([])
    ax.set_xticklabels(['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
    return fig

# Calculate Angles
hv_angles = np.radians([0, 120, 240])
hv_labels = ["A2", "B2", "C2"] # EMF rises to terminal 2

# Displacement logic[cite: 1]
shift_deg = clock * 30
lv_angles = hv_angles + np.radians(shift_deg)
lv_labels = ["a2", "b2", "c2"]

col_hv, col_lv = st.columns(2)

with col_hv:
    st.pyplot(create_phasor_plot("HV Primary Side", hv_angles, hv_labels, "red"))

with col_lv:
    st.pyplot(create_phasor_plot(f"LV Secondary Side ({groups[selected_grp]['label']})", lv_angles, lv_labels, "blue"))

# ---------------- TERMINAL LOGIC & NOTES[cite: 1] ----------------
st.divider()
st.markdown(f"""
### Connection Properties for {vg_name}[cite: 1]:
* **Phase Displacement**: This transformer belongs to **{selected_grp}**, representing a {groups[selected_grp]['label']} relative to the HV side[cite: 1].
* **Terminal Polarities**: Following the polarity test and dot convention, if EMF rises from $A_1$ to $A_2$, it rises from $a_1$ to $a_2$ on the secondary[cite: 1].
* **Connection Types**:
    * **{hv_type}**: Primary side is connected in {'Star' if hv_type=='Y' else 'Mesh' if hv_type=='D' else 'Zig-zag'} fashion[cite: 1].
    * **{lv_type}**: Secondary side is connected in {'star' if lv_type=='y' else 'mesh' if lv_type=='d' else 'zig-zag'} fashion[cite: 1].
* **Parallel Operation**: This vector group configuration must match exactly for proper functioning when deploying multiple units[cite: 1].
""")
