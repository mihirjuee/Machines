import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(page_title="IM Lab Pro", page_icon="⚡", layout="wide")

# =========================
# 🎨 PROFESSIONAL CSS
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
    color: white;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1c1c1c, #2b2b2b);
}
h1, h2, h3 {
    color: #00e6e6;
}
.stMetric {
    background-color: rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏷️ TITLE
# =========================
st.title("⚡ Induction Motor Lab Pro")
st.subheader("Starting Methods Comparison with Circuit Diagrams")

# =========================
# 🔁 SESSION STATE
# =========================
if "run" not in st.session_state:
    st.session_state.run = False

# =========================
# 🎛️ SIDEBAR CONTROLS
# =========================
st.sidebar.header("⚙️ Motor Parameters")

V = st.sidebar.slider("Rated Voltage (V)", 200, 500, 400)
I_sc = st.sidebar.slider("Short Circuit Current (A)", 50, 500, 200)
T_full = st.sidebar.slider("Full Load Torque (Nm)", 10, 300, 120)
tap = st.sidebar.slider("Auto-Transformer Tap (%)", 50, 100, 70) / 100

st.sidebar.markdown("---")

if st.sidebar.button("▶️ Run Simulation"):
    st.session_state.run = True

if st.sidebar.button("⏹ Stop Simulation"):
    st.session_state.run = False

# =========================
# 🚀 SIMULATION SECTION
# =========================
if st.session_state.run:

    # --- CALCULATIONS ---
    I_dol = I_sc
    T_dol = T_full

    I_sd = I_sc / 3
    T_sd = T_full / 3

    I_auto = I_sc * tap**2
    T_auto = T_full * tap**2

    # =========================
    # 📊 METRICS DASHBOARD
    # =========================
    st.subheader("📊 Live Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("DOL Current", f"{I_dol:.1f} A")
        st.metric("DOL Torque", f"{T_dol:.1f} Nm")

    with col2:
        st.metric("Star-Delta Current", f"{I_sd:.1f} A")
        st.metric("Star-Delta Torque", f"{T_sd:.1f} Nm")

    with col3:
        st.metric("Auto-T Current", f"{I_auto:.1f} A")
        st.metric("Auto-T Torque", f"{T_auto:.1f} Nm")

    # =========================
    # 📈 PLOTS
    # =========================
    st.subheader("📈 Comparative Analysis")

    methods = ["DOL", "Star-Delta", "Auto-T"]

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    ax[0].bar(methods, [I_dol, I_sd, I_auto])
    ax[0].set_title("Starting Current")
    ax[0].set_ylabel("Amperes")
    ax[0].grid(True, linestyle='--', alpha=0.5)

    ax[1].bar(methods, [T_dol, T_sd, T_auto])
    ax[1].set_title("Starting Torque")
    ax[1].set_ylabel("Nm")
    ax[1].grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)

    # =========================
    # 🔌 CIRCUIT DIAGRAMS
    # =========================
    st.subheader("🔌 Circuit Diagrams")

    col1, col2, col3 = st.columns(3)

    # --- DOL ---
    with col1:
        st.markdown("### 🔹 DOL Starter")
        d = schemdraw.Drawing()

        d += elm.SourceV().label("3Φ Supply")
        d += elm.Switch().right().label("Contactor")
        d += elm.Line().right()
        d += elm.Motor().label("IM")

        st.pyplot(d.draw())

    # --- STAR-DELTA ---
    with col2:
        st.markdown("### 🔹 Star-Delta Starter")
        d = schemdraw.Drawing()

        d += elm.SourceV().label("3Φ")
        d += elm.Switch().right().label("Main")
        d += elm.Line().right()
        d += elm.Switch().down().label("Star")
        d += elm.Switch().right().label("Delta")
        d += elm.Line().right()
        d += elm.Motor().label("IM")

        st.pyplot(d.draw())

    # --- AUTO-TRANSFORMER ---
    with col3:
        st.markdown("### 🔹 Auto-Transformer Starter")
        d = schemdraw.Drawing()

        d += elm.SourceV().label("3Φ")
        d += elm.Transformer().right().label("Auto-T")
        d += elm.Switch().right().label("Contactor")
        d += elm.Line().right()
        d += elm.Motor().label("IM")

        st.pyplot(d.draw())

    # =========================
    # 🧠 INSIGHTS
    # =========================
    st.subheader("🧠 Engineering Insights")

    st.info(f"""
• DOL gives highest starting torque but very high current  
• Star-Delta reduces both current & torque to ~33%  
• Auto-transformer provides controlled starting at {tap*100:.0f}% voltage  
• Best choice depends on load requirement  
""")

else:
    st.warning("👉 Click 'Run Simulation' from sidebar")

# =========================
# 📘 THEORY SECTION
# =========================
with st.expander("📘 Theory & Explanation"):

    st.markdown("""
### 🔹 DOL Starter
- Full voltage applied directly  
- High starting current & torque  

### 🔹 Star-Delta Starter
- Voltage reduced to 1/√3  
- Current & torque reduce to 1/3  

### 🔹 Auto-Transformer Starter
- Adjustable voltage using taps  
- Smooth and flexible starting  

---

### ⚡ Key Relations:
- Torque ∝ Voltage²  
- Current ∝ Voltage  
""")
