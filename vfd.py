import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Learn EE Interactive - IM Simulator", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .variac-panel { 
        background-color: #2c3e50; padding: 20px; border-radius: 15px; 
        text-align: center; color: white; border: 5px solid #bdc3c7;
    }
    </style>
""", unsafe_allow_html=True)

# --- Physics Engine: Induction Motor Model ---
def calculate_motor_performance(V_line, f, slip, R1, X1, R2, X2, Xm, Rc):
    if V_line == 0 or slip == 0:
        return 0, 0, 0, 0, 0
    
    V_ph = V_line / np.sqrt(3)
    omega_s = 2 * np.pi * f * (2 / 4) # Assuming 4-pole motor
    
    # Equivalent Circuit Impedance
    Z_rotor = (R2 / slip) + 1j * X2
    Z_mag = (Rc * 1j * Xm) / (Rc + 1j * Xm)
    Z_parallel = (Z_rotor * Z_mag) / (Z_rotor + Z_mag)
    Z_total = (R1 + 1j * X1) + Z_parallel
    
    # Currents
    I1 = V_ph / abs(Z_total)
    E1 = V_ph - I1 * abs(R1 + 1j * X1)
    I2 = abs(E1 / Z_rotor)
    
    # Torque and Power
    torque = (3 * (I2**2) * (R2 / slip)) / omega_s
    power_out = torque * omega_s * (1 - slip)
    power_in = 3 * V_ph * I1 * np.cos(np.angle(Z_total))
    eff = (power_out / power_in) * 100 if power_in > 0 else 0
    
    return I1, torque, power_out, eff, power_in

# --- Sidebar: Machine Parameters ---
with st.sidebar:
    st.header("🛠️ Machine Nameplate")
    v_rated = st.number_input("Rated Voltage (V)", value=415)
    f_rated = st.number_input("Rated Frequency (Hz)", value=50)
    
    st.divider()
    st.subheader("Equivalent Circuit Params")
    r1 = st.slider("Stator Res (R1)", 0.1, 5.0, 1.2)
    r2 = st.slider("Rotor Res (R2')", 0.1, 5.0, 0.8)
    xm = st.slider("Mag Reactance (Xm)", 10, 300, 150)
    
    st.divider()
    st.subheader("Live Controls")
    v_supply = st.slider("Variac Output (V)", 0, 480, 415)
    slip_input = st.slider("Operating Slip (s)", 0.001, 0.1, 0.03, format="%.3f")

# --- App Layout ---
st.title("⚡ Interactive Three-Phase Induction Motor Lab")
st.markdown("Analyze motor performance under varying supply and load conditions.")

# Row 1: The Variac and The Meters
col_var, col_met = st.columns([1, 2])

with col_var:
    st.markdown('<div class="variac-panel">', unsafe_allow_html=True)
    rot = (v_supply / 480) * 270
    st.markdown(f"""
        <svg width="150" height="150" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="#34495e" />
            <g transform="rotate({rot} 50 50)">
                <circle cx="50" cy="50" r="25" fill="#ecf0f1" />
                <line x1="50" y1="50" x2="50" y2="28" stroke="#e74c3c" stroke-width="4" stroke-linecap="round"/>
            </g>
        </svg>
        <h2 style="color: #e74c3c;">{v_supply}V</h2>
        <p>3Ф VARIAC</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Calculation
I1, T, P_out, Eff, P_in = calculate_motor_performance(v_supply, f_rated, slip_input, r1, 1.5, r2, 1.2, xm, 1200)

with col_met:
    m1, m2, m3 = st.columns(3)
    m1.metric("Stator Current (A)", f"{I1:.2f}")
    m2.metric("Output Torque (Nm)", f"{T:.2f}")
    m3.metric("Efficiency (%)", f"{Eff:.1f}")
    
    m4, m5, m6 = st.columns(3)
    m4.metric("Output Power (W)", f"{P_out:.1f}")
    m5.metric("Input Power (W)", f"{P_in:.1f}")
    m6.metric("Synchronous Speed", "1500 RPM")

st.divider()

# Row 2: Performance Curves
st.subheader("📈 Torque-Slip Characteristics")
slips = np.linspace(0.001, 1.0, 100)
torques = [calculate_motor_performance(v_supply, f_rated, s, r1, 1.5, r2, 1.2, xm, 1200)[1] for s in slips]

fig = go.Figure()
fig.add_trace(go.Scatter(x=slips, y=torques, mode='lines', name='Torque', line=dict(color='firebrick', width=3)))
fig.add_vline(x=slip_input, line_dash="dash", line_color="green", annotation_text="Operating Point")
fig.update_layout(xaxis_title="Slip (s)", yaxis_title="Torque (Nm)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Row 3: Connection Status
st.divider()
st.subheader("🔌 Connection Schematic (Star Connected)")


st.info("The simulation uses the exact equivalent circuit model. Increasing R2 will shift the maximum torque toward higher slip values.")
