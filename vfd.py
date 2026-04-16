import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Learn EE - No Load Test Simulator", layout="wide")

# --- GAUGE FUNCTION ---
def create_gauge(value, min_val, max_val, label, unit, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"<b>{label}</b><br><span style='font-size:0.8em;color:gray'>{unit}</span>"},
        gauge={
            'axis': {'range': [min_val, max_val]},
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
                'value': value
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- HEADER ---
st.title("⚡ 3-Phase Induction Motor: No-Load Test Virtual Lab")

st.markdown("""
Adjust the **Variac voltage** and observe real-time readings of:
- Voltmeter
- Ammeter
- Wattmeters (Two-Wattmeter Method)
""")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Machine Parameters")
v_rated = st.sidebar.number_input("Rated Voltage (V)", value=415)
i_rated = st.sidebar.number_input("Rated Current (A)", value=10.0)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")
v_input = st.sidebar.slider("Variac Output Voltage (V)", 0, 480, 415)

# --- MACHINE CONSTANTS ---
R_core = 1200   # Core loss resistance
X_m = 150       # Magnetizing reactance
R1 = 0.5        # Stator resistance

# --- CALCULATIONS ---
v_phase = v_input / np.sqrt(3)

if v_phase > 0:
    i_core = v_phase / R_core
    i_mag = v_phase / X_m
    i_no_load = np.sqrt(i_core**2 + i_mag**2)

    # Power factor angle
    pf = i_core / i_no_load
    pf = min(pf, 1)
    phi = np.arccos(pf)

    # Two-wattmeter readings
    w1 = v_input * i_no_load * np.cos(np.radians(30) + phi)
    w2 = v_input * i_no_load * np.cos(np.radians(30) - phi)

    # Total power (realistic)
    p_total = w1 + w2

else:
    i_no_load = 0
    w1 = 0
    w2 = 0
    p_total = 0
    pf = 0

# --- GAUGE LIMITS ---
max_current = max(i_rated, i_no_load * 1.2)
max_power = max(2000, p_total * 1.2)

# --- DISPLAY METERS ---
st.subheader("🧪 Laboratory Instrument Panel")

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(create_gauge(v_input, 0, 500, "Voltmeter", "Volts", "blue"), use_container_width=True)

with col2:
    st.plotly_chart(create_gauge(i_no_load, 0, max_current, "Ammeter", "Amps", "red"), use_container_width=True)

with col3:
    st.plotly_chart(create_gauge(p_total, 0, max_power, "Wattmeter", "Watts", "green"), use_container_width=True)

# --- WATTMETER READINGS ---
st.markdown("---")
col4, col5 = st.columns(2)

with col4:
    st.info("### 🔌 Wattmeter Readings")
    st.write(f"**W₁:** {w1:.2f} W")
    st.write(f"**W₂:** {w2:.2f} W")
    st.write(f"**Total Power (P₀):** {p_total:.2f} W")

with col5:
    st.success("### 📊 Calculated Parameters")
    st.metric("Power Factor", f"{pf:.3f}")
    st.metric("No-load Current", f"{i_no_load:.2f} A")

# --- WARNING ---
if pf < 0.2 and v_input > 0:
    st.warning("⚠️ Very low power factor — typical for no-load condition")

# --- CONNECTION DIAGRAM ---
st.markdown("---")
st.subheader("🔌 Connection Diagram (Conceptual)")

st.markdown("""
