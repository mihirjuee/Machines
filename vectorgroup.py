import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- IITM VECTOR GROUP DEFINITIONS ----------------
groups = {
    "Group I (0°)": {"clock": 0, "label": "0° Displacement"},
    "Group II (180°)": {"clock": 6, "label": "180° Displacement"},
    "Group III (30° lag)": {"clock": 1, "label": "-30° Displacement"},
    "Group IV (30° lead)": {"clock": 11, "label": "+30° Displacement"}
}

# ---------------- SIDEBAR ----------------
st.sidebar.header("IITM Standard Config")
selected_grp = st.sidebar.selectbox("Select Vector Group", list(groups.keys()))
hv_type = st.sidebar.selectbox("HV Side (Capitals)", ["Y", "D"])
lv_type = st.sidebar.selectbox("LV Side (Small)", ["y", "d"])

clock = groups[selected_grp]["clock"]
vg_name = f"{hv_type}{lv_type}{clock}"

# ---------------- VISUALIZATION LOGIC ----------------
def draw_diagram(title, angles, labels, color, conn_type):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)  # Clockwise
    
    # Coordinates for the three phases
    r = 1.0
    theta = angles
    
    # Draw the connection geometry (The "Star" or "Delta" shape)
    if conn_type.upper() in ['Y', 'Y']:
        # Star: Lines from center to each point
        for i in range(3):
            ax.plot([0, theta[i]], [0, r], color=color, lw=2, linestyle='-')
    else:
        # Delta: Lines connecting the points to each other (Mesh)
        # Close the triangle by adding the first point to the end
        delta_theta = np.append(theta, theta[0])
        delta_r = [r, r, r, r]
        ax.plot(delta_theta, delta_r, color=color, lw=2, linestyle='-')

    # Draw Phasor Arrows (The EMF direction)
    for i in range(3):
        ax.annotate('', xy=(theta[i], r), xytext=(0, 0) if conn_type.upper() in ['Y', 'Y'] else (theta[i-1], r),
                    arrowprops=dict(edgecolor=color, lw=1.5, arrowstyle='->', alpha=0.6))
        
        # Labels for terminals
        ax.text(theta[i], r + 0.2, labels[i], weight='bold', color=color, ha='center')

    ax.set_title(title, pad=30, weight='bold', size=14)
    ax.set_yticklabels([])
    # Clock face numbering
    ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax.set_xticklabels(['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
    return fig

# ---------------- CALCULATIONS ----------------
# Standard HV reference (A-phase at 12 o'clock)
hv_angles = np.radians([0, 120, 240])
hv_labels = ["A2", "B2", "C2"]

# Displacement logic
shift_deg = clock * 30
lv_angles = hv_angles + np.radians(shift_deg)
lv_labels = ["a2", "b2", "c2"]

# ---------------- UI LAYOUT ----------------
st.title("⚡ Transformer Vector Group Simulator")
st.write(f"Visualizing the **{vg_name}** configuration following IITM standards.")

col_hv, col_lv = st.columns(2)

with col_hv:
    st.pyplot(draw_diagram(f"HV: {hv_type} Side", hv_angles, hv_labels, "red", hv_type))

with col_lv:
    st.pyplot(draw_diagram(f"LV: {lv_type} Side ({groups[selected_grp]['label']})", lv_angles, lv_labels, "blue", lv_type))

# ---------------- CONNECTION DETAILS ----------------
st.divider()
st.subheader("🔗 Coil & Terminal Connections")

def get_details(ctype, is_hv):
    t1, t2 = ("1", "2") # Terminal suffix
    p = "A,B,C" if is_hv else "a,b,c"
    
    if ctype.upper() in ['Y', 'Y']:
        return f"**Star Connection:** Terminals {p}{t1} are shorted to form the Neutral. Power is connected to {p}{t2}."
    else:
        return f"**Delta Connection:** Terminals are connected in a mesh. {p[0]}{t2} connects to {p[2]}{t1}, etc., forming a closed loop."

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"#### Primary ({hv_type})")
    st.info(get_details(hv_type, True))
with c2:
    st.markdown(f"#### Secondary ({lv_type})")
    st.info(get_details(lv_type, False))

st.warning("**Note on Parallel Operation:** Transformers must belong to the same group to be paralleled. Connecting a Group I with a Group III will cause a 30° phase mismatch and high circulating currents.")
