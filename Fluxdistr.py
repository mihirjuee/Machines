# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:31:07 2026

@author: Hp
"""

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
# POLAR FLUX DISTRIBUTION (CORRECT ALL N→S FLUX PATHS)
# Replace ONLY your existing POLAR PLOT section with this
# ============================================================

st.subheader("🧭 Polar Flux Path (Each North → Adjacent South)")

fig3 = plt.figure(figsize=(9,9))
ax3 = fig3.add_subplot(111, projection='polar')

# ============================================================
# FLUX ENVELOPE (Magnitude only)
# ============================================================
B_mag = np.abs(B)
ax3.plot(theta_mech, B_mag, linewidth=2)

# ============================================================
# BASIC PARAMETERS
# ============================================================
pole_spacing = 2 * np.pi / pole
r_pole = np.max(B_mag)

# Pole angular positions
pole_angles = []

# ============================================================
# DRAW ALL POLES
# ============================================================
for k in range(pole):

    # Pole center
    pole_angle = (wt / p) + k * pole_spacing
    pole_angles.append(pole_angle)

    # Alternate N-S
    pole_label = "N" if k % 2 == 0 else "S"

    # Radial pole axis
    ax3.plot(
        [pole_angle, pole_angle],
        [0, r_pole],
        linewidth=2
    )

    # Pole label
    ax3.text(
        pole_angle,
        r_pole + 0.25 * Bm,
        pole_label,
        fontsize=16,
        fontweight='bold',
        ha='center'
    )

# ============================================================
# DRAW OUTER AIR-GAP FLUX LINES
# EACH NORTH CONNECTS TO NEXT SOUTH
# ============================================================
for k in range(0, pole, 2):

    theta_n = pole_angles[k]
    theta_s = pole_angles[(k + 1) % pole]

    # Wrap-around correction
    if theta_s < theta_n:
        theta_s += 2 * np.pi

    # Smooth angular path
    theta_flux = np.linspace(theta_n, theta_s, 300)

    # Outer arc (air-gap path)
    r_flux = r_pole + 0.30 * Bm * np.sin(
        np.pi * (theta_flux - theta_n) / (theta_s - theta_n)
    )

    # Plot outer flux
    ax3.plot(theta_flux, r_flux, linewidth=3)

    # Arrow direction N → S
    mid = len(theta_flux) // 2

    ax3.annotate(
        "",
        xy=(theta_flux[mid + 3], r_flux[mid + 3]),
        xytext=(theta_flux[mid - 3], r_flux[mid - 3]),
        arrowprops=dict(
            arrowstyle="->",
            lw=2
        )
    )

# ============================================================
# DRAW INNER RETURN FLUX LINES
# EACH SOUTH RETURNS TO NEXT NORTH
# ============================================================
for k in range(1, pole, 2):

    theta_s = pole_angles[k]
    theta_n = pole_angles[(k + 1) % pole]

    if theta_n < theta_s:
        theta_n += 2 * np.pi

    theta_return = np.linspace(theta_s, theta_n, 300)

    # Inner return path through rotor
    r_return = r_pole - 0.45 * Bm * np.sin(
        np.pi * (theta_return - theta_s) / (theta_n - theta_s)
    )

    # Prevent collapse near origin
    r_return = np.maximum(r_return, 0.15 * r_pole)

    # Plot return flux
    ax3.plot(theta_return, r_return, linestyle='--', linewidth=2)

    # Arrow direction S → N (return)
    mid = len(theta_return) // 2

    ax3.annotate(
        "",
        xy=(theta_return[mid + 3], r_return[mid + 3]),
        xytext=(theta_return[mid - 3], r_return[mid - 3]),
        arrowprops=dict(
            arrowstyle="->",
            lw=1.8
        )
    )

# ============================================================
# OPTIONAL: COMPLETE FLUX LOOPS FOR VISUAL CLARITY
# ============================================================
for k in range(0, pole, 2):

    # Previous south to current north
    theta_prev_s = pole_angles[k - 1]
    theta_curr_n = pole_angles[k]

    if theta_curr_n < theta_prev_s:
        theta_curr_n += 2 * np.pi

    theta_loop = np.linspace(theta_prev_s, theta_curr_n, 200)

    r_loop = r_pole - 0.25 * Bm * np.sin(
        np.pi * (theta_loop - theta_prev_s) / (theta_curr_n - theta_prev_s)
    )

    r_loop = np.maximum(r_loop, 0.2 * r_pole)

    ax3.plot(theta_loop, r_loop, linestyle=':', linewidth=1.5)

# ============================================================
# SETTINGS
# ============================================================
ax3.set_title(f"{pole}-Pole Complete Flux Loops (N → S)")
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
