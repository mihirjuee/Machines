import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import pandas as pd
import matplotlib
matplotlib.use('Agg')

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="IM Lab Pro", layout="wide")

# =========================
# 🎨 UI STYLE
# =========================
st.markdown("""
<style>

/* ✅ Clean light background */
.stApp {
    background-color: #f5f7fa;
}

/* ✅ Main text */
h1, h2, h3, h4, h5, h6, p, label {
    color: #222222;
}

/* ✅ Cards / Metrics */
div[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}

/* ✅ Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}
section[data-testid="stSidebar"] * {
    color: #222 !important;
}

/* ✅ Buttons */
button[kind="primary"] {
    background-color: #2c7744 !important;
    color: white !important;
    border-radius: 8px;
}

/* ✅ Plot area fix */
.plotly-chart, .stPlotlyChart {
    background-color: white !important;
    border-radius: 10px;
    padding: 10px;
}

/* ✅ Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    color: black;
}

</style>
""", unsafe_allow_html=True)

st.title("⚡ Three Phase Induction Motor Lab")

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("⚙️ Machine Parameters")

V_line = st.sidebar.slider("Line Voltage (V)", 100, 500, 400)
slip = st.sidebar.slider("Slip", 0.01, 1.0, 0.05)

R1 = st.sidebar.slider("R1 (Ω)", 0.1, 5.0, 1.0)
X1 = st.sidebar.slider("X1 (Ω)", 0.1, 5.0, 1.0)
R2 = st.sidebar.slider("R2 (Ω)", 0.1, 5.0, 1.0)
X2 = st.sidebar.slider("X2 (Ω)", 0.1, 5.0, 1.0)
Rc = st.sidebar.slider("Rc (Ω)", 10.0, 500.0, 100.0)
Xm = st.sidebar.slider("Xm (Ω)", 10.0, 500.0, 100.0)

V_phase = V_line / np.sqrt(3)
Z1 = complex(R1, X1)

# =========================
# ⚙️ CORE CALCULATION
# =========================
Z2 = complex(R2/slip, X2)
Zm = 1 / (1/Rc + 1/complex(0, Xm))
Zp = (Z2 * Zm) / (Z2 + Zm)
Zt = Z1 + Zp

I1 = V_phase / Zt
pf = np.cos(np.angle(I1))

P_input = 3 * V_phase * abs(I1) * pf

V_airgap = abs(V_phase - I1 * Z1)
I2 = V_airgap / Z2

P_ag = 3 * (abs(I2)**2) * (R2/slip)
P_mech = P_ag * (1 - slip)
P_out = P_mech

P_stator = 3 * (abs(I1)**2) * R1
P_core = 3 * (abs(V_airgap)**2) / Rc
P_rotor = 3 * (abs(I2)**2) * R2

eff = P_out / P_input if P_input > 0 else 0

# =========================
# 📊 METRICS
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Input Power", f"{P_input:.1f} W")
col2.metric("Output Power", f"{P_out:.1f} W")
col3.metric("Efficiency", f"{eff*100:.1f} %")

# =========================
# 🔌 COLORED CIRCUIT
# =========================
st.subheader("🔌 Power Flow Circuit")

d = schemdraw.Drawing(unit=2.5)

d += elm.SourceSin().label("Vph")
d += elm.Arrow().right().color("blue").label("Pin")

d += elm.Resistor().right().label("R1").color("red")
d += elm.Inductor().right().label("X1")

d += elm.Dot()
d.push()

d += elm.Line().down()
d += elm.Resistor().label("Rc").color("red")
d += elm.Ground()

d.pop()
d.push()

d += elm.Line().down()
d += elm.Inductor().label("Xm")
d += elm.Ground()

d.pop()

d += elm.Line().right()
d += elm.Arrow().right().color("orange").label("Pag")

d += elm.Resistor().label("R2/s")
d += elm.Inductor().label("X2")

d += elm.Arrow().right().color("green").label("Pout")
d += elm.Ground()

d.draw()                 # draw first
fig = plt.gcf()          # get current figure
st.pyplot(fig)           # always works

# =========================
# 🔷 SANKEY DIAGRAM
# =========================
st.subheader("🔷 Power Flow Diagram")

