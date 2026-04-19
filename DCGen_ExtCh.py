import streamlit as st
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import numpy as np

# ================= PAGE =================
st.set_page_config(page_title="DC Generator Virtual Lab", page_icon="logo.png", layout="wide")

st.title("⚡ DC Generator Virtual Lab (All Types + Characteristics)")

# ================= SIDEBAR =================
gen_type = st.sidebar.selectbox(
    "Select DC Generator Type",
    [
        "Separately Excited",
        "Shunt Generator",
        "Series Generator",
        "Compound (Short Shunt)"
    ]
)
st.header("Machine Parameters")

phi = st.slider("Flux per pole (ϕ in Wb)", 0.01, 0.2, 0.05)
N = st.slider("Speed (N in RPM)", 200, 2000, 1000)
Ra = st.sidebar.slider("Armature Resistance (Ohm)", 0.1, 5.0, 1.0)
k = st.sidebar.slider("Machine constant (k)", 0.5, 5.0, 1.0)
R_load = st.sidebar.slider("Load Resistance (Ohm)", 1, 100, 20)
V = k * phi * N
# ================= CIRCUITS =================

def separately_excited():
    d = schemdraw.Drawing(unit=2)
    
    d += elm.Line().up()
    d += elm.Motor().label("Ea")
    d += elm.Resistor().label("Ra")
    d += elm.Line().right()
    d += elm.Resistor().down().label("Load")
    d += elm.Line().down()
    d += elm.Line().left()
    return d


def shunt_generator():
    d = schemdraw.Drawing(unit=2)

    # Armature
    d += elm.Motor().label("Ea")
    d += elm.Resistor().label("Ra")

    # Junction point (no node stored)
    d += elm.Dot()

    # Load branch
    d.push()
    d += elm.Line().right()
    d += elm.Resistor().down().label("Load")
    d.pop()

    # Shunt field branch (parallel path)
    d.push()
    d += elm.Line().up()
    d += elm.Resistor().label("Rsh (Field)")
    d += elm.Line().down()
    d.pop()

    return d


def series_generator():
    d = schemdraw.Drawing(unit=2)

    d += elm.Motor().label("Ea")
    d += elm.Resistor().label("Ra")
    d += elm.Resistor().label("Series Field")
    d += elm.Resistor().label("Load")

    return d


def compound_generator():
    d = schemdraw.Drawing(unit=2)

    # ===== ARMATURE =====
    d += elm.Motor().label("Ea")
    d += elm.Resistor().label("Ra")

    # Junction point
    d += elm.Dot()

    # ===== SERIES FIELD + LOAD PATH =====
    d.push()
    d += elm.Resistor().right().label("Series Field")
    d += elm.Resistor().down().label("Load")
    d.pop()

    # ===== SHUNT FIELD (PARALLEL) =====
    d.push()
    d += elm.Line().up()
    d += elm.Resistor().label("Shunt Field")
    d += elm.Line().down()
    d.pop()

    return d


# ================= CHARACTERISTICS =================

def characteristics(gen_type):
    IL = np.linspace(0, 10, 60)

    if gen_type == "Separately Excited":
        Vt = V - 0.5 * IL * Ra
        return IL, Vt

    elif gen_type == "Shunt Generator":
        Vt = V - 0.8 * IL * Ra - 0.6 * IL**1.2
        return IL, Vt

    elif gen_type == "Series Generator":
        Vt = V + 2.0 * IL - 0.7 * IL**1.3
        Vt = np.maximum(Vt, 0)
        return IL, Vt

    else:
        IL = np.linspace(0, 10, 60)

        under = V - 1.2 * IL - 0.4 * IL**1.3
        flat = V - 0.3 * IL
        over = V + 0.4 * IL - 0.1 * IL**1.2

        return IL, under, flat, over


# ================= SELECTION =================
if gen_type == "Separately Excited":
    d = separately_excited()
elif gen_type == "Shunt Generator":
    d = shunt_generator()
elif gen_type == "Series Generator":
    d = series_generator()
else:
    d = compound_generator()


# ================= UI LAYOUT =================
col1, col2 = st.columns([1.2, 1])

# -------- CIRCUIT --------
with col1:
    st.subheader("🔌 Circuit Diagram")

    d.draw()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.clf()

# -------- CHARACTERISTICS --------
with col2:
    st.subheader("📉 External Characteristics")

    fig2, ax = plt.subplots()

    if gen_type != "Compound (Short Shunt)":

        IL, Vt = characteristics(gen_type)

        ax.plot(IL, Vt, linewidth=2)

        ax.set_xlabel("Load Current (IL)")
        ax.set_ylabel("Terminal Voltage (Vt)")
        ax.set_title(gen_type + " Characteristic")
        ax.grid(True)

    else:

        IL, under, flat, over = characteristics(gen_type)

        ax.plot(IL, under, label="Under-compounded", linewidth=2)
        ax.plot(IL, flat, label="Flat-compounded", linewidth=2)
        ax.plot(IL, over, label="Over-compounded", linewidth=2)

        ax.set_xlabel("Load Current (IL)")
        ax.set_ylabel("Terminal Voltage (Vt)")
        ax.set_title("Compound Generator Characteristics")
        ax.grid(True)
        ax.legend()

    st.pyplot(fig2)

# ================= INFO =================
st.info("This simulation shows DC generator circuits and external characteristics.")
