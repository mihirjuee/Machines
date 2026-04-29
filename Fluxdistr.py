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
st.set_page_config(page_title="Correct Air-Gap Flux Waveform", page_icon="logo.png", layout="wide")

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
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Key Equation")

st.markdown(f"""
### Resultant Air-Gap Flux:
**B(θ,t) = 1.5 Bm cos(pθ − ωt)**

Where:

**Bm = {Bm:.2f}**  
**p = P/2 = {p}**

---

## Clarification:
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
