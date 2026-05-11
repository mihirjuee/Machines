
# =========================================
# TRANSFORMER WORKING SIMULATOR

# =========================================
=========================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go

---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="Transformer Working Simulator",
page_icon="⚡",
layout="wide"
)

---------------- CUSTOM CSS ----------------

st.markdown("""

<style> .main { background-color: #eaf6ff; } .result-box { padding:18px; border-radius:15px; background-color:white; box-shadow:2px 2px 10px rgba(0,0,0,0.15); text-align:center; margin-bottom:10px; } </style>

""", unsafe_allow_html=True)

---------------- TITLE ----------------

st.title("⚡ Transformer Working Simulator")
st.markdown("### Visualize Step-Up / Step-Down Transformer Operation")

---------------- SIDEBAR ----------------

st.sidebar.header("🔧 Transformer Controls")

Vp = st.sidebar.slider("Primary Voltage (Vp)", 50, 500, 230)
Np = st.sidebar.slider("Primary Turns (Np)", 50, 1000, 500)
Ns = st.sidebar.slider("Secondary Turns (Ns)", 50, 1000, 250)
load_resistance = st.sidebar.slider("Load Resistance (Ω)", 1, 500, 50)

---------------- CALCULATIONS ----------------

turn_ratio = Ns / Np
Vs = Vp * turn_ratio
Ip = Vp / max(Np, 1)
Is = Vs / max(load_resistance, 1)
efficiency = min((Vs * Is) / (Vp * Ip + 1e-9) * 100, 100)

transformer_type = "Step-Up Transformer" if Ns > Np else "Step-Down Transformer" if Ns < Np else "Isolation Transformer"

---------------- FORMULAS ----------------

st.subheader("📘 Transformer Equation")
st.latex(r"\frac{V_s}{V_p} = \frac{N_s}{N_p}")

---------------- MAIN RESULTS ----------------

col1, col2, col3 = st.columns(3)

with col1:
st.markdown(f"""
<div class="result-box">
<h3>Secondary Voltage</h3>
<h2>{Vs:.2f} V</h2>
</div>
""", unsafe_allow_html=True)

with col2:
st.markdown(f"""
<div class="result-box">
<h3>Turn Ratio</h3>
<h2>{turn_ratio:.2f}</h2>
</div>
""", unsafe_allow_html=True)

with col3:
st.markdown(f"""
<div class="result-box">
<h3>Efficiency</h3>
<h2>{efficiency:.2f}%</h2>
</div>
""", unsafe_allow_html=True)

st.info(f"🔍 Transformer Type: {transformer_type}")

---------------- TRANSFORMER DIAGRAM ----------------

st.subheader("🔄 Transformer Visualization")

fig = go.Figure()

Primary coil

for i in range(8):
fig.add_shape(
type="circle",
x0=1, y0=i,
x1=2, y1=i+0.8,
line_color="blue"
)

Secondary coil

for i in range(8):
fig.add_shape(
type="circle",
x0=6, y0=i,
x1=7, y1=i+0.8,
line_color="red"
)

Core

fig.add_shape(type="rect", x0=3, y0=-0.5, x1=5, y1=8.5, line_color="black", line_width=5)

Flux arrows

for y in [1, 3, 5, 7]:
fig.add_annotation(
x=4, y=y,
ax=4, ay=y+0.8,
showarrow=True,
arrowhead=3
)

Labels

fig.add_annotation(x=1.5, y=8.8, text="Primary", showarrow=False)
fig.add_annotation(x=6.5, y=8.8, text="Secondary", showarrow=False)
fig.add_annotation(x=4, y=9.5, text="Magnetic Core", showarrow=False)

fig.update_layout(
width=900,
height=600,
xaxis=dict(visible=False, range=[0, 8]),
yaxis=dict(visible=False, range=[-1, 10]),
plot_bgcolor="white",
margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

---------------- VOLTAGE COMPARISON GRAPH ----------------

st.subheader("📈 Primary vs Secondary Voltage")

bar_fig = go.Figure(data=[
go.Bar(name='Voltage', x=['Primary Voltage', 'Secondary Voltage'], y=[Vp, Vs])
])

bar_fig.update_layout(
template="plotly_white",
yaxis_title="Voltage (V)"
)

st.plotly_chart(bar_fig, use_container_width=True)

---------------- WAVEFORM ----------------

st.subheader("🌊 AC Waveform")

t = np.linspace(0, 2*np.pi, 500)
primary_wave = Vp * np.sin(t)
secondary_wave = Vs * np.sin(t)

wave_fig = go.Figure()
wave_fig.add_trace(go.Scatter(x=t, y=primary_wave, mode='lines', name='Primary Voltage'))
wave_fig.add_trace(go.Scatter(x=t, y=secondary_wave, mode='lines', name='Secondary Voltage'))

wave_fig.update_layout(
xaxis_title="Time",
yaxis_title="Voltage",
template="plotly_white"
)

st.plotly_chart(wave_fig, use_container_width=True)

---------------- QUIZ ----------------

st.subheader("🧠 Quick Quiz")

answer = st.number_input("If Np = 100 and Ns = 200, transformer is:", min_value=0)

if st.button("Check Answer"):
st.success("✅ Step-Up Transformer")

---------------- EDUCATIONAL NOTES ----------------

st.markdown("---")
st.markdown("### 📚 Learning Outcomes")
st.markdown("""

Understand turns ratio
Step-Up and Step-Down action
Mutual induction
Voltage transformation
Magnetic flux linkage
""")
---------------- FOOTER ----------------

st.markdown("---")
st.markdown("### 🎓 Designed for Basic Electrical Engineering Students")
st.markdown("Learn • Visualize • Explore ⚡")
