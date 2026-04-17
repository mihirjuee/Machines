import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="DC Motor Simulator", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("⚡ Machine Inputs")
v_in = st.sidebar.slider("Terminal Voltage (V)", 100, 600, 240)
ra_in = st.sidebar.number_input("Armature Resistance (Ω)", value=0.5, step=0.1)
rse_in = st.sidebar.number_input("Series Field Resistance (Ω)", value=0.2, step=0.1)
kphi_in = st.sidebar.slider("Shunt Flux Constant", 1.0, 5.0, 2.0)

# --- NEW: Toggle/Selection Logic ---
st.sidebar.header("Chart Options")
selected_motors = st.sidebar.multiselect(
    "Select Motors to Display",
    ["Shunt", "Series", "Cumulative Compound"],
    default=["Shunt", "Series"]
)

# --- Calculations ---
def get_data(V, Ra, Rse, Kphi):
    Ia = np.linspace(1, 60, 100)
    results = {}
    
    # Shunt
    results["Shunt"] = {
        "speed": (V - (Ia * Ra)) / Kphi,
        "torque": Kphi * Ia,
        "color": "blue"
    }
    
    # Series (Phi proportional to Ia)
    ks = Kphi / 30 
    results["Series"] = {
        "speed": (V - (Ia * (Ra + Rse))) / (ks * Ia),
        "torque": ks * (Ia**2),
        "color": "red"
    }
    
    # Compound
    phi_comp = Kphi + (ks * Ia)
    results["Cumulative Compound"] = {
        "speed": (V - (Ia * (Ra + Rse))) / phi_comp,
        "torque": phi_comp * Ia,
        "color": "green"
    }
    
    return results

data = get_data(v_in, ra_in, rse_in, kphi_in)

# --- UI Layout ---
st.title("⚙️ DC Motor Characteristic Analyzer")

fig = go.Figure()

# Only add traces that are selected in the sidebar
for motor in selected_motors:
    m_data = data[motor]
    fig.add_trace(go.Scatter(
        x=m_data["torque"], 
        y=m_data["speed"], 
        name=motor,
        line=dict(color=m_data["color"], width=3)
    ))

fig.update_layout(
    title=f"Speed vs. Torque ({', '.join(selected_motors)})",
    xaxis_title="Torque (N-m)",
    yaxis_title="Speed (rad/s)",
    yaxis=dict(range=[0, 150]), # Adjusted for visibility
    xaxis=dict(range=[0, 150]),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Comparison Cards
if len(selected_motors) > 0:
    cols = st.columns(len(selected_motors))
    for i, motor in enumerate(selected_motors):
        with cols[i]:
            st.metric(f"{motor} Max Torque", f"{max(data[motor]['torque']):.1f} Nm")
