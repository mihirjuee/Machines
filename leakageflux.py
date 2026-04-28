# Proper Transformer Leakage Flux Animation with Realistic Closed Magnetic Core
# Streamlit App

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import time

st.set_page_config(page_title="Transformer Leakage Flux Animation", layout="centered")

st.title("⚡ Transformer Leakage Flux Animation (Proper Core Design)")

# ================= USER INPUTS =================
freq = st.slider("Supply Frequency (Hz)", 1, 60, 50)
leakage_factor = st.slider("Leakage Flux Strength", 0.1, 1.0, 0.3, 0.1)
turns_ratio = st.slider("Turns Ratio N₂/N₁", 0.5, 2.0, 1.0, 0.1)

run_anim = st.button("▶ Start Animation")

plot_area = st.empty()

# ================= ANIMATION =================
if run_anim:

    for frame in range(150):

        t = frame / 25
        current = np.sin(2 * np.pi * freq * t / 50)

        # Flux calculations
        mutual_flux = current
        primary_leakage = leakage_factor * current
        secondary_leakage = leakage_factor * turns_ratio * current

        fig, ax = plt.subplots(figsize=(9, 7))

        # =====================================================
        # CLOSED RECTANGULAR TRANSFORMER CORE (Proper Magnetic Path)
        # =====================================================
        # Outer core
        outer_core = Rectangle((2, 1), 4, 4, fill=False, linewidth=6, edgecolor='black')

        # Inner window
        inner_core = Rectangle((3, 2), 2, 2, fill=False, linewidth=6, edgecolor='white')

        ax.add_patch(outer_core)
        ax.add_patch(inner_core)

        # =====================================================
        # PRIMARY WINDING (LEFT LIMB)
        # =====================================================
        for i in range(6):
            y = 1.4 + i * 0.5
            ax.plot([1.3, 2], [y, y], color='blue', linewidth=3)

        # =====================================================
        # SECONDARY WINDING (RIGHT LIMB)
        # =====================================================
        for i in range(6):
            y = 1.4 + i * 0.5
            ax.plot([6, 6.7], [y, y], color='green', linewidth=3)

        # =====================================================
        # MAIN FLUX (Through Core)
        # =====================================================
        main_flux = FancyArrowPatch(
            (4, 4.6), (4, 1.4),
            connectionstyle="arc3,rad=0",
            arrowstyle='->',
            mutation_scale=20 + abs(mutual_flux) * 20,
            linewidth=4,
            color='red'
        )
        ax.add_patch(main_flux)

        # =====================================================
        # PRIMARY LEAKAGE FLUX (Outside Primary Only)
        # =====================================================
        primary_flux = FancyArrowPatch(
            (1.6, 4.2), (1.6, 1.8),
            connectionstyle="arc3,rad=0.5",
            arrowstyle='->',
            mutation_scale=15 + abs(primary_leakage) * 15,
            linewidth=3,
            color='orange'
        )
        ax.add_patch(primary_flux)

        # =====================================================
        # SECONDARY LEAKAGE FLUX (Outside Secondary Only)
        # =====================================================
        secondary_flux = FancyArrowPatch(
            (6.4, 1.8), (6.4, 4.2),
            connectionstyle="arc3,rad=0.5",
            arrowstyle='->',
            mutation_scale=15 + abs(secondary_leakage) * 15,
            linewidth=3,
            color='purple'
        )
        ax.add_patch(secondary_flux)

        # =====================================================
        # LABELS
        # =====================================================
        ax.text(0.9, 5.3, "Primary", fontsize=12, weight='bold', color='blue')
        ax.text(6.1, 5.3, "Secondary", fontsize=12, weight='bold', color='green')

        ax.text(4.2, 3, "Main Flux", color='red', fontsize=11)
        ax.text(0.4, 3, "Primary Leakage", color='orange', fontsize=10)
        ax.text(6.9, 3, "Secondary Leakage", color='purple', fontsize=10)

        # =====================================================
        # LIVE VALUES
        # =====================================================
        ax.text(0.3, 0.6, f"Instantaneous Current = {current:.2f}", fontsize=11)
        ax.text(0.3, 0.3, f"Leakage Factor = {leakage_factor:.2f}", fontsize=11)

        # =====================================================
        # AXIS SETTINGS
        # =====================================================
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 6)
        ax.axis("off")

        plot_area.pyplot(fig)

        plt.close(fig)

        time.sleep(0.05)

# ================= THEORY =================
st.write("---")
st.subheader("📘 Transformer Core Insight")
st.info("""
🟥 Main Flux:
Flows through the closed iron core and links both windings.

🟧 Primary Leakage Flux:
Only links primary winding, does not transfer useful energy.

🟪 Secondary Leakage Flux:
Only links secondary winding.

⚡ Proper closed core ensures efficient magnetic coupling and reduces leakage.
""")
