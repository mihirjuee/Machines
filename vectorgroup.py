import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIGURATION ----------------
VALID_GROUPS = {
    "Group I (0°)": {"clock": 0, "label": "0°", "desc": "In-phase"},
    "Group II (180°)": {"clock": 6, "label": "180°", "desc": "Phase opposition"},
    "Group III (30° lag)": {"clock": 1, "label": "LV lags HV by 30°"},
    "Group IV (30° lead)": {"clock": 11, "label": "LV leads HV by 30°"}
}

st.set_page_config(page_title="Transformer Vector Group Analyzer", layout="wide")
st.title("⚡ Transformer Vector Group & Coil Connection Analyzer")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Configuration")
selected_grp_name = st.sidebar.selectbox("Select Vector Group", list(VALID_GROUPS.keys()))
hv_type = st.sidebar.selectbox("HV Side", ["Y", "D"])
lv_type = st.sidebar.selectbox("LV Side", ["y", "d"])

selected_grp = VALID_GROUPS[selected_grp_name]
clock = selected_grp["clock"]
vg_name = f"{hv_type}{lv_type}{clock}"

# ---------------- COIL CONNECTION ----------------
def draw_coil_connections(conn_type="Y", is_hv=True):
    fig, ax = plt.subplots(figsize=(7,4))
    ax.set_xlim(0,12)
    ax.set_ylim(0,8)

    color = "red" if is_hv else "blue"
    prefix = ["A","B","C"] if is_hv else ["a","b","c"]

    x_positions = [2, 6, 10]

    # Draw coils
    for i, x in enumerate(x_positions):
        ax.add_patch(plt.Rectangle((x-0.6,2),1.2,3,
                                   edgecolor=color,
                                   facecolor='none',
                                   lw=2))
        ax.text(x,5.4,f"{prefix[i]}1",ha='center',color=color,weight='bold')
        ax.text(x,1.5,f"{prefix[i]}2",ha='center',color=color,weight='bold')

    # STAR CONNECTION
    if conn_type.upper() == "Y":
        ax.plot([2,6],[1.8,1.8],'k',lw=2)
        ax.plot([6,10],[1.8,1.8],'k',lw=2)
        ax.text(11,1.8,"Neutral",fontsize=10)

    # DELTA CONNECTION
    else:
        # A2-B1
        ax.plot([2,6],[1.8,5.2],'k',lw=2)
        # B2-C1
        ax.plot([6,10],[1.8,5.2],'k',lw=2)
        # C2-A1
        ax.plot([10,2],[1.8,5.2],'k',lw=2)

    ax.set_title(f"{'HV' if is_hv else 'LV'} Coil Connection ({conn_type})")
    ax.axis("off")
    return fig

# ---------------- PHASOR CLOCK ----------------
def draw_phasor_clock(base_angles, labels, color, conn_type, title):
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw={'projection':'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # Draw vectors
    for ang, lab in zip(base_angles, labels):
        ax.annotate("",
                    xy=(ang,1),
                    xytext=(0,0),
                    arrowprops=dict(arrowstyle="->", lw=2, color=color))
        ax.text(ang,1.15,lab,color=color,weight='bold')

    # Draw delta triangle
    if conn_type.upper() == "D":
        closed_angles = np.append(base_angles, base_angles[0])
        ax.plot(closed_angles,[1]*4,color=color,lw=2)

    ax.set_xticks(np.linspace(0,2*np.pi,12,endpoint=False))
    ax.set_xticklabels(['12','1','2','3','4','5','6','7','8','9','10','11'])
    ax.set_yticklabels([])
    ax.set_title(title)
    return fig

# ---------------- ANGLE CALCULATION ----------------
hv_angles = np.radians([0,120,240])

# Clock notation:
# Positive clock means LV lags HV clockwise
lv_angles = hv_angles + np.radians(clock*30)

# ---------------- DISPLAY ----------------
st.header(f"Vector Group: {vg_name}")
st.write(f"**Phase Displacement:** {selected_grp['label']}")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(draw_coil_connections(hv_type, True))
    st.pyplot(draw_phasor_clock(hv_angles,
                                ["A","B","C"],
                                "red",
                                hv_type,
                                "HV Reference"))

with col2:
    st.pyplot(draw_coil_connections(lv_type, False))
    st.pyplot(draw_phasor_clock(lv_angles,
                                ["a","b","c"],
                                "blue",
                                lv_type,
                                f"LV ({clock} o'clock)"))

# ---------------- NOTES ----------------
st.divider()
st.subheader("Technical Notes")
st.markdown(f"""
### Connection Summary:
- **HV Side:** {hv_type}
- **LV Side:** {lv_type}
- **Clock Number:** {clock}

### Parallel Operation:
Only transformers in **{selected_grp_name}** can operate in parallel.

### Delta Bridge Sequence:
A2 → B1  
B2 → C1  
C2 → A1

### Star Neutral:
A2 + B2 + C2 connected together
""")
