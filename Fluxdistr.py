# ============================================================
# CORRECT 3-PHASE INDUCTION MOTOR AIR-GAP FLUX WAVEFORM
# FIXES:
# ✅ Wave amplitude properly scales with Bm
# ✅ True sinusoidal waveform around air-gap
# ✅ Pole count changes spatial cycles
# ✅ Air-gap waveform visually appears sinusoidal
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Correct Air-Gap Flux Waveform", layout="wide")

st.title("⚡ Correct Resultant Air-Gap Flux Waveform")
st.markdown("### True sinusoidal flux distribution with proper Bm scaling and pole variation")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density Bm", 0.1, 3.0, 1.0, 0.1)
wt_deg = st.sidebar.slider("Electrical Angle ωt (degrees)", 0, 360, 0)

wt = np.radians(wt_deg)

# Pole pairs
p = pole // 2

# ---------------- SPACE AXIS ----------------
theta_mech_deg = np.linspace(0, 360, 4000)
theta_mech = np.radians(theta_mech_deg)

# ============================================================
# TRUE RESULTANT FLUX DENSITY
# ============================================================
B = 1.5 * Bm * np.cos(p * theta_mech - wt)

# For air-gap shape:
# Radius offset + signed sinusoidal modulation
r_mean = 0.86
scale = 0.10 * Bm   # directly scales with Bm

R_wave = r_mean + scale * np.cos(p * theta_mech - wt)

# Cartesian conversion
X_wave = R_wave * np.cos(theta_mech)
Y_wave = R_wave * np.sin(theta_mech)

Ns = 120 * f / pole

# ============================================================
# METRICS
# ============================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Bm", f"{Bm:.2f} T")
col2.metric("Poles", f"{pole}")
col3.metric("Peak Flux", f"{1.5*Bm:.2f}")
col4.metric("Synchronous Speed", f"{Ns:.1f} RPM")

# ============================================================
# AIR-GAP WAVEFORM
# ============================================================
st.subheader("🌀 True Sinusoidal Flux Waveform in the Air-Gap")

fig, ax = plt.subplots(figsize=(10,10))

# Radii
r_rotor = 0.55
r_stator = 1.18
r_axis = r_mean

# Rotor & stator
rotor = Circle((0,0), r_rotor, fill=False, linewidth=3)
stator = Circle((0,0), r_stator, fill=False, linewidth=3)
axis_circle = Circle((0,0), r_axis, fill=False, linestyle='--', linewidth=1)

ax.add_patch(rotor)
ax.add_patch(stator)
ax.add_patch(axis_circle)

# Main axes
ax.plot([-r_stator, r_stator], [0,0], linestyle='--', linewidth=1)
ax.plot([0,0], [-r_stator, r_stator], linestyle='--', linewidth=1)

# ============================================================
# PLOT TRUE SINUSOIDAL AIR-GAP SHAPE
# ============================================================
ax.plot(X_wave, Y_wave, linewidth=4)

# ============================================================
# MULTIPLE N/S POLES
# ============================================================
for k in range(pole):
    pole_angle = (wt + k*np.pi) / p

    if k >= pole:
        continue

# Better pole positions:
for k in range(pole):
    angle = (2*np.pi/pole) * k + wt/p

    label = "N" if k % 2 == 0 else "S"

    ax.text(
        1.28*np.cos(angle),
        1.28*np.sin(angle),
        label,
        fontsize=16,
        fontweight='bold',
        ha='center',
        va='center'
    )

# ============================================================
# DEGREE MARKINGS
# ============================================================
for ang in np.arange(0, 360, 360/pole):
    a = np.radians(ang)
    ax.text(
        1.38*np.cos(a),
        1.38*np.sin(a),
        f"{int(ang)}°",
        fontsize=10,
        ha='center'
    )

# Labels
ax.text(0, 0, "ROTOR", ha='center', va='center',
        fontsize=14, fontweight='bold')

ax.text(0, 1.48, "STATOR", ha='center',
        fontsize=15, fontweight='bold')

ax.text(0, -1.48,
        f"{pole}-Pole Sinusoidal Air-Gap Flux",
        ha='center', fontsize=12)

# Formatting
ax.set_aspect('equal')
ax.set_xlim(-1.55, 1.55)
ax.set_ylim(-1.55, 1.55)
ax.axis('off')

st.pyplot(fig)

# ============================================================
# LINEAR FLUX DISTRIBUTION
# ============================================================
st.subheader("📈 Actual Flux Density vs Mechanical Space Angle")

fig2, ax2 = plt.subplots(figsize=(14,6))

ax2.plot(theta_mech_deg, B, linewidth=4)

