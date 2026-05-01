# =========================================================
# ADD THESE CHANGES TO YOUR EXISTING CODE
# New Feature:
# ✅ Added Zig-Zag (Z/z) connection for HV & LV
# ✅ Physical zig-zag split-coil winding
# ✅ Vector diagram support
# =========================================================

# ---------------- SIDEBAR UPDATE ----------------
hv_type = st.sidebar.selectbox("HV Side", ["Y", "D", "Z"])
lv_type = st.sidebar.selectbox("LV Side", ["y", "d", "z"])


# =========================================================
# REPLACE draw_coil_connections() WITH THIS VERSION
# =========================================================
def draw_coil_connections(conn_type="Y", is_hv=True):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    color = "red" if is_hv else "blue"
    prefix = ["A", "B", "C"] if is_hv else ["a", "b", "c"]

    x_positions = [2, 6, 10]

    # -----------------------------------------------------
    # NORMAL Y / D COILS
    # -----------------------------------------------------
    if conn_type.upper() in ["Y", "D"]:
        for i, x in enumerate(x_positions):
            ax.add_patch(
                plt.Rectangle(
                    (x - 0.5, 2),
                    1,
                    3,
                    edgecolor=color,
                    facecolor="none",
                    lw=2
                )
            )

            ax.text(x, 5.4, f"{prefix[i]}1",
                    ha="center", color=color, weight="bold")

            ax.text(x, 1.5, f"{prefix[i]}2",
                    ha="center", color=color, weight="bold")

        # STAR
        if conn_type.upper() == "Y":
            ax.plot([2, 6], [1.8, 1.8], "k", lw=2)
            ax.plot([6, 10], [1.8, 1.8], "k", lw=2)
            ax.text(11, 1.8, "Neutral", fontsize=10)

        # DELTA
        else:
            ax.plot([2, 6], [1.8, 5.2], "k", lw=2)
            ax.plot([6, 10], [1.8, 5.2], "k", lw=2)
            ax.plot([10, 2], [1.8, 5.2], "k", lw=2)

    # -----------------------------------------------------
    # ZIG-ZAG CONNECTION
    # Each phase split into two halves on adjacent limbs
    # -----------------------------------------------------
    elif conn_type.upper() == "Z":
        for i, x in enumerate(x_positions):
            # Upper half
            ax.plot(
                [x - 0.3, x + 0.3],
                [4.8, 3.8],
                color=color,
                lw=3
            )

            # Lower half
            ax.plot(
                [x - 0.3, x + 0.3],
                [3.2, 2.2],
                color=color,
                lw=3
            )

            # Labels
            ax.text(x, 5.3, f"{prefix[i]}1",
                    ha="center", color=color, weight="bold")

            ax.text(x, 2.0, f"{prefix[i]}2",
                    ha="center", color=color, weight="bold")

        # Zig-Zag crossover
        ax.plot([2.3, 5.7], [3.8, 3.2], "k", lw=2)
        ax.plot([6.3, 9.7], [3.8, 3.2], "k", lw=2)
        ax.plot([10.3, 2.0], [3.8, 3.2], "k", lw=2)

        # Neutral
        ax.plot([2, 6], [1.5, 1.5], "k", lw=2)
        ax.plot([6, 10], [1.5, 1.5], "k", lw=2)
        ax.text(11, 1.5, "Neutral", fontsize=10)

    ax.set_title(
        f"{'HV' if is_hv else 'LV'} Coil Connection ({conn_type})"
    )

    ax.axis("off")
    return fig


# =========================================================
# UPDATE PHASOR FUNCTION
# =========================================================
def draw_phasor_clock(base_angles, labels, color, conn_type, title):
    fig, ax = plt.subplots(
        figsize=(5,5),
        subplot_kw={'projection':'polar'}
    )

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    for ang, lab in zip(base_angles, labels):
        ax.annotate(
            "",
            xy=(ang,1),
            xytext=(0,0),
            arrowprops=dict(
                arrowstyle="->",
                lw=2,
                color=color
            )
        )

        ax.text(
            ang,
            1.15,
            lab,
            color=color,
            weight='bold'
        )

    # DELTA
    if conn_type.upper() == "D":
        closed_angles = np.append(base_angles, base_angles[0])
        ax.plot(closed_angles, [1]*4, color=color, lw=2)

    # ZIG-ZAG
    elif conn_type.upper() == "Z":
        for ang in base_angles:
            ax.plot([ang, ang + np.radians(30)],
                    [0.5, 1],
                    color=color,
                    lw=2)

    ax.set_xticks(np.linspace(0,2*np.pi,12,endpoint=False))

    ax.set_xticklabels(
        ['12','1','2','3','4','5','6',
         '7','8','9','10','11']
    )

    ax.set_yticklabels([])
    ax.set_title(title)

    return fig


# =========================================================
# NOTES SECTION UPDATE
# =========================================================
st.markdown(f"""
### Connection Summary:
- **HV Side:** {hv_type}
- **LV Side:** {lv_type}
- **Clock Number:** {clock}

### Supported Connections:
- **Y/y** → Star
- **D/d** → Delta
- **Z/z** → Zig-Zag

### Zig-Zag Features:
- Split winding per phase
- Neutral stabilization
- Harmonic reduction
- Better unbalanced load handling

### Delta Bridge:
A2 → B1  
B2 → C1  
C2 → A1
""")
