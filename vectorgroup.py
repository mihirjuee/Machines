import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# TRANSFORMER VECTOR GROUP & COIL CONNECTION ANALYZER
# Features:
# ✅ Valid IEC Groups Only (0, 6, 1, 11)
# ✅ Shows INVALID combinations
# ✅ Supports Y / D / Z
# ✅ Actual coil winding diagrams
# ✅ Dynamic vector clock
# =========================================================

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Transformer Vector Group Analyzer",
    layout="wide"
)

st.title("⚡ Transformer Vector Group & Coil Connection Analyzer")

# ---------------- VALID GROUPS ----------------
VALID_GROUPS = {
    "Group I (0°)": {
        "clock": 0,
        "label": "0°",
        "desc": "In-phase"
    },
    "Group II (180°)": {
        "clock": 6,
        "label": "180°",
        "desc": "Phase opposition"
    },
    "Group III (30° lag)": {
        "clock": 1,
        "label": "30° Lag",
        "desc": "LV lags HV by 30°"
    },
    "Group IV (30° lead)": {
        "clock": 11,
        "label": "30° Lead",
        "desc": "LV leads HV by 30°"
    }
}

# =========================================================
# VALIDATION FUNCTION
# =========================================================
def is_valid_vector_group(hv, lv, clock):
    hv = hv.upper()
    lv = lv.upper()

    # 0° and 180° groups
    if clock in [0, 6]:
        return True

    # 30° groups
    elif clock in [1, 11]:
        valid_pairs = [
            ("Y", "D"), ("D", "Y"),
            ("Y", "Z"), ("Z", "Y")
        ]
        return (hv, lv) in valid_pairs

    return False


# ---------------- SIDEBAR ----------------
st.sidebar.header("Configuration")

selected_grp_name = st.sidebar.selectbox(
    "Select Vector Group",
    list(VALID_GROUPS.keys())
)

hv_type = st.sidebar.selectbox(
    "HV Side",
    ["Y", "D", "Z"]
)

lv_type = st.sidebar.selectbox(
    "LV Side",
    ["y", "d", "z"]
)

selected_grp = VALID_GROUPS[selected_grp_name]
clock = selected_grp["clock"]

vg_name = f"{hv_type}{lv_type}{clock}"

# ---------------- VALIDATION ----------------
if not is_valid_vector_group(hv_type, lv_type, clock):
    st.error(
        f"""
❌ Invalid Vector Group Combination: {vg_name}

Clock {clock} is not valid for:
HV = {hv_type}
LV = {lv_type}

Allowed:
• Clock 0 / 6 → Any practical Y/D/Z combination  
• Clock 1 → Yd1, Dy1, Yz1, Zy1  
• Clock 11 → Yd11, Dy11, Yz11, Zy11
"""
    )
    st.stop()


# =========================================================
# DRAW COIL CONNECTIONS
# =========================================================
def draw_coil_connections(conn_type="Y", is_hv=True):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    color = "red" if is_hv else "blue"
    prefix = ["A", "B", "C"] if is_hv else ["a", "b", "c"]

    x_positions = [2, 6, 10]

    # -----------------------------------------------------
    # STAR / DELTA
    # -----------------------------------------------------
    if conn_type.upper() in ["Y", "D"]:

        # Draw coils
        for i, x in enumerate(x_positions):
            y = np.linspace(2, 5, 200)
            coil = x + 0.25 * np.sin(10 * np.pi * (y - 2) / 3)

            ax.plot(coil, y, color=color, lw=2)

            ax.text(
                x,
                5.3,
                f"{prefix[i]}1",
                ha="center",
                color=color,
                weight="bold"
            )

            ax.text(
                x,
                1.6,
                f"{prefix[i]}2",
                ha="center",
                color=color,
                weight="bold"
            )

        # STAR CONNECTION
        if conn_type.upper() == "Y":
            neutral_x = 6
            neutral_y = 1.2

            # A2
            ax.plot([2, 2], [2, neutral_y], "k", lw=2)

            # B2
            ax.plot([6, 6], [2, neutral_y], "k", lw=2)

            # C2
            ax.plot([10, 10], [2, neutral_y], "k", lw=2)

            # Neutral bus
            ax.plot([2, 10], [neutral_y, neutral_y], "k", lw=2)

            # Neutral node
            ax.scatter(neutral_x, neutral_y, color="black", s=40)

            ax.text(10.8, neutral_y, "N", fontsize=12, weight="bold")

        # DELTA CONNECTION
        else:
            ax.plot([2, 6], [2, 5], "k", lw=2)     # A2-B1
            ax.plot([6, 10], [2, 5], "k", lw=2)    # B2-C1
            ax.plot([10, 2], [2, 5], "k", lw=2)    # C2-A1

    # -----------------------------------------------------
    # ZIG-ZAG
    # -----------------------------------------------------
    elif conn_type.upper() == "Z":

        for i, x in enumerate(x_positions):

            # Upper split
            y1 = np.linspace(4, 5, 100)
            c1 = x + 0.2 * np.sin(8 * np.pi * (y1 - 4))

            # Lower split
            y2 = np.linspace(2.5, 3.5, 100)
            c2 = x + 0.2 * np.sin(8 * np.pi * (y2 - 2.5))

            ax.plot(c1, y1, color=color, lw=2)
            ax.plot(c2, y2, color=color, lw=2)

            ax.text(
                x,
                5.3,
                f"{prefix[i]}1",
                ha="center",
                color=color,
                weight="bold"
            )

            ax.text(
                x,
                2.2,
                f"{prefix[i]}2",
                ha="center",
                color=color,
                weight="bold"
            )

        # Zig-zag links
        ax.plot([2.2, 5.8], [4, 3.5], "k", lw=2)
        ax.plot([6.2, 9.8], [4, 3.5], "k", lw=2)
        ax.plot([10.2, 2], [4, 3.5], "k", lw=2)

        # Neutral
        ax.plot([2, 10], [1.5, 1.5], "k", lw=2)
        ax.text(10.8, 1.5, "N", fontsize=12, weight="bold")

    ax.set_title(
        f"{'HV' if is_hv else 'LV'} Coil Connection ({conn_type})",
        weight="bold"
    )

    ax.axis("off")

    return fig


