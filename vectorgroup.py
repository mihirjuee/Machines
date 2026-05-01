import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- VALID GROUPS ----------------
VALID_GROUPS = {
    "Group I (0°)": {"clock": 0},
    "Group II (180°)": {"clock": 6},
    "Group III (30° Lag)": {"clock": 1},
    "Group IV (30° Lead)": {"clock": 11},
}

st.set_page_config(layout="wide")
st.title("⚡ Transformer Actual Coil Connection Analyzer")

# ---------------- SIDEBAR ----------------
group_name = st.sidebar.selectbox("Select Valid Group", list(VALID_GROUPS.keys()))
hv_conn = st.sidebar.selectbox("HV Connection", ["Y", "D"])
lv_conn = st.sidebar.selectbox("LV Connection", ["y", "d"])

clock = VALID_GROUPS[group_name]["clock"]
vector_group = f"{hv_conn}{lv_conn}{clock}"

# ---------------- COIL POSITIONS ----------------
HV_X = [2, 6, 10]
LV_X = [2, 6, 10]


# ---------------- DRAW COILS ----------------
def draw_actual_connections(conn_type, is_hv=True, clock=0):
    fig, ax = plt.subplots(figsize=(9, 5))

    color = "red" if is_hv else "blue"
    prefix = ["A", "B", "C"] if is_hv else ["a", "b", "c"]
    x_positions = HV_X if is_hv else LV_X

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    # Draw coils
    terminals = {}
    for i, x in enumerate(x_positions):
        ax.plot([x, x], [2, 5], color=color, lw=8, solid_capstyle='round')

        top = f"{prefix[i]}1"
        bottom = f"{prefix[i]}2"

        terminals[top] = (x, 5)
        terminals[bottom] = (x, 2)

        ax.text(x, 5.4, top, ha='center', color=color, weight='bold')
        ax.text(x, 1.6, bottom, ha='center', color=color, weight='bold')

    # ---------------- STAR ----------------
    if conn_type.upper() == "Y":
        neutral_y = 1
        joined = [f"{prefix[0]}2", f"{prefix[1]}2", f"{prefix[2]}2"]

        for t in joined:
            x, y = terminals[t]
            ax.plot([x, x], [y, neutral_y], 'k', lw=2)

        ax.plot(
            [terminals[joined[0]][0], terminals[joined[-1]][0]],
            [neutral_y, neutral_y],
            'k', lw=2
        )

        ax.text(11, neutral_y, "N", fontsize=12, weight='bold')

    # ---------------- DELTA ----------------
    else:
        if is_hv or clock in [0, 6]:
            pairs = [
                (f"{prefix[0]}2", f"{prefix[1]}1"),
                (f"{prefix[1]}2", f"{prefix[2]}1"),
                (f"{prefix[2]}2", f"{prefix[0]}1"),
            ]

        elif clock == 1:  # LV lag
            pairs = [
                (f"{prefix[0]}2", f"{prefix[2]}1"),
                (f"{prefix[1]}2", f"{prefix[0]}1"),
                (f"{prefix[2]}2", f"{prefix[1]}1"),
            ]

        elif clock == 11:  # LV lead
            pairs = [
                (f"{prefix[0]}2", f"{prefix[1]}1"),
                (f"{prefix[1]}2", f"{prefix[0]}1"),
                (f"{prefix[2]}2", f"{prefix[2]}1"),
            ]

        for start, end in pairs:
            x1, y1 = terminals[start]
            x2, y2 = terminals[end]
            ax.plot([x1, x2], [y1, y2], 'k', lw=2)

    ax.set_title(
        f"{'HV' if is_hv else 'LV'} Actual Coil Connections ({conn_type})",
        fontsize=14,
        weight='bold'
    )

    ax.axis("off")
    return fig


# ---------------- PHASOR ----------------
def draw_phasor(clock):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    hv_angles = np.radians([0, 120, 240])
    lv_angles = hv_angles + np.radians(clock * 30)

    for ang in hv_angles:
        ax.arrow(ang, 0, 0, 1, color='red', lw=2)

    for ang in lv_angles:
        ax.arrow(ang, 0, 0, 0.85, color='blue', lw=2)

    ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax.set_xticklabels(
        ['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    )
    ax.set_yticklabels([])
    ax.set_title(f"Clock Position: {clock}")
    return fig


# ---------------- UI ----------------
st.header(f"Vector Group: {vector_group}")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(draw_actual_connections(hv_conn, True, clock))

with col2:
    st.pyplot(draw_actual_connections(lv_conn, False, clock))

st.pyplot(draw_phasor(clock))

# ---------------- NOTES ----------------
st.subheader("Active Connection Logic")
st.write(f"Selected group: {group_name}")
st.write(f"Clock number: {clock}")
st.write("Only valid IEC/IITM vector groups shown.")
