# ======================================================================
# DC SHUNT GENERATOR VOLTAGE BUILD-UP SIMULATOR
# FIXED:
# ✅ Proper critical resistance using true tangent from origin
# ✅ Correct slope visualization
# ✅ Accurate tangent point
# ✅ Better OCC realism
# ======================================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voltage Build-up Simulation",
                   page_icon="logo.png",
                   layout="wide")

gradient_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
}
</style>
"""
st.markdown(gradient_bg, unsafe_allow_html=True)

st.title("⚡ DC Shunt Generator: Voltage Build-up")

# --- SIDEBAR ---
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.header("🔧 Generator Settings")

Rf = st.sidebar.slider("Field Resistance (Ohms)", 20.0, 300.0, 100.0)
residual_v = st.sidebar.slider("Residual Voltage (V)", 1.0, 15.0, 5.0)
speed_factor = st.sidebar.slider("Speed Ratio (Actual/Rated)", 0.5, 1.5, 1.0)

# --- FIELD CURRENT RANGE ---
If = np.linspace(0.001, 5, 500)

# --- OCC MODEL ---
# More realistic saturation curve
E_max = 260 * speed_factor
a = 1.25
E_occ = residual_v + E_max * (1 - np.exp(-a * If))

# --- FIELD RESISTANCE LINE ---
V_field = Rf * If

# ======================================================================
# TRUE CRITICAL RESISTANCE:
# Rc = maximum slope of line from origin tangent to OCC
# Rc = max(E/If)
# ======================================================================
slope_origin = E_occ / If
crit_idx = np.argmax(slope_origin)

Rc = slope_origin[crit_idx]
If_crit = If[crit_idx]
E_crit = E_occ[crit_idx]

# Critical resistance line
V_critical = Rc * If

# ======================================================================
# BUILD-UP INTERSECTION
# ======================================================================
diff = E_occ - V_field
idx = None

for i in range(len(diff) - 1):
    if diff[i] >= 0 and diff[i + 1] < 0:
        idx = i
        break

If_intersect, V_intersect = None, None

if idx is not None:
    x1, x2 = If[idx], If[idx + 1]
    y1, y2 = diff[idx], diff[idx + 1]

    If_intersect = x1 - y1 * (x2 - x1) / (y2 - y1)
    V_intersect = residual_v + E_max * (1 - np.exp(-a * If_intersect))

# ======================================================================
# PLOTTING
# ======================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# OCC
ax.plot(If, E_occ, linewidth=3, label="OCC (Open Circuit Characteristic)")

# Field resistance line
ax.plot(If, V_field, '--', linewidth=2,
        label=f"Field Resistance Line (Rf = {Rf:.1f} Ω)")

# Critical resistance line
ax.plot(If, V_critical, ':', linewidth=3,
        label=f"Critical Resistance Line (Rc = {Rc:.1f} Ω)")

# Tangent point
ax.plot(If_crit, E_crit, 'mo', markersize=8)
ax.annotate("Critical Point",
            (If_crit, E_crit),
            xytext=(20, -20),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->"))

# Build-up point
if If_intersect is not None:
    ax.plot(If_intersect, V_intersect, 'ro', markersize=8)

    ax.annotate(f"Build-up Voltage = {V_intersect:.1f} V",
                (If_intersect, V_intersect),
                xytext=(15, 15),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))

# --- AXIS ---
ax.set_xlabel("Field Current, If (A)")
ax.set_ylabel("Generated EMF, Eg (V)")
ax.set_title("Voltage Build-up of DC Shunt Generator")
ax.set_xlim(0, 5)
ax.set_ylim(0, max(E_occ) * 1.15)

ax.grid(True)
ax.legend()

st.pyplot(fig)

# ======================================================================
# STATUS
# ======================================================================
if Rf > Rc:
    st.error("❌ Voltage will NOT build up (Rf > Rc)")
else:
    st.success(f"✅ Voltage builds up successfully to approximately {V_intersect:.1f} V")

# ======================================================================
# THEORY
# ======================================================================
st.divider()
st.subheader("📘 Key Conditions for Voltage Build-up")

st.markdown("""
### Essential Conditions:
### 1️⃣ Residual Magnetism
Initial residual flux must exist.

### 2️⃣ Correct Field Polarity
Field current should strengthen residual flux.

### 3️⃣ Field Resistance Condition
**Rf < Rc**

### 4️⃣ Critical Speed
Generator speed must exceed critical speed.

---
### Formula:
**Critical Resistance = Slope of tangent from origin to OCC**
""")

# ======================================================================
# ADDITIONAL INSIGHTS
# ======================================================================
with st.expander("📊 Additional Insights"):
    st.write(f"**Critical Resistance (Rc):** {Rc:.2f} Ω")
    st.write(f"**Critical Field Current:** {If_crit:.2f} A")
    st.write(f"**Critical Voltage:** {E_crit:.2f} V")

    if If_intersect is not None:
        st.write(f"**Build-up Field Current:** {If_intersect:.2f} A")
        st.write(f"**Build-up Voltage:** {V_intersect:.2f} V")
