# ============================================================
# MMF DISTRIBUTION OF AC WINDINGS (CORRECT COIL MAGNETIC AXIS)
# Shows:
# ✅ Pole-dependent MMF distribution
# ✅ Correct coil magnetic axis through actual coil pair
# ✅ Textbook-style dashed flux lines
# ✅ Alternating N-S poles
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="MMF Distribution of AC Windings", layout="wide")

st.title("⚡ MMF Distribution of AC Windings")
st.markdown("### Correct coil magnetic axis + pole-wise MMF distribution")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Machine Parameters")

pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Ni = st.sidebar.slider("Ampere-Conductors (Ni)", 1, 20, 10)

# Pole pairs
p = pole // 2

# ============================================================
# MAIN FIGURE
# ============================================================
fig, ax = plt.subplots(figsize=(10,10))

# Radii
r_stator = 1.25
r_rotor = 0.78
r_coil = 1.02

# Draw stator and rotor
stator = Circle((0,0), r_stator, fill=False, linewidth=3)
rotor = Circle((0,0), r_rotor, fill=False, linewidth=3)

ax.add_patch(stator)
ax.add_patch(rotor)

# ============================================================
# POLE POSITIONS
# ============================================================
pole_angles = np.linspace(0, 2*np.pi, pole, endpoint=False)

# ============================================================
# DRAW POLES + COILS
# ============================================================
for k, ang in enumerate(pole_angles):

    # Alternate poles
    pole_label = "N" if k % 2 == 0 else "S"

    # Pole label in air-gap
    ax.text(
        0.88*np.cos(ang),
        0.88*np.sin(ang),
        pole_label,
        fontsize=16,
        fontweight='bold',
        ha='center',
        va='center'
    )

    # Coil side marker
    x_coil = r_coil * np.cos(ang)
    y_coil = r_coil * np.sin(ang)

    # Dot/Cross
    coil_symbol = "⊙" if k % 2 == 0 else "⊗"

    ax.text(
        x_coil,
        y_coil,
        coil_symbol,
        fontsize=18,
        fontweight='bold',
        ha='center',
        va='center'
    )

# ============================================================
# FLUX / MMF LINES (N → S)
# ============================================================
for k in range(0, pole, 2):

    ang_n = pole_angles[k]
    ang_s = pole_angles[(k+1) % pole]

    # Ensure continuity
    if ang_s < ang_n:
        ang_s += 2*np.pi

    # Multiple dashed loops
    for offset in [0.12, 0.28, 0.44]:

        theta = np.linspace(ang_n, ang_s, 300)

        # Outer bulging path
        r_loop = r_rotor + offset + 0.18*np.sin(
            np.pi * (theta - ang_n) / (ang_s - ang_n)
        )

        x = r_loop * np.cos(theta)
        y = r_loop * np.sin(theta)

        ax.plot(
            x,
            y,
            linestyle='--',
            linewidth=1.4
        )

        # Arrow
        idx = len(theta)//2

        ax.annotate(
            "",
            xy=(x[idx+2], y[idx+2]),
            xytext=(x[idx-2], y[idx-2]),
            arrowprops=dict(
                arrowstyle="->",
                lw=1.3
            )
        )

# ============================================================
# CORRECT COIL MAGNETIC AXIS
# Axis through first N-S pole pair center
# ============================================================
axis_angle = (pole_angles[0] + pole_angles[1]) / 2

# Full axis line
x1 = -1.5 * np.cos(axis_angle)
y1 = -1.5 * np.sin(axis_angle)

x2 = 1.5 * np.cos(axis_angle)
y2 = 1.5 * np.sin(axis_angle)

ax.plot(
    [x1, x2],
    [y1, y2],
    linestyle='--',
    linewidth=1.8
)

# Arrow
ax.arrow(
    1.2*np.cos(axis_angle),
    1.2*np.sin(axis_angle),
    0.22*np.cos(axis_angle),
    0.22*np.sin(axis_angle),
    head_width=0.05,
    head_length=0.08,
    linewidth=2
)

# Label
ax.text(
    1.6*np.cos(axis_angle),
    1.6*np.sin(axis_angle),
    "Coil magnetic axis",
    fontsize=12,
    ha='left' if np.cos(axis_angle) >= 0 else 'right',
    va='center'
)

# ============================================================
# THETA ANGLE MARKER
# ============================================================
theta_arc = np.linspace(0, axis_angle, 100)

r_theta = 0.42

ax.plot(
    r_theta*np.cos(theta_arc),
    r_theta*np.sin(theta_arc),
    linewidth=1.2
)

theta_mid = axis_angle / 2

ax.text(
    0.52*np.cos(theta_mid),
    0.52*np.sin(theta_mid),
    r"$\theta$",
    fontsize=14
)

# ============================================================
# Ni LABEL
# ============================================================
ax.text(
    0,
    1.48,
    f"{Ni} ampere-conductors",
    fontsize=12,
    fontweight='bold',
    ha='center'
)

# ============================================================
# TITLE
# ============================================================
ax.text(
    0,
    -1.55,
    f"{pole}-Pole MMF Distribution",
    fontsize=14,
    fontweight='bold',
    ha='center'
)

# ============================================================
# FORMATTING
# ============================================================
ax.set_aspect('equal')
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.axis('off')

st.pyplot(fig)

# ============================================================
# MMF WAVEFORM
# ============================================================
st.subheader("📈 Spatial MMF Waveform")

theta_deg = np.linspace(0, 360, 3000)
theta = np.radians(theta_deg)

# Pole-dependent MMF
F = Ni * np.cos(p * theta)

fig2, ax2 = plt.subplots(figsize=(14,5))

ax2.plot(theta_deg, F, linewidth=4)

ax2.axhline(0, linestyle='--')

# Pole boundaries
for k in range(pole + 1):
    ax2.axvline(
        k * 360 / pole,
        linestyle=':',
        linewidth=1
    )

ax2.set_title(f"{pole}-Pole Spatial MMF Distribution")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("MMF")

ax2.set_xticks(np.arange(0, 361, 360/pole))

ax2.grid(True)

st.pyplot(fig2)

# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 MMF Equation")

st.markdown(f"""
### Spatial MMF:
**F(θ) = Ni cos(pθ)**

Where:

**Ni = {Ni} ampere-conductors**  
**p = P/2 = {p}**

---

## Key Meaning:
### 2-Pole:
1 spatial cycle

### 4-Pole:
2 spatial cycles

### 6-Pole:
3 spatial cycles

### 8-Pole:
4 spatial cycles

---

## Important:
The coil magnetic axis always passes through the center of the active N-S pole pair.
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ Distributed windings produce a sinusoidal spatial MMF wave aligned with the coil magnetic axis.")
