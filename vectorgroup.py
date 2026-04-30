import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIGURATION & DATA ----------------
# Valid groups based on IITM Standard
VALID_GROUPS = {
    "Group I (0°)": {"clock": 0, "label": "0° Displacement", "desc": "In-phase connection"},
    "Group II (180°)": {"clock": 6, "label": "180° Displacement", "desc": "Phase opposition"},
    "Group III (30° lag)": {"clock": 1, "label": "-30° Displacement", "desc": "Standard for Dy1"},
    "Group IV (30° lead)": {"clock": 11, "label": "+30° Displacement", "desc": "Standard for Dy11"}
}

st.set_page_config(page_title="EE Interactive: Transformer Vector Groups", layout="wide")
st.title("⚡ Transformer Vector Group & Coil Analyzer")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Configuration")
selected_grp_name = st.sidebar.selectbox("Select Valid Vector Group", list(VALID_GROUPS.keys()))
hv_type = st.sidebar.selectbox("HV Side (Primary)", ["Y", "D"])
lv_type = st.sidebar.selectbox("LV Side (Secondary)", ["y", "d"])

selected_grp = VALID_GROUPS[selected_grp_name]
clock = selected_grp["clock"]
vg_name = f"{hv_type}{lv_type}{clock}"

# ---------------- DRAWING FUNCTIONS ----------------

def draw_coil_connections(conn_type, is_hv=True):
    """Draws physical coils on limbs with bridge connections"""
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    color = "#d62728" if is_hv else "#1f77b4" # Red for HV, Blue for LV
    p = "A" if is_hv else "a"
    
    # Draw 3 limbs
    for i, phase in enumerate(['1', '2', '3']):
        x = 2 + i * 3
        # Draw Winding
        ax.add_patch(plt.Rectangle((x-0.6, 2), 1.2, 2, color=color, alpha=0.2, hatch='///'))
        # Terminals
        ax.text(x, 4.3, f"{p}{i+1}_2", ha='center', weight='bold', color=color)
        ax.text(x, 1.4, f"{p}{i+1}_1", ha='center', weight='bold', color=color)
        
    # Wiring Logic
    if conn_type.upper() in ['Y', 'y']:
        # Star: Short all '1' terminals for neutral
        ax.plot([1.4, 7.6], [1.7, 1.7], color='black', lw=2.5, linestyle='--')
        ax.text(8.5, 1.6, "Neutral", fontsize=8)
    else:
        # Delta: Mesh (Finish of one to start of next)
        ax.annotate('', xy=(4.4, 1.7), xytext=(2, 4.1), arrowprops=dict(arrowstyle='-', lw=1.5))
        ax.annotate('', xy=(7.4, 1.7), xytext=(5, 4.1), arrowprops=dict(arrowstyle='-', lw=1.5))
        ax.annotate('', xy=(1.4, 1.7), xytext=(8, 4.1), arrowprops=dict(arrowstyle='-', lw=1.5, connectionstyle="arc3,rad=-0.4"))

    ax.set_title(f"{'HV' if is_hv else 'LV'} Physical Coil Wiring ({conn_type})", pad=15)
    ax.axis('off')
    return fig

def draw_phasor_clock(angles, labels, color, conn_type, title):
    """Draws the phasor diagram on a clock face"""
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1) # Clockwise rotation
    
    # Draw geometry (Star lines or Delta triangle)
    if conn_type.upper() in ['Y', 'y']:
        for ang in angles:
            ax.plot([0, ang], [0, 1], color=color, lw=2.5)
    else:
        # Mesh connection visuals
        d_theta = np.append(angles, angles[0])
        ax.plot(d_theta, [1, 1, 1, 1], color=color, lw=2.5)

    # Add terminal labels
    for i, ang in enumerate(angles):
        ax.annotate('', xy=(ang, 1), xytext=(0, 0), arrowprops=dict(edgecolor=color, arrowstyle='->', lw=2))
        ax.text(ang, 1.25, labels[i], weight='bold', color=color, ha='center')
        
    ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax.set_xticklabels(['12','1','2','3','4','5','6','7','8','9','10','11'])
    ax.set_yticklabels([])
    ax.set_title(title, weight='bold', pad=20)
    return fig

# ---------------- MAIN UI ----------------
st.header(f"Vector Group: {vg_name}")
st.write(f"**Displacement:** {selected_grp['label']} ({selected_grp['desc']})")

# Math
hv_angles = np.radians([0, 120, 240])
lv_angles = hv_angles + np.radians(clock * 30)

col1, col2 = st.columns(2)

with col1:
    st.pyplot(draw_coil_connections(hv_type, is_hv=True))
    st.pyplot(draw_phasor_clock(hv_angles, ["A2", "B2", "C2"], "#d62728", hv_type, "HV Phasor (Primary)"))

with col2:
    st.pyplot(draw_coil_connections(lv_type, is_hv=False))
    st.pyplot(draw_phasor_clock(lv_angles, ["a2", "b2", "c2"], "#1f77b4", lv_type, f"LV Phasor ({selected_grp['label']})"))

# ---------------- TECHNICAL NOTES ----------------
st.divider()
st.subheader("Technical Connection Properties")
st.markdown(f"""
* **Polarity Check**: If EMF rises from terminal 1 to 2 in the HV winding, the same occurs in the LV winding for this model.
* **Connection Choice**: 
    * **{hv_type}**: Chosen for the Primary side based on system grounding and insulation requirements.
    * **{lv_type}**: Secondary configuration tailored for load requirements (e.g., star for neutral access).
* **Parallel Operation**: This **{vg_name}** unit can only be paralleled with units from **{selected_grp_name}** to avoid severe circulating currents.
""")
