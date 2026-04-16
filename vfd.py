import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Virtual Lab - No Load Test", layout="wide")

st.title("⚡ 3-Phase Induction Motor Virtual Lab")

st.markdown("### 🔌 No-Load Test Setup with Virtual Instruments")

# --- SIDEBAR INPUTS ---
st.sidebar.header("⚙️ Supply & Motor")

V = st.sidebar.slider("Line Voltage (V)", 200, 500, 400)
I = st.sidebar.slider("No-load Current (A)", 1.0, 20.0, 5.0)
P = st.sidebar.slider("Wattmeter Reading (W)", 100, 5000, 800)

# --- CALCULATIONS ---
pf = P / (np.sqrt(3) * V * I)
pf = min(pf, 1)

# --- GAUGE FUNCTION ---
def gauge(title, value, max_val):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, max_val]},
        }
    ))
    return fig

# --- DISPLAY METERS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(gauge("Voltmeter (V)", V, 500), use_container_width=True)

with col2:
    st.plotly_chart(gauge("Ammeter (A)", I, 20), use_container_width=True)

with col3:
    st.plotly_chart(gauge("Wattmeter (W)", P, 5000), use_container_width=True)

# --- RESULTS ---
st.subheader("📊 Calculated Values")

col4, col5 = st.columns(2)

with col4:
    st.metric("Power Factor", f"{pf:.3f}")

with col5:
    st.metric("Input Power", f"{P:.2f} W")

# --- CONNECTION DIAGRAM (SIMPLIFIED TEXT) ---
st.subheader("🔌 Connection Diagram (Conceptual)")

st.markdown("""
