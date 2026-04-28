# Transformer Leakage Flux Animation
# Proper shell/core-type style magnetic core + realistic coil windings

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Arc
import time

st.set_page_config(page_title="Proper Transformer Core & Winding", layout="centered")

st.title("⚡ Transformer Leakage Flux Animation (Proper Core + Windings)")

# ================= USER INPUTS =================
freq = st.slider("Supply Frequency (Hz)", 1, 60, 50)
leakage_factor = st.slider("Leakage Flux Strength", 0.1, 1.0, 0.3, 0.1)
turns_ratio = st.slider("Turns Ratio N₂/N₁", 0.5, 2.0, 1.0, 0.1)

run_anim = st.button("▶ Start Animation")

plot_area = st.empty()

# ================= WINDING DRAW FUNCTION =================
def draw_winding(ax, x_center, y_bottom, turns=6, radius=0.22, spacing=0.38, color="blue"):
    """
    Draws vertical transformer winding loops around a limb.
    """
    for i in range(turns):
        y = y_bottom + i * spacing
        arc_left = Arc((x_center - radius, y), width=radius * 2, height=spacing * 0.9,
                       theta1=-90, theta2=90, linewidth=2.5, color=color)
        arc_right = Arc((x_center + radius, y), width=radius * 2, height=spacing * 0.9,
                        theta1=90, theta2=270, linewidth=2.5, color=color)

        ax.add_patch(arc_left)
        ax.add_patch(arc_right)

# ================= ANIMATION =================
if run_anim:

    for frame in range(140):

        t = frame / 25
        current = np.sin(2 * np.pi * freq * t / 50)

        # Flux values
        mutual_flux = current
        primary_leakage = leakage_factor * current
        secondary_leakage = leakage_factor * turns_ratio * current

        fig, ax = plt.subplots(figsize=(10, 7))

        # =====================================================
        # PROPER CORE (2-LIMB CORE TYPE)
        # =====================================================
        # Left limb
        ax.add_patch(Rectangle((2, 1), 0.7, 4, color="black"))

        # Right limb
        ax.add_patch(Rectangle((5.3, 1), 0.7, 4, color="black"))

        # Top yoke
        ax.add_patch(Rectangle((2, 4.3), 4, 0.7, color="black"))

        # Bottom yoke
        ax.add_patch(Rectangle((2, 1), 4, 0.7, color="black"))

        # Window opening
        ax.add_patch(Rectangle((2.7, 1.7), 2.6, 2.6, color="white"))

        # =====================================================
        # PRIMARY WINDING (LEFT LIMB)
        # =====================================================
        draw_winding(ax, x_center=1.7, y_bottom=1.8, turns=7, color="blue")

        # =====================================================
        # SECONDARY WINDING (RIGHT LIMB)
        # =====================================================
        draw_winding(ax, x_center=6.3, y_bottom=1.8, turns=7, color="green")

        # =====================================================
        # MAIN MUTUAL FLUX (inside core path)
        # =====================================================
        main_flux = FancyArrowPatch(
            (3.3, 4.6), (4.7, 4.6),
            connectionstyle="arc3,rad=0.35",
            arrowstyle='->',
            mutation_scale=20 + abs(mutual_flux) * 18,
            linewidth=3.5,
            color='red'
        )
        ax.add_patch(main_flux)

        # =====================================================
        # PRIMARY LEAKAGE FLUX
        # =====================================================
        primary_flux = FancyArrowPatch(
            (1.3, 4.4), (1.3, 1.6),
            connectionstyle="arc3,rad=0.55",
            arrowstyle='->',
            mutation_scale=14 + abs(primary_leakage) * 14,
            linewidth=2.5,
            color='orange'
        )
        ax.add_patch(primary_flux)

        # =====================================================
        # SECONDARY LEAKAGE FLUX
        # =====================================================
        secondary_flux = FancyArrowPatch(
            (6.7, 1.6), (6.7, 4.4),
            connectionstyle="arc3,rad=0.55",
            arrowstyle='->',
            mutation_scale=14 + abs(secondary_leakage) * 14,
            linewidth=2.5,
            color='purple'
        )
        ax.add_patch(secondary_flux)

        # =====================================================
        # LABELS
        # =====================================================
        ax.text(1.0, 5.4, "Primary Winding", fontsize=12, weight="bold", color="blue")
        ax.text(5.8, 5.4, "Secondary Winding", fontsize=12, weight="bold", color="green")

        ax.text(3.6, 5.25, "Main Flux", fontsize=11, color="red")
        ax.text(0.15, 3.1, "Primary Leakage", fontsize=10, color="orange", rotation=90)
        ax.text(7.25, 3.1, "Secondary Leakage", fontsize=10, color="purple", rotation=90)

        # Live current
        ax.text(0.3, 0.55, f"Instantaneous Magnetizing Current = {current:.2f}", fontsize=11)
        ax.text(0.3, 0.25, f"Leakage Factor = {leakage_factor:.2f}", fontsize=11)

        # =====================================================
        # DISPLAY SETTINGS
        # =====================================================
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 6)
        ax.axis("off")

        plot_area.pyplot(fig)
        plt.close(fig)

        time.sleep(0.05)

# ================= THEORY =================
st.write("---")
st.subheader("📘 Proper Transformer Structure")
st.info("""
🟦 Primary winding creates magnetizing current.

🟥 Main flux travels through the closed iron core path (limbs + yokes).

🟧 Primary leakage flux links only primary winding.

🟪 Secondary leakage flux links only secondary winding.

⚡ Proper winding placement around core limbs improves coupling and reduces leakage reactance.
""")
