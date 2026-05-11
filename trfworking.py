# =========================================
# TRANSFORMER WORKING SIMULATOR
# Streamlit App - Basic Electrical Engineering
# =========================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Transformer Working Simulator",
    page_icon="⚡",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #eaf6ff;
}
.result-box {
    padding: 18px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    text-align: center;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("⚡ Transformer Working Simulator")
st.markdown("### Visualize Step-Up / Step-Down Transformer Operation")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔧 Transformer Controls")

Vp = st.sidebar.slider("Primary Voltage Vp (V)", 50, 500, 230)
Np = st.sidebar.slider("Primary Turns Np", 50, 1000, 500)
Ns = st.sidebar.slider("Secondary Turns Ns", 50, 1000, 250)
load_resistance = st.sidebar.slider("Load Resistance (Ω)", 1, 500, 50)

# ---------------- CALCULATIONS ----------------
turn_ratio = Ns / Np
Vs = Vp * turn_ratio

# Ideal transformer current approximation
Is = Vs / load_resistance
Ip = Is * (Ns / Np)

input_power = Vp * Ip
output_power = Vs * Is

efficiency = (output_power / input_power * 100) if input_power > 0 else 0
efficiency = min(efficiency, 100)

# Transformer Type
if Ns > Np:
    transformer_type = "Step-Up Transformer"
elif Ns < Np:
    transformer_type = "Step-Down Transformer"
else:
    transformer_type = "Isolation Transformer"

# ---------------- FORMULAS ----------------
st.subheader("📘 Transformer Equation")
st.latex(r"\frac{V_s}{V_p} = \frac{N_s}{N_p}")

st.latex(r"\frac{I_s}{I_p} = \frac{N_p}{N_s}")

# ---------------- RESULTS ----------------
col1, col2, col3, col4 = st.columns(4)

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
    <h3>Secondary Current</h3>
    <h2>{Is:.2f} A</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="result-box">
    <h3>Turns Ratio</h3>
    <h2>{turn_ratio:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="result-box">
    <h3>Efficiency</h3>
    <h2>{efficiency:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.info(f"🔍 Transformer Type: {transformer_type}")

# ---------------- TRANSFORMER VISUALIZATION ----------------
st.subheader("🔄 Transformer Construction & Working")

fig = go.Figure()

# Primary winding
for i in range(8):
    fig.add_shape(
        type="circle",
        x0=1,
        y0=i,
        x1=2,
        y1=i + 0.7,
        line_color="blue",
        line_width=3
    )

# Secondary winding
for i in range(8):
    fig.add_shape(
        type="circle",
        x0=7,
        y0=i,
        x1=8,
        y1=i + 0.7,
        line_color="red",
        line_width=3
    )

# Magnetic Core
fig.add_shape(
    type="rect",
    x0=3.5,
    y0=-0.5,
    x1=5.5,
    y1=8.5,
    line_color="black",
    line_width=6
)

# Flux arrows
for y in [1, 3, 5, 7]:
    fig.add_annotation(
        x=4.5,
        y=y + 0.5,
        ax=4.5,
        ay=y + 1.3,
        showarrow=True,
        arrowhead=3
    )

# Labels
fig.add_annotation(x=1.5, y=9.2, text="Primary Coil", showarrow=False)
fig.add_annotation(x=7.5, y=9.2, text="Secondary Coil", showarrow=False)
fig.add_annotation(x=4.5, y=9.8, text="Magnetic Core", showarrow=False)
fig.add_annotation(x=4.5, y=-1, text="Mutual Flux", showarrow=False)

fig.update_layout(
    width=1000,
    height=650,
    xaxis=dict(visible=False, range=[0, 9]),
    yaxis=dict(visible=False, range=[-1.5, 10]),
    plot_bgcolor="white",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- BAR GRAPH ----------------
st.subheader("📊 Voltage Comparison")

bar_fig = go.Figure()

bar_fig.add_trace(go.Bar(
    x=["Primary Voltage", "Secondary Voltage"],
    y=[Vp, Vs]
))

bar_fig.update_layout(
    template="plotly_white",
    yaxis_title="Voltage (V)"
)

st.plotly_chart(bar_fig, use_container_width=True)

# ---------------- AC WAVEFORMS ----------------
st.subheader("🌊 AC Input vs Output Waveform")

t = np.linspace(0, 2 * np.pi, 500)

primary_wave = Vp * np.sin(t)
secondary_wave = Vs * np.sin(t)

wave_fig = go.Figure()

wave_fig.add_trace(go.Scatter(
    x=t,
    y=primary_wave,
    mode="lines",
    name="Primary Voltage"
))

wave_fig.add_trace(go.Scatter(
    x=t,
    y=secondary_wave,
    mode="lines",
    name="Secondary Voltage"
))

wave_fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Voltage",
    template="plotly_white"
)

st.plotly_chart(wave_fig, use_container_width=True)

# ---------------- POWER DISPLAY ----------------
st.subheader("⚡ Power Analysis")

pcol1, pcol2 = st.columns(2)

with pcol1:
    st.metric("Input Power (W)", f"{input_power:.2f}")

with pcol2:
    st.metric("Output Power (W)", f"{output_power:.2f}")

# ---------------- QUIZ ----------------
st.subheader("🧠 Quick Quiz")

quiz = st.radio(
    "If Np = 100 and Ns = 200, the transformer is:",
    ["Step-Down Transformer", "Step-Up Transformer", "Isolation Transformer"]
)

if st.button("Check Answer"):
    if quiz == "Step-Up Transformer":
        st.success("✅ Correct! Since Ns > Np, voltage increases.")
    else:
        st.error("❌ Incorrect! Correct Answer: Step-Up Transformer")

# ---------------- EDUCATIONAL NOTES ----------------
st.markdown("---")
st.markdown("### 📚 Learning Outcomes")
st.markdown("""
- Understand transformer turns ratio  
- Step-Up and Step-Down action  
- Voltage and current transformation  
- Mutual induction principle  
- Magnetic flux linkage  
- Ideal transformer efficiency  
""")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### 🎓 Designed for Basic Electrical Engineering Students")
st.markdown("Learn • Visualize • Explore ⚡")
