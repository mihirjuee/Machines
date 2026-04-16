import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="Learn EE - No Load Test Simulator", layout="wide")

def create_gauge(value, min_val, max_val, label, unit, color):
    """Creates a realistic analog-style gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"<b>{label}</b><br><span style='font-size:0.8em;color:gray'>{unit}</span>"},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_val*0.8], 'color': '#f0f0f0'},
                {'range': [max_val*0.8, max_val], 'color': '#ffcccc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=30, r=30, t=50, b=20))
    return fig

# --- App Header ---
st.title("⚡ 3-Phase Induction Motor: No-Load Test")
st.markdown("""
Connect the Voltmeter, Ammeter, and Two Wattmeters to observe the motor characteristics 
as you vary the input voltage via the Variac.
""")

# --- Sidebar Inputs (Simulation Parameters) ---
st.sidebar.header("Machine Parameters")
v_rated = st.sidebar.number_input("Rated Line Voltage (V)", value=415)
i_rated = st.sidebar.number_input("Rated Current (A)", value=10.0)
f = st.sidebar.slider("Frequency (Hz)", 45, 55, 50)

st.sidebar.markdown("---")
st.sidebar.header("Control Panel")
v_input = st.sidebar.slider("Variac Output (Line Voltage)", 0, 480, 415)

# --- Mathematical Model (No-Load Logic) ---
# Realistic constants for a small motor
R_core = 1200  # Ohms (Representing core loss)
X_m = 150      # Ohms (Representing magnetizing reactance)
R1 = 0.5       # Stator resistance

# Per-phase calculations
v_phase = v_input / np.sqrt(3)
if v_phase > 0:
    i_core = v_phase / R_core
    i_mag = v_phase / X_m
    i_no_load_phase = np.sqrt(i_core**2 + i_mag**2)
    
    # Power calculations (Two-Wattmeter Method)
    p_total = 3 * (i_core**2) * R_core # Total No-load loss (Core + Friction)
    pf_angle = np.arccos(i_core / i_no_load_phase) # Radian
    
    # W1 = V_line * I_line * cos(30 + phi)
    # W2 = V_line * I_line * cos(30 - phi)
    w1 = v_input * i_no_load_phase * np.cos(np.radians(30) + pf_angle)
    w2 = v_input * i_no_load_phase * np.cos(np.radians(30) - pf_angle)
else:
    i_no_load_phase = 0
    w1 = 0
    w2 = 0
    p_total = 0

# --- UI Layout ---
st.subheader("Laboratory Instrument Panel")
m1, m2, m3 = st.columns(3)

with m1:
    st.plotly_chart(create_gauge(v_input, 0, 500, "Voltmeter", "Volts (V)", "blue"), use_container_width=True)

with m2:
    st.plotly_chart(create_gauge(i_no_load_phase, 0, i_rated, "Ammeter", "Amps (A)", "red"), use_container_width=True)

with m3:
    st.plotly_chart(create_gauge(p_total, 0, 2000, "Total Power", "Watts (W)", "green"), use_container_width=True)

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.info("### Wattmeter Readings")
    st.write(f"**Wattmeter 1 ($W_1$):** {w1:.2f} W")
    st.write(f"**Wattmeter 2 ($W_2$):** {w2:.2f} W")
    st.write(f"**Total No-Load Loss ($P_o$):** {w1 + w2:.2f} W")

with col_b:
    st.success("### Connection Diagram Status")
    st.write("✅ Variac connected to 3-Phase Supply")
    st.write("✅ Ammeter in Line R")
    st.write("✅ Wattmeter PC across R-Y and B-Y")
    # Placeholder for your diagram
    st.caption("Ensure the Two-Wattmeter method is followed for accurate $P_o$ results.")

# --- Results Table ---
st.subheader("Test Data Log")
data = {
    "Voltage (V)": [v_input],
    "Current (A)": [round(i_no_load_phase, 3)],
    "Power (W)": [round(p_total, 2)],
    "Power Factor": [round(p_total / (np.sqrt(3) * v_input * i_no_load_phase), 3) if v_input > 0 else 0]
}
st.table(data)
