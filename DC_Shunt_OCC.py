import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voltage Build-up Simulation", layout="wide")

st.title("⚡ DC Shunt Generator: Voltage Build-up")

# --- SIDEBAR ---
st.sidebar.header("🔧 Generator Settings")

Rf = st.sidebar.slider("Field Resistance (Ohms)", 50.0, 200.0, 100.0)
residual_v = st.sidebar.slider("Residual Voltage (V)", 1.0, 10.0, 5.0)
speed_factor = st.sidebar.slider("Speed Ratio (Actual/Rated)", 0.5, 1.2, 1.0)

# --- FIELD CURRENT RANGE ---
If = np.linspace(0.001, 3, 200)  # avoid zero division

# --- OCC MODEL (Improved Saturation Curve) ---
k = 250.0
b = 1.2
E_occ = k * (1 - np.exp(-b * If)) * speed_factor + residual_v

# --- FIELD RESISTANCE LINE ---
V_field = If * Rf

# --- FIND INTERSECTION (BUILD-UP POINT) ---
diff = E_occ - V_field

idx = None
for i in range(len(diff) - 1):
    if diff[i] >= 0 and diff[i+1] < 0:
        idx = i
        break

# --- INTERPOLATION FOR ACCURATE POINT ---
If_intersect, V_intersect = None, None

if idx is not None:
    x1, x2 = If[idx], If[idx+1]
    y1, y2 = diff[idx], diff[idx+1]

    If_intersect = x1 - y1 * (x2 - x1) / (y2 - y1)
    V_intersect = k * (1 - np.exp(-b * If_intersect)) * speed_factor + residual_v

# --- CRITICAL RESISTANCE (APPROXIMATION) ---
Rc = max(E_occ / If)

V_critical = If * Rc

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(If, E_occ, label="OCC (Saturation Curve)", linewidth=2)
ax.plot(If, V_field, '--', label=f"Field Resistance Line (Rf = {Rf:.1f} Ω)")
ax.plot(If, V_critical, ':', label=f"Critical Resistance (~{Rc:.1f} Ω)")

# --- MARK INTERSECTION ---
if If_intersect is not None:
    ax.plot(If_intersect, V_intersect, 'ro')

    ax.annotate(f"{V_intersect:.1f} V",
                (If_intersect, V_intersect),
                textcoords="offset points",
                xytext=(10, 10),
                arrowprops=dict(arrowstyle="->"))

# --- AXIS SETTINGS ---
ax.set_xlabel("Field Current (If)")
ax.set_ylabel("Generated EMF (V)")
ax.set_title("Voltage Build-up in DC Shunt Generator")
ax.set_xlim(0, 3)
ax.set_ylim(0, max(E_occ) * 1.1)

ax.grid(True)
ax.legend()

# --- DISPLAY ---
st.pyplot(fig)

# --- STATUS MESSAGE ---
if If_intersect is None:
    st.error("❌ Voltage will NOT build up! (Rf > Critical Resistance)")
else:
    st.success(f"✅ Voltage builds up to approximately {V_intersect:.1f} V")

# --- THEORY SECTION ---
st.divider()
st.subheader("📘 Key Conditions for Voltage Build-up")

st.markdown("""
1. **Residual Magnetism**  
   The generator must have some initial magnetism to start voltage generation.

2. **Correct Field Connection**  
   The field winding must aid the residual flux (not oppose it).

3. **Critical Resistance**  
   Field resistance must satisfy:  
   👉 **Rf < Rc (Critical Resistance)**  
   Otherwise, no voltage build-up occurs.

4. **Critical Speed**  
   The generator must run above a minimum speed to ensure sufficient EMF generation.
""")

# --- EXTRA INFO PANEL ---
with st.expander("📊 Additional Insights"):
    st.write(f"**Critical Resistance (Rc):** {Rc:.2f} Ω")
    if If_intersect is not None:
        st.write(f"**Field Current at Build-up:** {If_intersect:.2f} A")
        st.write(f"**Generated Voltage:** {V_intersect:.2f} V")
