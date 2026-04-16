import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(page_title="Learn EE Interactive Lab", layout="wide")

# Custom CSS for the Lab Environment
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .variac-container {
        border: 4px solid #444;
        border-radius: 15px;
        background-color: #d1d1d1;
        padding: 20px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
    }
    .meter-label { font-weight: bold; font-size: 1.1em; color: #333; }
    </style>
""", unsafe_allow_html=True)

# --- Real-Look Gauge Function ---
def create_gauge(value, min_val, max_val, title, unit, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"<b>{title}</b><br><span style='font-size:0.8em'>{unit}</span>"},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_val*0.8], 'color': "#f0f0f0"},
                {'range': [max_val*0.8, max_val], 'color': "#ffcccc"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- App Header ---
st.title("🔌 Induction Motor No-Load Test Simulator")
st.write("Adjust the Variac to vary the 3-phase supply voltage and observe the motor parameters.")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Machine Specs")
    v_rated = st.number_input("Rated Line Voltage (V)", value=415)
    i_rated = st.number_input("Rated Current (A)", value=10.0)
    
    st.markdown("---")
    st.header("Manual Variac Control")
    v_input = st.slider("Rotate Knob", 0, 480, 415, step=1)

# --- Physics Engine: No-Load Logic ---
Rc = 1000  
Xm = 120   
v_phase = v_input / np.sqrt(3)

if v_phase > 0:
    i_core = v_phase / Rc
    i_mag = v_phase / Xm
    i_0 = np.sqrt(i_core**2 + i_mag**2) 
    p_0 = 3 * (i_core**2) * Rc          
    
    phi_0 = np.arccos(i_core / i_0)
    w1 = v_input * i_0 * np.cos(np.radians(30) + phi_0)
    w2 = v_input * i_0 * np.cos(np.radians(30) - phi_0)
else:
    i_0 = p_0 = w1 = w2 = 0

# --- Layout: Variac and Meters ---
col_variac, col_meters = st.columns([1, 2])

with col_variac:
    st.markdown('<div class="variac-container">', unsafe_allow_html=True)
    rotation = (v_input / 480) * 270 
    
    svg_variac = f"""
    <svg width="180" height="180" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="48" fill="#555" />
        <circle cx="50" cy="50" r="40" fill="#eee" stroke="#333" stroke-width="2"/>
        <g stroke="#333" stroke-width="1">
            <line x1="50" y1="10" x2="50" y2="15"/>
            <line x1="10" y1="50" x2="15" y2="50"/>
            <line x1="90" y1="50" x2="85" y2="50"/>
        </g>
        <g transform="rotate({rotation} 50 50)">
            <circle cx="50" cy="50" r="25" fill="#222" />
            <line x1="50" y1="50" x2="50" y2="28" stroke="red" stroke-width="4" stroke-linecap="round"/>
        </g>
    </svg>
    <div style="font-size: 2em; font-weight: bold; color: #d32f2f;">{v_input} V</div>
    <div class="meter-label">VARIAC CONTROL</div>
    """
    st.markdown(svg_variac, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_meters:
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.plotly_chart(create_gauge(v_input, 0, 500, "Voltmeter", "Volts (V)", "#1f77b4"), use_container_width=True)
        st.plotly_chart(create_gauge(w1 + w2, 0, 1500, "Total Wattmeter", "Watts (W)", "#2ca02c"), use_container_width=True)
    with m_col2:
        st.plotly_chart(create_gauge(i_0, 0, i_rated, "Ammeter", "Amps (A)", "#d62728"), use_container_width=True)
        st.info("### Wattmeter Readings")
        st.write(f"**W1:** {w1:.2f} W")
        st.write(f"**W2:** {w2:.2f} W")

st.divider()

# --- Realistic Connection Diagram Function ---
def render_connection_diagram():
    svg_diag = """
    <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; text-align: center;">
        <svg width="100%" height="auto" viewBox="0 0 800 350" preserveAspectRatio="xMidYMid meet">
            <text x="10" y="55" font-family="Arial" font-weight="bold" fill="red">R</text>
            <text x="10" y="155" font-family="Arial" font-weight="bold" fill="#FFD700">Y</text>
            <text x="10" y="255" font-family="Arial" font-weight="bold" fill="blue">B</text>

            <line x1="30" y1="50" x2="80" y2="50" stroke="red" stroke-width="3"/>
            <rect x="80" y="30" width="50" height="40" rx="5" fill="#333"/>
            <text x="88" y="55" fill="white" font-family="Arial" font-size="10">AMM</text>
            <line x1="130" y1="50" x2="180" y2="50" stroke="red" stroke-width="3"/>
            <rect x="180" y="25" width="70" height="50" rx="5" fill="#f4f4f4" stroke="#333" stroke-width="2"/>
            <text x="205" y="55" fill="black" font-family="Arial" font-weight="bold">W1</text>
            <circle cx="215" cy="75" r="4" fill="red"/> 
            <line x1="250" y1="50" x2="600" y2="50" stroke="red" stroke-width="3"/>

            <line x1="30" y1="150" x2="600" y2="150" stroke="#FFD700" stroke-width="3"/>

            <line x1="30" y1="250" x2="180" y2="250" stroke="blue" stroke-width="3"/>
            <rect x="180" y="225" width="70" height="50" rx="5" fill="#f4f4f4" stroke="#333" stroke-width="2"/>
            <text x="205" y="255" fill="black" font-family="Arial" font-weight="bold">W2</text>
            <circle cx="215" cy="225" r="4" fill="blue"/>
            <line x1="250" y1="250" x2="600" y2="250" stroke="blue" stroke-width="3"/>

            <line x1="215" y1="75" x2="215" y2="150" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
            <line x1="215" y1="225" x2="215" y2="150" stroke="blue" stroke-width="2" stroke-dasharray="5,5"/>

            <rect x="40" y="80" width="30" height="40" rx="3" fill="#555"/>
            <text x="48" y="105" fill="white" font-size="10">V</text>
            <line x1="55" y1="50" x2="55" y2="80" stroke="red" stroke-width="2"/>
            <line x1="55" y1="120" x2="55" y2="150" stroke="#FFD700" stroke-width="2"/>

            <rect x="600" y="40" width="140" height="230" rx="10" fill="#777" stroke="#333" stroke-width="3"/>
            <rect x="615" y="60" width="110" height="190" rx="5" fill="#999" />
            <text x="635" y="290" font-family="Arial" font-weight="bold">3Ф MOTOR</text>
        </svg>
    </div>
    """
    st.markdown(svg_diag, unsafe_allow_html=True)

st.subheader("🛠️ Experimental Connection Diagram")
render_connection_diagram()

# --- Results & Table ---
st.divider()
pf = (w1 + w2) / (np.sqrt(3) * v_input * i_0) if (v_input > 0 and i_0 > 0) else 0

st.subheader("📊 Test Results")
c1, c2, c3 = st.columns(3)
c1.metric("Current (I₀)", f"{i_0:.3f} A")
c2.metric("Total Power (P₀)", f"{(w1+w2):.2f} W")
c3.metric("Power Factor", f"{pf:.3f}")

st.table({
    "Voltage (V)": [v_input],
    "Current (A)": [round(i_0, 3)],
    "Power (W)": [round(w1 + w2, 2)],
    "Power Factor": [round(pf, 3)]
})
