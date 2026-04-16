import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config & Styling ---
st.set_page_config(page_title="Learn EE Interactive Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- Gauge Component Function ---
def draw_analog_meter(value, min_v, max_v, title, unit, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'font': {'size': 20, 'color': "black"}, 'suffix': f" {unit}"},
        title={'text': title, 'font': {'size': 18}},
        gauge={
            'axis': {'range': [min_v, max_v], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, max_v * 0.7], 'color': "#e8f5e9"},
                {'range': [max_v * 0.7, max_v * 0.9], 'color': "#fff3e0"},
                {'range': [max_v * 0.9, max_v], 'color': "#ffebee"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=280, margin=dict(l=30, r=30, t=40, b=20))
    return fig

# --- App Header ---
st.title("🔬 Virtual Machines Lab: No-Load Test")
st.write("Perform the no-load test on a 3-phase Induction Motor to determine rotational losses.")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("🔌 Control Bench")
    v_line = st.slider("Variac Output (Line Voltage V₀)", 0, 440, 415, step=5)
    
    st.divider()
    st.subheader("Machine Nameplate")
    p_rated = st.number_input("Rated Power (kW)", value=5.5)
    f_supply = st.number_input("Frequency (Hz)", value=50)
    st.info("Note: No-load current is typically 30-40% of rated current.")

# --- Physics Engine (No-Load Calculation) ---
# Parameters for a typical 7.5HP / 5.5kW Motor
R1 = 0.8        # Stator resistance per phase
Xm = 110        # Magnetizing reactance
Rc = 950        # Core loss resistance (representing iron losses)
friction_loss = 150 # Watts (Mechanical loss)

if v_line > 0:
    v_phase = v_line / np.sqrt(3)
    
    # Current components
    i_core = v_phase / Rc
    i_mag = v_phase / Xm
    i_no_load = np.sqrt(i_core**2 + i_mag**2) # Line current (No-load)
    
    # Power calculations
    p_core = 3 * (i_core**2) * Rc
    p_cu_nl = 3 * (i_no_load**2) * R1
    p_total = p_core + friction_loss + p_cu_nl
    
    # Phase angle for Two-Wattmeter logic
    pf_no_load = p_total / (np.sqrt(3) * v_line * i_no_load)
    phi = np.arccos(pf_no_load)
    
    # Two Wattmeter Readings
    # W1 = Vl*Il*cos(30 + phi), W2 = Vl*Il*cos(30 - phi)
    w1 = v_line * i_no_load * np.cos(np.radians(30) + phi)
    w2 = v_line * i_no_load * np.cos(np.radians(30) - phi)
else:
    i_no_load = w1 = w2 = p_total = pf_no_load = 0

# --- Dashboard Layout ---
tab1, tab2 = st.tabs(["📊 Meter Panel", "🔌 Connection Diagram"])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(draw_analog_meter(v_line, 0, 500, "Voltmeter (V₀)", "V", "#2196F3"), use_container_width=True)
    
    with col2:
        st.plotly_chart(draw_analog_meter(i_no_load, 0, 15, "Ammeter (I₀)", "A", "#F44336"), use_container_width=True)
        
    with col3:
        # Combined Wattmeter Reading
        st.plotly_chart(draw_analog_meter(w1 + w2, 0, 2000, "Total Power (W₀)", "W", "#4CAF50"), use_container_width=True)

    st.divider()
    
    # Detailed Wattmeter Readings (Crucial for Lab reports)
    c1, c2, c3 = st.columns(3)
    c1.metric("Wattmeter 1 (W₁)", f"{w1:.2f} W")
    c2.metric("Wattmeter 2 (W₂)", f"{w2:.2f} W")
    c3.metric("Power Factor (cos φ₀)", f"{pf_no_load:.3f}")

with tab2:
    st.subheader("Circuit Schematic: Two-Wattmeter Method")
    st.write("""
    **Connection Instructions:**
    1. Connect **Ammeter** in series with Line R.
    2. Connect **Voltmeter** across Line R and Line Y.
    3. **W1:** Current coil in Line R, Potential coil across R and B.
    4. **W2:** Current coil in Line Y, Potential coil across Y and B.
    """)
    # Diagram placeholder (In a real app, you would use st.image() here)
    st.warning("⚠️ High Voltage Area: Ensure Variac is at zero before starting simulation.")

# --- Data Logger ---
st.subheader("📋 Observed Data Table")
if 'log' not in st.session_state:
    st.session_state.log = []

if st.button("Log Data Point"):
    st.session_state.log.append({
        "Voltage (V)": v_line,
        "Current (A)": round(i_no_load, 2),
        "W1 (W)": round(w1, 1),
        "W2 (W)": round(w2, 1),
        "Total P (W)": round(w1 + w2, 1)
    })

if st.session_state.log:
    st.table(st.session_state.log)
    if st.button("Clear Table"):
        st.session_state.log = []
