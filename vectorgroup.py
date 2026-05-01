import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# TRANSFORMER VECTOR GROUP & COIL CONNECTION ANALYZER
# =========================================================

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Transformer Vector Group Analyzer",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Transformer Vector Group & Coil Connection Analyzer")
st.write("Analyze phase displacement and winding connections according to IEC 60076 standards.")

# ---------------- CONSTANTS & DATA ----------------
VALID_GROUPS = {
    "Group I (0°)": {"clock": 0, "label": "0°", "desc": "In-phase (No displacement)"},
    "Group II (180°)": {"clock": 6, "label": "180°", "desc": "Phase opposition"},
    "Group III (30° lag)": {"clock": 1, "label": "-30° (Lag)", "desc": "LV lags HV by 30°"},
    "Group IV (30° lead)": {"clock": 11, "label": "+30° (Lead)", "desc": "LV leads HV by 30°"}
}

# ---------------- VALIDATION LOGIC ----------------
def is_valid_vector_group(hv, lv, clock):
    hv, lv = hv.upper(), lv.upper()
    
    # Clock 0 and 6: Same winding types (Yy, Dd, Zz)
    if clock in [0, 6]:
        return hv == lv
    
    # Clock 1 and 11: Dissimilar winding types (Yd, Dy, Yz, Zy)
    if clock in [1, 11]:
        return hv != lv
    
    return False

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔧 Configuration")

selected_grp_name = st.sidebar.selectbox(
    "Select Phase Displacement",
    list(VALID_GROUPS.keys())
)

hv_type = st.sidebar.selectbox("HV Connection (Primary)", ["Y", "D", "Z"], index=0)
lv_type = st.sidebar.selectbox("LV Connection (Secondary)", ["y", "d", "z"], index=1)

selected_grp = VALID_GROUPS[selected_grp_name]
clock = selected_grp["clock"]
vg_full_name = f"{hv_type}{lv_type}{clock}"

# ---------------- VALIDATION CHECK ----------------
is_valid = is_valid_vector_group(hv_type, lv_type, clock)

if not is_valid:
    st.error(f"### ❌ Invalid Group: {vg_full_name}")
    st.info(f"""
    **Standard IEC Logic:**
    *   **Clocks 0 & 6:** Require similar connections (e.g., Yy0, Dd6).
    *   **Clocks 1 & 11:** Require dissimilar connections (e.g., Yd1, Dy11, Yz1).
    """)
    st.stop()

# ---------------- PLOTTING FUNCTIONS ----------------

def draw_coil_connections(conn_type="Y", is_hv=True):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    
    color = "#d32f2f" if is_hv else "#1976d2"
    prefix = ["A", "B", "C"] if is_hv else ["a", "b", "c"]
    x_positions = [2, 6, 10]

    # Draw Coils (Standard for Y and D)
    if conn_type.upper() in ["Y", "D"]:
        for i, x in enumerate(x_positions):
            y = np.linspace(2.5, 5.5, 200)
            coil = x + 0.3 * np.sin(12 * np.pi * (y - 2.5) / 3)
            ax.plot(coil, y, color=color, lw=2.5)
            ax.text(x, 6.0, f"{prefix[i]}1", ha="center", weight="bold", color=color)
            ax.text(x, 2.0, f"{prefix[i]}2", ha="center", weight="bold", color=color)

        if conn_type.upper() == "Y":
            # Star point
            ax.plot([2, 10], [1.2, 1.2], "k--", lw=1)
            for x in x_positions:
                ax.plot([x, x], [2, 1.2], "k", lw=1.5)
            ax.scatter(6, 1.2, color="black", zorder=5)
            ax.text(10.5, 1.2, "N", weight="bold")
        else:
            # Delta loop (simplified schematic)
            ax.plot([2, 6], [2, 5.5], "k", lw=1.5)
            ax.plot([6, 10], [2, 5.5], "k", lw=1.5)
            ax.plot([10, 2], [2, 5.5], "k", lw=1.5)

    elif conn_type.upper() == "Z":
        # Zig-zag has two winding halves per limb
        for i, x in enumerate(x_positions):
            # Upper half
            yu = np.linspace(4.5, 6, 100)
            ax.plot(x + 0.2 * np.sin(8 * np.pi * (yu-4.5)), yu, color=color, lw=2)
            # Lower half
            yl = np.linspace(2.5, 4, 100)
            ax.plot(x + 0.2 * np.sin(8 * np.pi * (yl-2.5)), yl, color=color, lw=2)
            ax.text(x, 6.3, f"{prefix[i]}1", ha="center", weight="bold", color=color)
        ax.plot([2, 10], [1.5, 1.5], "k--", lw=1) # Neutral

    ax.set_title(f"{'High' if is_hv else 'Low'} Voltage Winding ({conn_type})", pad=15, weight="bold")
    ax.axis("off")
    return fig

def draw_phasor_clock(hv_angles, lv_angles, clock_val):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # HV Phasors
    for ang, lab in zip(hv_angles, ["A", "B", "C"]):
        ax.annotate("", xy=(ang, 1.0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", lw=3, color="#d32f2f"))
        ax.text(ang, 1.15, lab, color="#d32f2f", weight="bold", fontsize=12)

    # LV Phasors
    for ang, lab in zip(lv_angles, ["a", "b", "c"]):
        ax.annotate("", xy=(ang, 0.75), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", lw=3, color="#1976d2"))
        ax.text(ang, 0.85, lab, color="#1976d2", weight="bold", fontsize=10)

    ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax.set_xticklabels(["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
    ax.set_yticklabels([])
    ax.grid(True, alpha=0.3)
    return fig

# ---------------- DISPLAY ----------------
st.success(f"### Current Vector Group: {vg_full_name}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Phasor Relationship")
    hv_angles = np.radians([0, 120, 240])
    # Clock 1 is 30 deg lag (-30), Clock 11 is 30 deg lead (+30)
    # Clock is standard (Clock * 30 degrees)
    lv_angles = hv_angles + np.radians(clock * 30)
    st.pyplot(draw_phasor_clock(hv_angles, lv_angles, clock))

with col2:
    st.subheader("📖 Connection Properties")
    st.info(f"""
    **Displacement:** {selected_grp['label']}  
    **Description:** {selected_grp['desc']}  
    **Phase Sequence:** A-B-C (Positive)
    """)
    st.metric("Clock Angle", f"{clock * 30}°")

st.divider()

st.subheader("🛠 Winding Schematic")
c_hv, c_lv = st.columns(2)
with c_hv:
    st.pyplot(draw_coil_connections(hv_type, True))
with c_lv:
    st.pyplot(draw_coil_connections(lv_type, False))

# ---------------- FOOTER ----------------
st.sidebar.divider()
st.sidebar.caption("Educational tool for Electrical Engineers. Logic follows IEC 60076 standards.")
