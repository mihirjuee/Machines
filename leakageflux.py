# Leakage Flux Animation in Transformer (Streamlit)
# Visualizes:
# - Main mutual flux (links both windings)
# - Primary leakage flux
# - Secondary leakage flux
# - Animated AC excitation

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import time

st.set_page_config(page_title="Transformer Leakage Flux Animation", layout="centered")

st.title("⚡ Transformer Leakage Flux Animation")

# ===================== USER INPUTS =====================
freq = st.slider("Supply Frequency (Hz)", 1, 60, 50)
leakage_factor = st.slider("Leakage Flux Strength", 0.1, 1.0, 0.4, 0.1)
turns_ratio = st.slider("Turns Ratio N2/N1", 0.5, 2.0, 1.0, 0.1)

run_anim = st.button("▶ Start Animation")

# ===================== PLACEHOLDER =====================
plot_area = st.empty()

# ===================== ANIMATION =====================
if run_anim:

    for frame in range(120):

        t = frame / 20
        current = np.sin(2 * np.pi * freq * t / 50)

        # Flux values
        mutual_flux = current
        primary_leakage = leakage_factor * current
        secondary_leakage = leakage_factor * turns_ratio * current

        fig, ax = plt.subplots(figsize=(8, 6))

        # ================= CORE =================
        core = Rectangle((3.5, 1), 1, 4, fill=False, linewidth=3)
        ax.add_patch(core)

        # ================= PRIMARY COIL =================
        for i in range(5):
            ax.plot([2.5, 3.5], [1.5 + i * 0.6, 1.5 + i * 0.6], color='blue', linewidth=2)

        # ================= SECONDARY COIL =================
        for i in range(5):
            ax.plot([4.5, 5.5], [1.5 + i * 0.6, 1.5 + i * 0.6], color='green', linewidth=2)

        # ================= MUTUAL FLUX =================
        mutual_arrow = FancyArrowPatch(
            (4, 4.8), (4, 1.2),
            connectionstyle="arc3,rad=0.0",
            arrowstyle='->',
            mutation_scale=20 + abs(mutual_flux) * 20,
            linewidth=3,
            color='red'
        )
        ax.add_patch(mutual_arrow)

        # ================= PRIMARY LEAKAGE =================
        primary_arrow = FancyArrowPatch(
            (2.8, 4.5), (2.8, 1.5),
            connectionstyle="arc3,rad=0.4",
            arrowstyle='->',
            mutation_scale=15 + abs(primary_leakage) * 15,
            linewidth=2,
            color='orange'
        )
        ax.add_patch(primary_arrow)

        # ================= SECONDARY LEAKAGE =================
        secondary_arrow = FancyArrowPatch(
            (5.2, 1.5), (5.2, 4.5),
            connectionstyle="arc3,rad=0.4",
            arrowstyle='->',
            mutation_scale=15 + abs(secondary_leakage) * 15,
            linewidth=2,
            color='purple'
        )
        ax.add_patch(secondary_arrow)

        # ================= LABELS =================
        ax.text(2.2, 5.2, "Primary")
        ax.text(4.8, 5.2, "Secondary")
        ax.text(4.2, 3, "Main Flux", color='red')
        ax.text(1.8, 3, "Primary Leakage", color='orange')
        ax.text(5.6, 3, "Secondary Leakage", color='purple')

        # ================= CURRENT DISPLAY =================
        ax.text(0.5, 0.5, f"Instantaneous Current: {current:.2f}")
        ax.text(0.5, 0.2, f"Leakage Factor: {leakage_factor:.2f}")

        # ================= FORMAT =================
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 6)
        ax.axis("off")

        plot_area.pyplot(fig)

        plt.close(fig)

        time.sleep(0.05)

# ===================== THEORY =====================
st.write("---")
st.subheader("📘 Concept:")
st.info("""
🔴 Main Flux:
Links both primary and secondary winding and transfers energy.

🟠 Primary Leakage Flux:
Produced by primary current but links only primary winding.

🟣 Secondary Leakage Flux:
Produced by secondary current but links only secondary winding.

⚡ Higher leakage flux → Poorer voltage regulation.
""")