fig_sankey = go.Figure(go.Sankey(

    arrangement="snap",

    node=dict(
        pad=35,
        thickness=40,
        line=dict(color="black", width=2),

        label=[
            "Input\nPower",
            "Stator\nLoss",
            "Core\nLoss",
            "Air-gap\nPower",
            "Rotor\nLoss",
            "Mechanical\nPower",
            "Output\nPower"
        ],

        # ✅ Strong solid colors
        color=[
            "#007BFF",   # Input (Blue)
            "#DC3545",   # Stator loss (Red)
            "#FF7F50",   # Core loss (Orange)
            "#FFC107",   # Air-gap (Yellow)
            "#C82333",   # Rotor loss (Dark red)
            "#28A745",   # Mechanical (Green)
            "#20C997"    # Output (Bright green)
        ]
    ),

    link=dict(
        source=[0,0,0,3,3,5],
        target=[1,2,3,4,5,6],

        value=[
            P_stator,
            P_core,
            P_ag,
            P_rotor,
            P_mech,
            P_out
        ],

        # ✅ Thick & visible links
        color=[
            "rgba(220,53,69,0.8)",
            "rgba(255,127,80,0.8)",
            "rgba(255,193,7,0.9)",
            "rgba(200,35,51,0.8)",
            "rgba(40,167,69,0.9)",
            "rgba(32,201,151,0.9)"
        ],

        # ✅ Show values on hover clearly
        hovertemplate='Power Flow: %{value:.2f} W<extra></extra>'
    )
))

# ✅ Layout for maximum clarity
fig_sankey.update_layout(
    font=dict(size=18, color="black"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=500
)

st.plotly_chart(fig_sankey, use_container_width=True)
# =========================
# 🎛️ PARAMETER VARIATION
# =========================
st.subheader("📈 Parameter Variation")

mode = st.selectbox("Select Parameter", ["Slip", "Rotor Resistance", "Voltage"])

x_vals = np.linspace(0.01, 1, 50)
y_vals = []

for val in x_vals:

    s = slip
    R2_var = R2
    V_var = V_phase

    if mode == "Slip":
        s = val
    elif mode == "Rotor Resistance":
        R2_var = val * 5
    elif mode == "Voltage":
        V_var = val * 400 / np.sqrt(3)

    Z2_var = complex(R2_var/s, X2)
    Zp_var = (Z2_var * Zm) / (Z2_var + Zm)
    Zt_var = Z1 + Zp_var

    I1_var = V_var / Zt_var
    V_airgap_var = abs(V_var - I1_var * Z1)
    I2_var = V_airgap_var / Z2_var

    P_ag_var = 3 * (abs(I2_var)**2) * (R2_var/s)
    P_out_var = P_ag_var * (1 - s)

    y_vals.append(P_out_var)

fig2, ax = plt.subplots()
ax.plot(x_vals, y_vals)
ax.set_title(f"{mode} vs Output Power")
ax.grid()
st.pyplot(fig2)

# =========================
# 📊 MULTI CASE DASHBOARD
# =========================
st.subheader("📊 Multi-Parameter Comparison")

cases = []
for i in range(3):
    s = st.slider(f"Slip {i+1}", 0.01, 1.0, 0.1*(i+1), key=f"s{i}")
    R = st.slider(f"R2 {i+1}", 0.1, 5.0, 1.0+i, key=f"r{i}")
    V = st.slider(f"Voltage {i+1}", 100, 500, 400, key=f"v{i}")
    cases.append((s,R,V))

results = []
for idx,(s,R,V) in enumerate(cases):

    Vp = V/np.sqrt(3)
    Z2 = complex(R/s, X2)
    Zp = (Z2 * Zm) / (Z2 + Zm)
    Zt = Z1 + Zp

    I = Vp / Zt
    V_air = abs(Vp - I*Z1)
    I2 = V_air / Z2

    P_ag = 3*(abs(I2)**2)*(R/s)
    P_out = P_ag*(1-s)

    results.append((f"Case {idx+1}", P_out))

df = pd.DataFrame(results, columns=["Case","Output Power"])
st.dataframe(df)
