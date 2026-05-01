# transformer_test_lab.py
# ============================================================
# VIRTUAL TRANSFORMER TESTING LAB (REAL LAB PANEL STYLE)
# Open Circuit + Short Circuit Test Simulator
# Calculates:
# Rc, Xm, Req, Xeq, Zeq, Regulation, Efficiency
# ============================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Virtual Transformer Testing Lab",
    layout="wide",
    page_icon="⚡"
)

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
st.title("⚡ Virtual Transformer Testing Lab")
st.markdown("### Real Lab Panel Style | Open Circuit + Short Circuit Test Simulator")

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "Open Circuit Test"

# ------------------------------------------------------------
# SIDEBAR CONTROL PANEL
# ------------------------------------------------------------
st.sidebar.header("🎛 Transformer Rating")

rated_kva = st.sidebar.number_input("Rated Power (kVA)", min_value=0.1, value=100.0)
hv_voltage = st.sidebar.number_input("HV Voltage (V)", min_value=1.0, value=11000.0)
lv_voltage = st.sidebar.number_input("LV Voltage (V)", min_value=1.0, value=415.0)
frequency = st.sidebar.number_input("Frequency (Hz)", min_value=1.0, value=50.0)

st.sidebar.markdown("---")
mode = st.sidebar.radio(
    "🧪 Select Test Mode",
    ["Open Circuit Test", "Short Circuit Test"]
)

# ------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------
if mode == "Open Circuit Test":
    st.sidebar.subheader("🔓 Open Circuit Inputs")
    Voc = st.sidebar.number_input("Voc (V)", min_value=0.0, value=415.0)
    Ioc = st.sidebar.number_input("Ioc (A)", min_value=0.0001, value=9.5)
    Poc = st.sidebar.number_input("Poc (W)", min_value=0.0, value=850.0)

else:
    st.sidebar.subheader("🔒 Short Circuit Inputs")
    Vsc = st.sidebar.number_input("Vsc (V)", min_value=0.0, value=620.0)
    Isc = st.sidebar.number_input("Isc (A)", min_value=0.0001, value=9.1)
    Psc = st.sidebar.number_input("Psc (W)", min_value=0.0, value=1250.0)

# ------------------------------------------------------------
# RESET BUTTON
# ------------------------------------------------------------
if st.sidebar.button("🔄 Reset"):
    st.experimental_rerun()

# ------------------------------------------------------------
# ANALOG GAUGE FUNCTION
# ------------------------------------------------------------
def gauge(title, value, max_val):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={"axis": {"range": [0, max_val]}}
    ))
    fig.update_layout(height=250)
    return fig

# ------------------------------------------------------------
# MAIN PANELS
# ------------------------------------------------------------
col1, col2, col3 = st.columns([1.2, 1.2, 1.6])

# ------------------------------------------------------------
# LEFT PANEL - INSTRUMENTS
# ------------------------------------------------------------
with col1:
    st.subheader("🎚 Lab Instruments")

    if mode == "Open Circuit Test":
        st.plotly_chart(gauge("Voltmeter (V)", Voc, max(500, Voc*1.2)), use_container_width=True)
        st.plotly_chart(gauge("Ammeter (A)", Ioc, max(20, Ioc*1.5)), use_container_width=True)
        st.plotly_chart(gauge("Wattmeter (W)", Poc, max(2000, Poc*1.5)), use_container_width=True)

    else:
        st.plotly_chart(gauge("Voltmeter (V)", Vsc, max(1000, Vsc*1.2)), use_container_width=True)
        st.plotly_chart(gauge("Ammeter (A)", Isc, max(20, Isc*1.5)), use_container_width=True)
        st.plotly_chart(gauge("Wattmeter (W)", Psc, max(3000, Psc*1.5)), use_container_width=True)

# ------------------------------------------------------------
# CENTER PANEL - CIRCUIT
# ------------------------------------------------------------
with col2:
    st.subheader("🔌 Transformer Test Circuit")

    if mode == "Open Circuit Test":
        st.markdown("""
        ```text
        AC Supply ─ Variac ─ Ammeter ─ Wattmeter ─ LV Winding
                                   │
                               Voltmeter
        HV Side Open
        ```
        """)
    else:
        st.markdown("""
        ```text
        AC Supply ─ Variac ─ Ammeter ─ Wattmeter ─ HV Winding
                                   │
                               Voltmeter
        LV Side Shorted
        ```
        """)

    st.success("🟢 Supply ON")

