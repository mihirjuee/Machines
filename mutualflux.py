import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ============================================================
# ⚡ Learn EE: Wireless Power Transfer via Mutual Induction
# Features:
# ✅ Distance-based coupling
# ✅ Resonance frequency effect
# ✅ Coil misalignment effect
# ✅ Real-world modes
# ✅ 3D Coil + Magnetic Flux Visualization
# ✅ Voltage + Efficiency Metrics
# ✅ Waveform Comparison
# ============================================================

# --- Page Config ---
st.set_page_config(page_title="Learn EE: Wireless Power Transfer", layout="wide")

# --- Title ---
st.title("⚡ Wireless Power Transfer: Mutual Induction")
st.markdown("### Learn how electrical energy transfers wirelessly using magnetic fields")

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
st.sidebar.header("🔧 Control Parameters")

mode = st.sidebar.selectbox(
    "Application Mode",
    ["Wireless Charger", "EV Charging", "Transformer Core"]
)

# Mode Presets
if mode == "Wireless Charger":
    source_voltage = 12
    resonant_freq = 50
elif mode == "EV Charging":
    source_voltage = 400
    resonant_freq = 85
else:  # Transformer Core
    source_voltage = 230
    resonant_freq = 50

frequency = st.sidebar.slider("AC Frequency (Hz)", 10, 150, resonant_freq)
distance = st.sidebar.slider("Distance between Coils (cm)", 1, 20, 5)
turns_ratio = st.sidebar.slider("Secondary Turns Ratio", 0.5, 2.0, 1.0)
misalignment = st.sidebar.slider("Coil Misalignment (%)", 0, 100, 0)

# ============================================================
# PHYSICS MODEL
# ============================================================

# Coupling coefficient decreases with distance
coupling_coeff = 1 / (1 + (distance / 5) ** 2)

# Resonance effect
resonance_factor = 1 / (1 + abs(frequency - resonant_freq) / 20)

# Misalignment effect
alignment_factor = 1 - misalignment / 100

# Final induced voltage
induced_voltage = source_voltage * turns_ratio * coupling_coeff * resonance_factor * alignment_factor

# Efficiency
power_efficiency = coupling_coeff * resonance_factor * alignment_factor * 100

# ============================================================
# WAVEFORMS
# ============================================================
t = np.linspace(0, 0.1, 1000)

primary_wave = source_voltage * np.sin(2 * np.pi * frequency * t)
secondary_wave = induced_voltage * np.sin(2 * np.pi * frequency * t)

# ============================================================
# 3D COIL VISUALIZATION
# ============================================================
theta = np.linspace(0, 2 * np.pi, 100)

# Coil Coordinates
x_primary = np.cos(theta)
y_primary = np.sin(theta)
z_primary = np.full_like(theta, -2)

x_secondary = np.cos(theta)
y_secondary = np.sin(theta)
z_secondary = np.full_like(theta, distance / 2)

# Magnetic Flux Cylinder
z = np.linspace(-2, distance / 2, 30)
theta_grid, z_grid = np.meshgrid(theta, z)

flux_strength = 1 + 0.3 * np.sin(2 * np.pi * frequency * t[0])

x_field = flux_strength * coupling_coeff * np.cos(theta_grid)
y_field = flux_strength * coupling_coeff * np.sin(theta_grid)

# ============================================================
# PLOTLY FIGURE
# ============================================================
fig = go.Figure()

# Primary Coil
fig.add_trace(
    go.Scatter3d(
        x=x_primary,
        y=y_primary,
        z=z_primary,
        mode="lines",
        line=dict(color="red", width=10),
        name="Primary Coil"
    )
)

# Secondary Coil
fig.add_trace(
    go.Scatter3d(
        x=x_secondary,
        y=y_secondary,
        z=z_secondary,
        mode="lines",
        line=dict(color="blue", width=10),
        name="Secondary Coil"
    )
)

# Magnetic Flux
if coupling_coeff > 0.05:
    fig.add_trace(
        go.Mesh3d(
            x=x_field.flatten(),
            y=y_field.flatten(),
            z=z_grid.flatten(),
            opacity=0.15,
            color="cyan",
            name="Magnetic Flux"
        )
    )

fig.update_layout(
    scene=dict(
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=600
)

# ============================================================
# LAYOUT
# ============================================================
col1, col2 = st.columns([1.2, 1])

# ---------------- LEFT SIDE ----------------
with col1:
    st.subheader("🌀 Coil Coupling Visualization")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- RIGHT SIDE ----------------
with col2:
    st.subheader("📊 System Performance")

    st.metric("Source Voltage", f"{source_voltage:.1f} V")
    st.metric("Induced Voltage", f"{induced_voltage:.2f} V")
    st.metric("Coupling Efficiency", f"{coupling_coeff * 100:.1f}%")
    st.metric("Overall Transfer Efficiency", f"{power_efficiency:.1f}%")

    st.progress(min(int(power_efficiency), 100))

    # LED Status
    st.subheader("💡 Receiver Status")
    if induced_voltage > source_voltage * 0.7:
        st.success("🌟 FULL POWER! Device charging efficiently.")
    elif induced_voltage > source_voltage * 0.3:
        st.warning("⚡ Partial Charging... Adjust alignment or distance.")
    else:
        st.error("❌ Too Far / Misaligned — No Effective Charging")

# ============================================================
# WAVEFORM SECTION
# ============================================================
st.subheader("📈 Primary vs Secondary Voltage Waveforms")

waveform_data = {
    "Primary Voltage (V)": primary_wave,
    "Secondary Voltage (V)": secondary_wave
}

st.line_chart(waveform_data)

# ============================================================
# EDUCATIONAL SECTION
# ============================================================
st.markdown("---")
st.subheader("📘 Core Concept")

st.latex(r"E = -N \frac{d\Phi}{dt}")

st.info("""
**Faraday’s Law:** A changing magnetic flux through the secondary coil induces voltage.

### Key Factors:
- **Distance ↑** → Magnetic coupling ↓
- **Frequency mismatch ↑** → Resonance ↓
- **Misalignment ↑** → Energy transfer ↓

### Real Applications:
- 📱 Wireless Phone Chargers  
- 🚗 EV Wireless Charging  
- 🔌 Transformers  
""")

# ============================================================
# BONUS INSIGHT
# ============================================================
if mode == "Wireless Charger":
    st.success("📱 Wireless charging works best when your phone is centered on the pad.")
elif mode == "EV Charging":
    st.success("🚗 EV wireless systems require precise alignment and resonant tuning.")
else:
    st.success("🔌 Transformer cores minimize air-gap to maximize magnetic coupling.")
