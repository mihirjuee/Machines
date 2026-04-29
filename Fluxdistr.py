# ============================================================
# MMF DISTRIBUTION OF AC WINDINGS ACCORDING TO NUMBER OF POLES
# Shows:
# ✅ Stator + rotor air-gap structure
# ✅ Alternating N-S poles around circumference
# ✅ Coil magnetic axes
# ✅ Dashed MMF / flux lines like textbook figure
# ✅ Pole-dependent spatial MMF distribution
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Pole-wise MMF Distribution", layout="wide")

st.title("⚡ MMF Distribution of AC Windings")
st.markdown("### Textbook-style MMF distribution according to number of poles")

# ---------------- INPUTS ----------------
st.sidebar.header("Machine Parameters")

pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Ni = st.sidebar.slider("Ampere-Conductors (Ni)", 1, 20, 10)

# Pole pairs
p = pole // 2

# ============================================================
# FIGURE
# ============================================================
fig, ax = plt.subplots(figsize=(10,10))

# Radii
r_outer = 1.25
r_inner = 0.78

# Stator & rotor circles
stator = Circle((0,0), r_outer, fill=False, linewidth=3)
rotor = Circle((0,0), r_inner, fill=False, linewidth=3)

ax.add_patch(stator)
ax.add_patch(rotor)

# ============================================================
# POLE LOCATIONS
# ============================================================
pole_angles = np.linspace(0, 2*np.pi, pole, endpoint=False)

# Coil side radius
r_coil = 1.02

# ============================================================
# DRAW COILS + N/S LABELS
# ============================================================
for k, ang in enumerate(pole_angles):

    # Alternate N/S
    pole_label = "N" if k % 2 == 0 else "S"

    # Pole text inside air-gap
    ax.text(
        0.9*np.cos(ang),
        0.9*np.sin(ang),
        pole_label,
        fontsize=16,
        fontweight='bold',
        ha='center',
        va='center'
    )

    # Coil side markers
    x_coil = r_coil * np.cos(ang)
    y_coil = r_coil * np.sin(ang)

    # Dot / cross style
    if k % 2 == 0:
        coil_symbol = "⊙"   # current out
    else:
        coil_symbol = "⊗"   # current in

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
# MMF / FLUX LINES (TEXTBOOK STYLE)
# Dashed loops from each N → adjacent S
# ============================================================
for k in range(0, pole, 2):

    ang_n = pole_angles[k]
    ang_s = pole_angles[(k+1) % pole]

    # Ensure forward continuity
    if ang_s < ang_n:
        ang_s += 2*np.pi

    # Multiple dashed loops
    for offset in [0.15, 0.32, 0.50]:

        theta = np.linspace(ang_n, ang_s, 300)

        # Outer bulging loop
        r_loop = r_inner + offset + 0.18*np.sin(
            np.pi*(theta-ang_n)/(ang_s-ang_n)
        )

        x = r_loop * np.cos(theta)
        y = r_loop * np.sin(theta)

        ax.plot(x, y, linestyle='--', linewidth=1.5)

        # Arrow direction
        idx = len(theta)//2
        ax.annotate(
            "",
            xy=(x[idx+2], y[idx+2]),
            xytext=(x[idx-2], y[idx-2]),
            arrowprops=dict(
                arrowstyle="->",
                lw=1.5
            )
        )

# ============================================================
# COIL MAGNETIC AXIS
# ============================================================
ax.plot(
    [-1.5, 1.5],
    [0, 0],
    linestyle='--',
    linewidth=1.5
)

ax.arrow(
    1.25, 0,
    0.25, 0,
    head_width=0.05,
    head_length=0.08,
    linewidth=2
)

ax.text(
    1.55, 0.05,
    "Coil magnetic axis",
    fontsize=12,
    ha='left'
)

# ============================================================
# THETA MARKER
# ============================================================
arc = Arc((0,0), 2.2, 2.2, angle=0, theta1=0, theta2=25, linewidth=1.5)
ax.add_patch(arc)

ax.text(1.05, 0.22, r"$\theta$", fontsize=14)

# ============================================================
# Ni LABEL
# ============================================================
ax.text(
    0.15,
    1.38,
    f"{Ni} ampere-conductors",
    fontsize=12,
    fontweight='bold'
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
st.subheader("📈 Spatial MMF Distribution")

theta_deg = np.linspace(0, 360, 2000)
theta = np.radians(theta_deg)

# MMF waveform
F = Ni * np.cos(p * theta)

fig2, ax2 = plt.subplots(figsize=(14,5))

ax2.plot(theta_deg, F, linewidth=4)

ax2.axhline(0, linestyle='--')

# Pole divisions
for k in range(pole + 1):
    ax2.axvline(k * 360 / pole, linestyle=':', linewidth=1)

ax2.set_title(f"{pole}-Pole MMF Distribution")
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

## Pole Effect:
### {pole}-pole machine:
- {pole} alternating poles around stator
- {p} spatial cycles over 360°
- MMF axis determines magnetic orientation

---

## Key Idea:
More poles create more alternating N-S regions and compress the MMF wavelength in space.
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ Distributed AC windings create a spatial sinusoidal MMF wave whose pole count depends on winding arrangement.")