ax2.axhline(0, linestyle='--', linewidth=1)

# Pole divisions
for k in range(pole + 1):
    ax2.axvline(k * 360/pole, linestyle=':', linewidth=1)

ax2.set_title(f"{pole}-Pole Resultant Flux Density")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("Flux Density B(θ)")

ax2.set_xticks(np.arange(0, 361, 360/pole))

ax2.grid(True)

st.pyplot(fig2)

# ============================================================
# POLAR SINUSOID
# ============================================================
# ============================================================
# POLAR FLUX DISTRIBUTION WITH REAL FLUX PATH
# Shows:
# ✅ Flux lines connect North → South
# ✅ NSNS pole arrangement for multi-pole machines
# ✅ No negative radial plotting
# ✅ Air-gap field path visualization
# ============================================================
st.subheader("🧭 Polar Flux Path (North → South)")

fig3 = plt.figure(figsize=(9,9))
ax3 = fig3.add_subplot(111, projection='polar')

# ============================================================
# MAGNITUDE ONLY FOR ENVELOPE
# ============================================================
B_mag = np.abs(B)
ax3.plot(theta_mech, B_mag, linewidth=2)

# ============================================================
# POLE SPACING
# ============================================================
pole_spacing = 2 * np.pi / pole

# Pole center radius
r_pole = np.max(B_mag)

# Store pole positions
pole_angles = []

# ============================================================
# DRAW POLES
# ============================================================
for k in range(pole):

    pole_angle = (wt / p) + k * pole_spacing
    pole_angles.append(pole_angle)

    pole_label = "N" if k % 2 == 0 else "S"

    # Pole radial marker
    ax3.plot(
        [pole_angle, pole_angle],
        [0, r_pole],
        linewidth=2
    )

    # Pole label
    ax3.text(
        pole_angle,
        r_pole + 0.2 * Bm,
        pole_label,
        fontsize=16,
        fontweight='bold',
        ha='center'
    )

# ============================================================
# DRAW FLUX LINES FROM EACH N TO NEXT S
# ============================================================
# Flux leaves N and enters adjacent S through air-gap
# ============================================================
for k in range(0, pole, 2):

    # North pole
    theta_n = pole_angles[k]

    # Adjacent South pole
    theta_s = pole_angles[(k + 1) % pole]

    # Smooth angular transition
    if theta_s < theta_n:
        theta_s += 2 * np.pi

    theta_flux = np.linspace(theta_n, theta_s, 200)

    # Arc bulges outward to resemble field path
    r_flux = r_pole + 0.25 * Bm * np.sin(
        np.pi * (theta_flux - theta_n) / (theta_s - theta_n)
    )

    # Flux line
    ax3.plot(theta_flux, r_flux, linewidth=3)

    # Arrow near center of flux path
    mid_idx = len(theta_flux) // 2

    ax3.annotate(
        "",
        xy=(theta_flux[mid_idx + 2], r_flux[mid_idx + 2]),
        xytext=(theta_flux[mid_idx - 2], r_flux[mid_idx - 2]),
        arrowprops=dict(
            lw=2,
            arrowstyle="->"
        )
    )

# ============================================================
# OPTIONAL INNER RETURN PATH (Rotor side)
# ============================================================
for k in range(1, pole, 2):

    theta_s = pole_angles[k]
    theta_n = pole_angles[(k + 1) % pole]

    if theta_n < theta_s:
        theta_n += 2 * np.pi

    theta_return = np.linspace(theta_s, theta_n, 200)

    # Inner path
    r_return = r_pole - 0.35 * Bm * np.sin(
        np.pi * (theta_return - theta_s) / (theta_n - theta_s)
    )

    ax3.plot(theta_return, r_return, linestyle='--', linewidth=2)

# ============================================================
# SETTINGS
# ============================================================
ax3.set_title(f"{pole}-Pole Flux Lines (North → South)")
ax3.set_rticks([])
ax3.grid(True)

st.pyplot(fig3)
# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Correct Equation")

st.markdown(f"""
### Resultant Air-Gap Flux:
**B(θ,t) = 1.5 Bm cos(pθ − ωt)**

Where:

**Bm = {Bm:.2f}**  
**p = P/2 = {p}**

---

## Corrections:
### Bm:
Controls amplitude directly

### Pole Number:
Controls number of sinusoidal cycles in space

### Shape:
Always sinusoidal for distributed winding

---

## Example:
### {pole}-pole machine:
{p} complete sinusoidal cycles over 360° mechanical space

### Synchronous Speed:
**Ns = 120f/P = {Ns:.1f} RPM**
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ Distributed 3-phase windings create a true sinusoidal rotating magnetic field in the air-gap.")
