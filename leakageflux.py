# Textbook-Style Transformer Diagram with Leakage Flux Animation
# Core-type transformer: proper laminated core, concentric windings, mutual + leakage flux

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc
import time

st.set_page_config(page_title="Textbook Transformer Leakage Flux", layout="centered")

st.title("📘 Transformer Leakage Flux (Textbook Style)")

# ================= CONTROLS =================
freq = st.slider("Supply Frequency (Hz)", 1, 60, 50)
leakage_factor = st.slider("Leakage Flux", 0.1, 1.0, 0.3, 0.1)
run_anim = st.button("▶ Start Animation")

plot_area = st.empty()

# ================= COIL DRAW FUNCTION =================
def draw_vertical_coil(ax, x, y_start, turns, spacing, radius, color):
    """
    Draw textbook-style transformer winding as stacked circular turns.
    """
    for i in range(turns):
        y = y_start + i * spacing
        c = Circle((x, y), radius=radius, fill=False, linewidth=2.2, color=color)
        ax.add_patch(c)

# ================= ANIMATION =================
if run_anim:

    for frame in range(150):

        t = frame / 25
        i_m = np.sin(2 * np.pi * freq * t / 50)

        mutual_flux = i_m
        primary_leakage = leakage_factor * i_m
        secondary_leakage = leakage_factor * i_m

        fig, ax = plt.subplots(figsize=(10, 7))

        # =====================================================
        # TEXTBOOK CORE-TYPE TRANSFORMER
        # =====================================================

        # Left limb
        ax.add_patch(Rectangle((3.0, 1.0), 0.45, 4.0, fill=False, linewidth=3))

        # Right limb
        ax.add_patch(Rectangle((5.55, 1.0), 0.45, 4.0, fill=False, linewidth=3))

        # Top yoke
        ax.add_patch(Rectangle((3.0, 5.0), 3.0, 0.45, fill=False, linewidth=3))

        # Bottom yoke
        ax.add_patch(Rectangle((3.0, 0.55), 3.0, 0.45, fill=False, linewidth=3))

        # =====================================================
        # PRIMARY WINDING (left side, around left limb)
        # =====================================================
        draw_vertical_coil(
            ax=ax,
            x=2.4,
            y_start=1.4,
            turns=7,
            spacing=0.48,
            radius=0.18,
            color="blue"
        )

        # =====================================================
        # SECONDARY WINDING (right side, around right limb)
        # =====================================================
        draw_vertical_coil(
            ax=ax,
            x=6.6,
            y_start=1.4,
            turns=7,
            spacing=0.48,
            radius=0.18,
            color="green"
        )

        # =====================================================
        # SUPPLY TERMINALS
        # =====================================================
        ax.plot([1.8, 2.2], [4.4, 4.4], color="black", linewidth=1.5)
        ax.plot([1.8, 2.2], [1.6, 1.6], color="black", linewidth=1.5)

        # =====================================================
        # LOAD TERMINALS
        # =====================================================
        ax.plot([6.8, 7.4], [4.4, 4.4], color="black", linewidth=1.5)
        ax.plot([6.8, 7.4], [1.6, 1.6], color="black", linewidth=1.5)

        # =====================================================
        # MAIN FLUX (inside core)
        # =====================================================
        main_flux = FancyArrowPatch(
            (4.2, 4.75), (4.9, 4.75),
            connectionstyle="arc3,rad=0.35",
            arrowstyle='->',
            mutation_scale=18 + abs(mutual_flux) * 18,
            linewidth=3,
            color='red'
        )
        ax.add_patch(main_flux)

        # =====================================================
        # PRIMARY LEAKAGE FLUX
        # =====================================================
        p_flux = FancyArrowPatch(
            (2.0, 4.6), (2.0, 1.4),
            connectionstyle="arc3,rad=0.55",
            arrowstyle='->',
            mutation_scale=14 + abs(primary_leakage) * 14,
            linewidth=2.5,
            color='orange'
        )
        ax.add_patch(p_flux)

        # =====================================================
        # SECONDARY LEAKAGE FLUX
        # =====================================================
        s_flux = FancyArrowPatch(
            (7.0, 1.4), (7.0, 4.6),
            connectionstyle="arc3,rad=0.55",
            arrowstyle='->',
            mutation_scale=14 + abs(secondary_leakage) * 14,
            linewidth=2.5,
            color='purple'
        )
        ax.add_patch(s_flux)

        # =====================================================
        # LABELS
        # =====================================================
        ax.text(1.5, 5.55, "Primary", fontsize=12, weight="bold", color="blue")
        ax.text(6.2, 5.55, "Secondary", fontsize=12, weight="bold", color="green")

        ax.text(4.35, 5.3, "Φm", fontsize=14, color="red", weight="bold")
        ax.text(1.55, 3.0, "Φlp", fontsize=12, color="orange", rotation=90)
        ax.text(7.2, 3.0, "Φls", fontsize=12, color="purple", rotation=90)

        ax.text(0.7, 0.45, f"Magnetizing Current = {i_m:.2f}", fontsize=11)

        # =====================================================
        # STYLE
        # =====================================================
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 6)
        ax.axis("off")

        plot_area.pyplot(fig)
        plt.close(fig)

        time.sleep(0.05)

# ================= THEORY =================
st.write("---")
st.subheader("📘 Textbook Insight")
st.info("""
Φm  → Mutual (main) flux linking both windings through the iron core  
Φlp → Primary leakage flux linking only primary winding  
Φls → Secondary leakage flux linking only secondary winding  

⚡ In practical transformers, leakage flux causes leakage reactance and voltage drop.
""")
