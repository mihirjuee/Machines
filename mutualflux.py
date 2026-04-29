import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Learn EE: Wireless Power", layout="wide")
st.title("⚡ Wireless Power Transfer: Mutual Induction")
st.markdown("### How energy 'jumps' through thin air")

# --- Sidebar Controls ---
st.sidebar.header("Control Parameters")
frequency = st.sidebar.slider("AC Frequency (Hz)", 10, 100, 50)
distance = st.sidebar.slider("Distance between Coils (cm)", 1, 20, 5)
turns_ratio = st.sidebar.slider("Secondary Turns Ratio", 0.5, 2.0, 1.0)

# --- Physics Logic ---
# Simplified Mutual Inductance M ∝ 1 / (distance^2)
coupling_coeff = 1 / (1 + (distance/5)**2)
induced_voltage = 230 * turns_ratio * coupling_coeff

# --- Visualization ---
t = np.linspace(0, 0.1, 500)
primary_wave = 230 * np.sin(2 * np.pi * frequency * t)
secondary_wave = induced_voltage * np.sin(2 * np.pi * frequency * t)

# --- 3D Magnetic Field Plot ---
z = np.linspace(-10, 10, 20)
theta = np.linspace(0, 2*np.pi, 20)
theta_grid, z_grid = np.meshgrid(theta, z)
x_field = (1 + coupling_coeff) * np.cos(theta_grid)
y_field = (1 + coupling_coeff) * np.sin(theta_grid)

fig = go.Figure()

# Primary Coil Visual
fig.add_trace(go.Scatter3d(x=np.cos(theta), y=np.sin(theta), z=[-2]*20, 
                           mode='lines', line=dict(color='red', width=8), name="Primary Coil"))

# Secondary Coil Visual (Moves with Slider)
fig.add_trace(go.Scatter3d(x=np.cos(theta), y=np.sin(theta), z=[distance/2]*20, 
                           mode='lines', line=dict(color='blue', width=8), name="Secondary Coil"))

# Glowing Flux Lines (Concept)
if coupling_coeff > 0.2:
    fig.add_trace(go.Mesh3d(x=x_field.flatten(), y=y_field.flatten(), z=z_grid.flatten(), 
                            opacity=0.1, color='cyan', name="Magnetic Flux"))

fig.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                  margin=dict(l=0, r=0, b=0, t=0))

# --- Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write(f"**Coupling Efficiency:** {coupling_coeff*100:.1f}%")
    st.write(f"**Induced Voltage:** {induced_voltage:.2f} V")
    
    # LED Indicator
    if induced_voltage > 50:
        st.success("🌟 LED IS GLOWING BRIGHTLY!")
    elif induced_voltage > 10:
        st.warning("Dim Glow...")
    else:
        st.error("Too far! LED is OFF.")

    # Waveform Comparison
    st.line_chart({"Primary (V)": primary_wave, "Secondary (V)": secondary_wave})

st.info("💡 **Concept:** As you decrease the distance, the Magnetic Flux linkage increases, inducing a higher voltage in the secondary coil via Faraday's Law.")
