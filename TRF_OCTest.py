import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Transformer OC Test", page_icon="⚡", layout="wide")

st.title("⚡ Single-Phase Transformer Open Circuit Test")
st.write("This application calculates core loss parameters and visualizes the corresponding equivalent circuit.")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("OC Test Data (LV Side)")
    v_oc = st.number_input("Voltage (V_oc) [V]", min_value=1.0, value=220.0)
    i_oc = st.number_input("Current (I_oc) [A]", min_value=0.01, value=0.5)
    p_oc = st.number_input("Power (P_oc) [W]", min_value=0.01, value=50.0)
    st.info("The OC test is performed at rated voltage on the LV winding.")

# --- CALCULATIONS ---
# Initialize results to avoid undefined errors
r_c = 0
x_m = 0
cos_phi = 0
calc_success = False

# Ensure logical inputs: P cannot exceed V*I
if p_oc > (v_oc * i_oc):
    st.error(f"Input Error: Measured Power ({p_oc}W) cannot exceed apparent power ({v_oc * i_oc:.1f} VA). Check your inputs.")
elif v_oc * i_oc > 0:
    # Power Factor calculation: P = V * I * cos(phi)
    cos_phi = np.clip(p_oc / (v_oc * i_oc), 0, 1) # Safety clip
    sin_phi = np.sqrt(1 - cos_phi**2)
    
    # No-load current components
    i_w = i_oc * cos_phi  # Working component (Core loss current)
    i_m = i_oc * sin_phi  # Magnetizing component
    
    # Shunt parameters
    r_c = v_oc / i_w if i_w > 0 else float('inf')
    x_m = v_oc / i_m if i_m > 0 else float('inf')
    calc_success = True

# --- LAYOUT: DIAGRAM & RESULTS ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🔌 Equivalent Circuit (Shunt Branch)")
    
    # Function to draw the shunt branch measured by the OC test
    def draw_oc_equivalent_circuit(ax):
        d = schemdraw.Drawing(canvas=ax)
        
        # Primary Input Terminals
        d += elm.Dot().label('V_oc (LV)', 'left')
        d += (L1 := elm.Line().right(3))
        
        # Shunt Branch (parallel R and X)
        d.push()
        d += elm.Resistor().down(2.5).label(f'Rc\n({r_c:.1f} Ω)', 'right')
        d.pop()
        
        d.move(3, 0) # Move to place magnetizing reactance
        d.push()
        d += elm.Inductor().down(2.5).label(f'Xm\n({x_m:.1f} Ω)', 'right')
        d.pop()
        
        # Bottom connection / Return path
        d.move(-3, -2.5)
        d += (L2 := elm.Line().left(3))
        d += elm.Dot().label('Common', 'left')
        
        # Series components (negligible during OC test, shown as simple lines)
        d += elm.Line().right(2).at(L1.end).label('R1, X1 (Negligible)', 'top')
        d += elm.Line().right(2).at(L2.end)
        
        # Add labels for currents
        d += elm.Label().at(L1.start).label('I_oc', 'top')
        d += elm.Label().at(L1.end).label('I_w', 'left') # Core loss current
        
        d.draw()

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off') # Hide axes
    draw_oc_equivalent_circuit(ax)
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("📊 Results")
    if calc_success:
        st.success("Parameters Calculated Successfully")
        
        st.metric("Core Loss (P_core)", f"{p_oc:.1f} W")
        st.metric("Core Resistance (Rc)", f"{r_c:.1f} Ω")
        st.metric("Magnetizing Reactance (Xm)", f"{x_m:.1f} Ω")
        
        st.divider()
        
        st.metric("No-Load Power Factor", f"{cos_phi:.4f}")
        
        # Display as a percentage of apparent power
        apparent_power = v_oc * i_oc
        loss_percentage = (p_oc / apparent_power) * 100
        st.info(f"The core losses account for {loss_percentage:.1f}% of the no-load apparent power ({apparent_power:.1f} VA).")
        
    else:
        st.warning("Enter valid test data in the sidebar to view results.")
