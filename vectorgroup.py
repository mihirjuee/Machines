# ============================================================
# THREE-PHASE TRANSFORMER VECTOR GROUP ANALYZER (BASIC)
# Streamlit App
# Features:
# ✅ Select HV/LV winding type
# ✅ Neutral option
# ✅ Clock number (0–11)
# ✅ Auto vector group name
# ✅ Phasor diagram
# ✅ Phase shift calculation
# ✅ Parallel compatibility checker
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Transformer Vector Group Analyzer", layout="wide")

st.title("⚡ Three-Phase Transformer Vector Group Analyzer")

st.markdown("""
Learn transformer vector groups visually:
- HV/LV winding combinations
- Clock notation
- Phase displacement
- Parallel operation compatibility
""")

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("Transformer Configuration")

hv_type = st.sidebar.selectbox("HV Winding Type", ["D", "Y", "Z"])
lv_type = st.sidebar.selectbox("LV Winding Type", ["d", "y", "z"])

neutral = st.sidebar.checkbox("LV Neutral Available (n)", value=True)

clock = st.sidebar.slider("Clock Number", 0, 11, 11)

# ---------------- VECTOR GROUP NAME ----------------
vector_group = hv_type + lv_type
if neutral and lv_type in ["y", "z"]:
    vector_group += "n"

vector_group += str(clock)

# ---------------- PHASE SHIFT ----------------
phase_shift = clock * 30

# ---------------- DISPLAY INFO ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📘 Vector Group")
    st.write(f"### {vector_group}")

with col2:
    st.subheader("🕒 Phase Displacement")
    st.write(f"### {phase_shift}°")

# ---------------- PHASOR DIAGRAM ----------------
st.subheader("📈 Phasor Diagram")

fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection':'polar'})

# Primary phasors (HV reference)
angles_primary = np.radians([0, -120, 120])
labels_primary = ['R', 'Y', 'B']

# Secondary shifted phasors
angles_secondary = angles_primary - np.radians(phase_shift)
labels_secondary = ['r', 'y', 'b']

# Plot primary
for angle, label in zip(angles_primary, labels_primary):
    ax.arrow(angle, 0, 0, 1,
             width=0.015, head_width=0.08, head_length=0.1,
             length_includes_head=True)
    ax.text(angle, 1.15, label, fontsize=12)

# Plot secondary
for angle, label in zip(angles_secondary, labels_secondary):
    ax.arrow(angle, 0, 0, 0.8,
             width=0.01, head_width=0.06, head_length=0.08,
             length_includes_head=True)
    ax.text(angle, 0.92, label, fontsize=12)

ax.set_title(f"HV vs LV Phasor Shift ({vector_group})", pad=20)
ax.set_rticks([])
ax.grid(True)

st.pyplot(fig)

# ---------------- CLOCK DISPLAY ----------------
st.subheader("🕒 Clock Notation")
st.write(f"Clock Position = {clock} o'clock")
st.info("Each clock hour = 30° phase displacement")

# ---------------- PARALLEL CHECKER ----------------
st.subheader("🔗 Parallel Operation Checker")

vg2 = st.text_input("Enter another transformer vector group (e.g. Dyn11):")

if vg2:
    compatible = vg2.lower() == vector_group.lower()

    if compatible:
        st.success("✅ Compatible for parallel operation (basic vector group match)")
    else:
        st.error("❌ Not compatible — phase displacement mismatch may cause circulating currents")

# ---------------- THEORY ----------------
st.subheader("📖 Common Vector Groups")

st.markdown("""
- **Dyn11** → Distribution transformers  
- **Dyn1** → Specific industrial systems  
- **Yd1** → Industrial motor loads  
- **Dd0** → No phase shift  
- **Yy0** → Rare applications  
""")

# ---------------- EDUCATIONAL NOTES ----------------
st.subheader("🎯 Why Vector Groups Matter")

st.markdown("""
✅ Correct synchronization  
✅ Parallel operation  
✅ Harmonic suppression  
✅ Grounding method  
✅ Neutral availability  
""")

st.warning("Wrong vector group matching can lead to severe circulating current and transformer damage.")
