import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# TRANSFORMER VECTOR GROUP ANALYZER (VALID GROUPS ONLY)
# Shows:
# ✅ Actual coil winding connections (not box blocks)
# ✅ HV/LV dynamic update per vector group
# ✅ Correct vector/phasor clock diagram
# ✅ ONLY valid IEC groups: 0, 6, 1, 11
# =========================================================

st.set_page_config(page_title="Transformer Vector Group Analyzer", layout="wide")

# ---------------- VALID GROUPS ONLY ----------------
VALID_GROUPS = {
    "Group I  (Yy0 / Dd0 / Dy0 / Yd0)": {
        "clock": 0,
        "phase": "0° In Phase"
    },
    "Group II (Yy6 / Dd6 / Dy6 / Yd6)": {
        "clock": 6,
        "phase": "180° Phase Shift"
    },
    "Group III (Yd1 / Dy1)": {
        "clock": 1,
        "phase": "30° Lag"
    },
    "Group IV (Yd11 / Dy11)": {
        "clock": 11,
        "phase": "30° Lead"
    }
}

# ---------------- SIDEBAR ----------------
st.sidebar.title("Configuration")

selected_group = st.sidebar.selectbox(
    "Select Valid IEC Vector Group",
    list(VALID_GROUPS.keys())
)

hv_type = st.sidebar.selectbox("HV Connection", ["Y", "D"])

# Restrict LV choices for valid groups
clock = VALID_GROUPS[selected_group]["clock"]

if clock in [1, 11]:
    # practical groups
    lv_type = "d" if hv_type == "Y" else "y"
else:
    lv_type = st.sidebar.selectbox("LV Connection", ["y", "d"])

vector_group = f"{hv_type}{lv_type}{clock}"

# ---------------- ANGLES ----------------
hv_angles = np.radians([0, 120, 240])
lv_angles = hv_angles + np.radians(clock * 30)

# =========================================================
# DRAW ACTUAL COILS
# =========================================================
def draw_transformer_coils(conn_type, is_hv=True, clock=0):
    fig, ax = plt.subplots(figsize=(9, 5))

    color = "red" if is_hv else "blue"
    prefix = ["A", "B", "C"] if is_hv else ["a", "b", "c"]

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    terminals = {}
    x_positions = [2, 6, 10]

    # Draw real coils
    for i, x in enumerate(x_positions):
        y = np.linspace(2, 5, 200)
        turns = x + 0.25 * np.sin(12 * np.pi * (y - 2) / 3)
        ax.plot(turns, y, color=color, lw=2.5)

        t1 = f"{prefix[i]}1"
        t2 = f"{prefix[i]}2"

        terminals[t1] = (x, 5)
        terminals[t2] = (x, 2)

        ax.text(x, 5.4, t1, ha="center", color=color, weight="bold")
        ax.text(x, 1.5, t2, ha="center", color=color, weight="bold")

    # ---------------- STAR ----------------
    if conn_type.upper() == "Y":
        neutral_y = 1

        for i in range(3):
            x, y = terminals[f"{prefix[i]}2"]
            ax.plot([x, x], [y, neutral_y], "k", lw=2)

        ax.plot([2, 10], [neutral_y, neutral_y], "k", lw=2)
        ax.text(11, neutral_y, "Neutral", weight="bold")

    # ---------------- DELTA ----------------
    else:
        if clock == 0:
            pairs = [
                (f"{prefix[0]}2", f"{prefix[1]}1"),
                (f"{prefix[1]}2", f"{prefix[2]}1"),
                (f"{prefix[2]}2", f"{prefix[0]}1"),
            ]

        elif clock == 6:
            # Reverse polarity = 180°
            pairs = [
                (f"{prefix[0]}1", f"{prefix[1]}2"),
                (f"{prefix[1]}1", f"{prefix[2]}2"),
                (f"{prefix[2]}1", f"{prefix[0]}2"),
            ]

        elif clock == 1:
            # Lagging 30°
            pairs = [
                (f"{prefix[0]}2", f"{prefix[2]}1"),
                (f"{prefix[1]}2", f"{prefix[0]}1"),
                (f"{prefix[2]}2", f"{prefix[1]}1"),
            ]

        elif clock == 11:
            # Leading 30°
            pairs = [
                (f"{prefix[0]}2", f"{prefix[1]}1"),
                (f"{prefix[1]}2", f"{prefix[2]}1"),
                (f"{prefix[2]}2", f"{prefix[0]}1"),
            ]

        for start, end in pairs:
            x1, y1 = terminals[start]
            x2, y2 = terminals[end]
            ax.plot([x1, x2], [y1, y2], "k", lw=2)

    ax.set_title(
        f"{'HV' if is_hv else 'LV'} Coil Connections ({conn_type})",
        weight="bold"
    )

    ax.axis("off")
    return fig


# =========================================================
# VECTOR DIAGRAM
# =========================================================
def draw_vector_diagram():
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # HV
    hv_labels = ["A", "B", "C"]
    for ang, lab in zip(hv_angles, hv_labels):
        ax.annotate(
            "",
            xy=(ang, 1.0),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", lw=3, color="red")
        )
        ax.text(ang, 1.12, lab, color="red", weight="bold")

    # LV
    lv_labels = ["a", "b", "c"]
    for ang, lab in zip(lv_angles, lv_labels):
        ax.annotate(
            "",
            xy=(ang, 0.8),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", lw=3, color="blue")
        )
        ax.text(ang, 0.92, lab, color="blue", weight="bold")

    # Clock
    ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
    ax.set_xticklabels(
        ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    )

    ax.set_yticklabels([])

    ax.set_title(
        f"Vector Clock Diagram ({clock} o'clock = {VALID_GROUPS[selected_group]['phase']})",
        weight="bold",
        pad=25
    )

    return fig


# =========================================================
# MAIN UI
# =========================================================
st.title("⚡ Transformer Vector Group & Coil Analyzer")

st.header(f"Vector Group: {vector_group}")
st.write(f"### Phase Displacement: {VALID_GROUPS[selected_group]['phase']}")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(draw_transformer_coils(hv_type, True, clock))

with col2:
    st.pyplot(draw_transformer_coils(lv_type, False, clock))

st.pyplot(draw_vector_diagram())

# =========================================================
# NOTES
# =========================================================
st.divider()

st.subheader("Technical Notes")

st.markdown(f"""
### Active Group:
**{selected_group}**

### Clock Number:
**{clock}**

### Interpretation:
- **0** → HV and LV in phase
- **6** → 180° displacement
- **1** → LV lags HV by 30°
- **11** → LV leads HV by 30°

### Important:
Only valid IEC/IITM standard vector groups are selectable.
Invalid clock numbers like **5, 7, 9** are blocked.
""")