# =========================================================
# VECTOR / PHASOR CLOCK
# =========================================================
def draw_phasor_clock(hv_angles, lv_angles, hv_conn, lv_conn):
    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw={"projection": "polar"}
    )

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # HV
    for ang, lab in zip(hv_angles, ["A", "B", "C"]):
        ax.annotate(
            "",
            xy=(ang, 1.0),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", lw=3, color="red")
        )
        ax.text(ang, 1.12, lab, color="red", weight="bold")

    # LV
    for ang, lab in zip(lv_angles, ["a", "b", "c"]):
        ax.annotate(
            "",
            xy=(ang, 0.8),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", lw=3, color="blue")
        )
        ax.text(ang, 0.92, lab, color="blue", weight="bold")

    # Delta polygons
    if hv_conn.upper() == "D":
        hv_closed = np.append(hv_angles, hv_angles[0])
        ax.plot(hv_closed, [1]*4, color="red", lw=2)

    if lv_conn.upper() == "D":
        lv_closed = np.append(lv_angles, lv_angles[0])
        ax.plot(lv_closed, [0.8]*4, color="blue", lw=2)

    # Zig-zag indicators
    if hv_conn.upper() == "Z":
        for ang in hv_angles:
            ax.plot([ang, ang + np.radians(30)], [0.5, 1], color="red", lw=1.5)

    if lv_conn.upper() == "Z":
        for ang in lv_angles:
            ax.plot([ang, ang + np.radians(30)], [0.4, 0.8], color="blue", lw=1.5)

    ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax.set_xticklabels(
        ["12","1","2","3","4","5","6","7","8","9","10","11"]
    )

    ax.set_yticklabels([])

    ax.set_title(
        f"Vector Clock Diagram ({clock} o'clock = {selected_grp['desc']})",
        weight="bold",
        pad=25
    )

    return fig


# ---------------- ANGLES ----------------
hv_angles = np.radians([0, 120, 240])
lv_angles = hv_angles + np.radians(clock * 30)

# =========================================================
# DISPLAY
# =========================================================
st.header(f"Vector Group: {vg_name}")

st.write(
    f"### Phase Displacement: {selected_grp['label']} ({selected_grp['desc']})"
)

col1, col2 = st.columns(2)

with col1:
    st.pyplot(draw_coil_connections(hv_type, True))

with col2:
    st.pyplot(draw_coil_connections(lv_type, False))

st.pyplot(
    draw_phasor_clock(
        hv_angles,
        lv_angles,
        hv_type,
        lv_type
    )
)

# =========================================================
# NOTES
# =========================================================
st.divider()

st.subheader("Technical Notes")

st.markdown(f"""
### Connection Summary:
- **HV Side:** {hv_type}
- **LV Side:** {lv_type}
- **Clock Number:** {clock}

### Supported Connections:
- **Y / y** → Star
- **D / d** → Delta
- **Z / z** → Zig-Zag

### IEC Rules:
- **0 / 6** → Broad valid combinations  
- **1** → Yd1, Dy1, Yz1, Zy1  
- **11** → Yd11, Dy11, Yz11, Zy11  

### Important:
Invalid combinations are automatically blocked.
""")
