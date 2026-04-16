import streamlit as st
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="Learn EE Interactive - No-Load Test", layout="wide")

# Custom CSS for styling components
st.markdown("""
    <style>
    .variac-container {
        border: 2px solid #333;
        border-radius: 10px;
        background-color: #f0f0f0;
        padding: 20px;
        text-align: center;
        width: 100%;
        max-width: 400px;
        margin: auto;
    }
    .meter-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .phase-label { font-weight: bold; font-size: 1.2em; margin-bottom: 5px;}
    .readout { font-family: 'Courier New', Courier, monospace; font-size: 2.5em; font-weight: bold; color: blue;}
    </style>
""", unsafe_allow_html=True)


# --- Define the Dynamic Variac Component (SVG based) ---
def render_dynamic_variac(voltage):
    """Generates an HTML snippet containing an SVG Variac knob that rotates."""
    
    # Calculate knob rotation angle (0V = 0 degrees, 480V = ~300 degrees)
    # The scale on Variacs typically covers ~300 degrees.
    max_voltage = 480
    rotation_angle = (voltage / max_voltage) * 300 

    svg_code = f"""
    <div class="variac-container">
        <h3>Variac Control</h3>
        <svg width="200" height="200" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="#ddd" stroke-width="2"/>
            
            <g stroke="#333" stroke-width="1">
                <line x1="50" y1="5" x2="50" y2="10"/> <line x1="10" y1="50" x2="15" y2="50"/> <line x1="90" y1="50" x2="85" y2="50"/> }
            </g>
            
            <g transform="rotate({rotation_angle} 50 50)">
                <circle cx="50" cy="50" r="30" fill="#333" stroke="#222" stroke-width="2"/>
                <circle cx="30" cy="50" r="2" fill="#555"/>
                <circle cx="50" cy="30" r="2" fill="#555"/>
                <circle cx="70" cy="50" r="2" fill="#555"/>
                <circle cx="50" cy="70" r="2" fill="#555"/>
                
                <line x1="50" y1="30" x2="50" y2="10" stroke="red" stroke-width="3" stroke-linecap="round"/>
            </g>
            
            <text x="50" y="55" text-anchor="middle" font-size="6" font-family="Arial" fill="#ddd">VARIAC</text>
        </svg>
        <div style="font-size: 1.5em; font-weight: bold;">{voltage} V</div>
        <div style="font-size: 0.8em; color: gray;">0V - {max_voltage}V AC Output</div>
    </div>
    """
    return st.markdown(svg_code, unsafe_allow_html=True)


# --- Dashboard Layout ---
st.title("⚡ 3-Phase Induction Motor: Interactive No-Load Test")
st.markdown("Use the controls on the left to vary the supply voltage and observe the motor's behavior.")

# --- Sidebar Inputs (Simulation Parameters) ---
with st.sidebar:
    st.header("Simulation Control Panel")
    
    # Machine Specifications (Text inputs for customization)
    st.subheader("Motor Rated Values")
    v_rated = st.number_input("Rated Line Voltage (V)", value=415)
    i_rated = st.number_input("Rated Current (A)", value=10.0)
    p_rated = st.number_input("Rated Power (kW)", value=5.5)
    
    st.markdown("---")
    
    # **THIS IS THE MASTER SLIDER CONTROLLING VOLTAGE**
    st.subheader("Voltage Adjustment")
    v_input = st.slider("Select Output Voltage", 0, 480, 415, step=5, help="Controls the output of the 3-phase Variac.")

# --- Render the Realistic components ---
col1, col2 = st.columns([1, 2])

# Left Column: The Interactive Variac
with col1:
    # We call the function, passing the slider value.
    # The SVG redraws and rotates the knob automatically when v_input changes.
    render_dynamic_variac(v_input)

# Right Column: The Machine & Meters (Simplified placeholder for this demo)
with col2:
    st.subheader("Motor Connection & Measurement Bench")
    
    # Mathematical Model Logic (Simple model)
    # Realistic parameters for a ~5.5kW motor
    X_m = 150  # Magnetizing Reactance (Ohms)
    R_core = 1200 # Core Loss Resistance (Ohms)
    
    if v_input > 0:
        v_phase = v_input / np.sqrt(3)
        i_core = v_phase / R_core
        i_mag = v_phase / X_m
        i_no_load = np.sqrt(i_core**2 + i_mag**2) # Line Current
        
        # Simplified LPF Wattmeter values (Two-wattmeter method simulation)
        p_total = 3 * (i_core**2) * R_core # Core Loss + Rotation (simplified)
        w1_sim = (p_total / 2) + (v_input * i_no_load * 0.1) # Simulate imbalance
        w2_sim = (p_total / 2) - (v_input * i_no_load * 0.1) # Simulating potential negative/low reading
        
    else:
        i_no_load = w1_sim = w2_sim = p_total = 0

    # Meter readouts styled with CSS
    with st.container():
        st.markdown('<div class="meter-box">', unsafe_allow_html=True)
        st.markdown('<div class="phase-label">3Ф Line Current (I₀)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="readout">{i_no_load:.2f} A</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Wattmeter 1 (W₁)", f"{w1_sim:.1f} W", help="LPF Wattmeter simulation")
    with c2:
        st.metric("Wattmeter 2 (W₂)", f"{w2_sim:.1f} W", help="LPF Wattmeter simulation")

    st.success(f"Motor status: Running at {v_input}V No-Load.")
    st.info(f"Total rotational loss determined: **{p_total:.1f} W**")