# ------------------------------------------------------------
# RIGHT PANEL - CALCULATIONS
# ------------------------------------------------------------
with col3:
    st.subheader("📊 Calculated Parameters")

    if mode == "Open Circuit Test":
        cos_phi0 = Poc / (Voc * Ioc)
        cos_phi0 = np.clip(cos_phi0, -1, 1)

        Iw = Ioc * cos_phi0
        Im = Ioc * np.sin(np.arccos(cos_phi0))

        Rc = Voc / Iw if Iw != 0 else np.inf
        Xm = Voc / Im if Im != 0 else np.inf

        st.metric("No-load Power Factor", f"{cos_phi0:.4f}")
        st.metric("Core Loss Resistance Rc (Ω)", f"{Rc:.2f}")
        st.metric("Magnetizing Reactance Xm (Ω)", f"{Xm:.2f}")
        st.metric("Core Loss (W)", f"{Poc:.2f}")

    else:
        Zeq = Vsc / Isc
        Req = Psc / (Isc ** 2)
        Xeq = np.sqrt(max(Zeq**2 - Req**2, 0))

        st.metric("Equivalent Impedance Zeq (Ω)", f"{Zeq:.4f}")
        st.metric("Equivalent Resistance Req (Ω)", f"{Req:.4f}")
        st.metric("Equivalent Reactance Xeq (Ω)", f"{Xeq:.4f}")
        st.metric("Copper Loss (W)", f"{Psc:.2f}")

# ------------------------------------------------------------
# PERFORMANCE ANALYSIS
# ------------------------------------------------------------
st.markdown("---")
st.header("⚙ Performance Analysis")

load_percent = st.slider("Select Load (%)", 25, 100, 100)
pf = st.selectbox("Power Factor", [0.8, 0.9, 1.0])

# Use default losses if one mode missing
core_loss = Poc if mode == "Open Circuit Test" else 850
copper_loss_full = Psc if mode == "Short Circuit Test" else 1250

output_power = rated_kva * 1000 * (load_percent / 100) * pf
copper_loss = copper_loss_full * (load_percent / 100) ** 2

efficiency = (output_power / (output_power + core_loss + copper_loss)) * 100

# Regulation
if mode == "Short Circuit Test":
    regulation = ((Isc * (Req * pf + Xeq * np.sqrt(1 - pf**2))) / hv_voltage) * 100
else:
    regulation = 0

col4, col5 = st.columns(2)

with col4:
    st.metric("Efficiency (%)", f"{efficiency:.2f}")

with col5:
    st.metric("Voltage Regulation (%)", f"{regulation:.2f}")

# ------------------------------------------------------------
# GRAPHS
# ------------------------------------------------------------
loads = np.arange(25, 126, 25)
eff_curve = []
reg_curve = []

for l in loads:
    out = rated_kva * 1000 * (l / 100) * pf
    cu = copper_loss_full * (l / 100) ** 2
    eff = (out / (out + core_loss + cu)) * 100
    eff_curve.append(eff)

    if mode == "Short Circuit Test":
        reg = ((Isc * (Req * pf + Xeq * np.sqrt(1 - pf**2))) / hv_voltage) * 100
    else:
        reg = 0

    reg_curve.append(reg)

g1, g2 = st.columns(2)

with g1:
    fig_eff = go.Figure()
    fig_eff.add_trace(go.Scatter(x=loads, y=eff_curve, mode='lines+markers'))
    fig_eff.update_layout(
        title="Efficiency vs Load",
        xaxis_title="Load (%)",
        yaxis_title="Efficiency (%)"
    )
    st.plotly_chart(fig_eff, use_container_width=True)

with g2:
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Scatter(x=loads, y=reg_curve, mode='lines+markers'))
    fig_reg.update_layout(
        title="Voltage Regulation vs Load",
        xaxis_title="Load (%)",
        yaxis_title="Regulation (%)"
    )
    st.plotly_chart(fig_reg, use_container_width=True)

# ------------------------------------------------------------
# VIVA MODE
# ------------------------------------------------------------
st.markdown("---")
st.header("🎓 Viva Questions")

questions = [
    "Why is Open Circuit test usually conducted on LV side?",
    "Why is Short Circuit test usually conducted on HV side?",
    "Why is copper loss negligible in OC test?",
    "Why is core loss negligible in SC test?",
    "What is the practical use of equivalent circuit parameters?"
]

st.info(random.choice(questions))

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")
st.caption("⚡ Built for Electrical Engineering Learning | Virtual Transformer Lab")
