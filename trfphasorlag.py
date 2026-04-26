import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE SETUP =================
st.set_page_config(page_title="Professional Phasor", layout="wide")
st.title("⚡ Clear-View Transformer Phasor Diagram")

# ... [Keep your inputs and calculations same as previous step] ...

# ================= IMPROVED PLOTTING =================
def draw_arrow_large(fig, start, end, name, color):
    # Thicker lines for visibility
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode='lines', line=dict(color=color, width=4) 
    ))
    # Larger, clearer arrowheads
    fig.add_annotation(
        ax=start.real, ay=start.imag, x=end.real, y=end.imag,
        showarrow=True, arrowhead=2, arrowsize=2, arrowwidth=3, arrowcolor=color
    )
    # Larger, bold labels
    fig.add_annotation(
        x=end.real, y=end.imag, text=f"<b>{name}</b>", 
        showarrow=False, font=dict(color=color, size=20),
        yshift=20 
    )

fig = go.Figure()
# ... [Logic remains same as before, calling draw_arrow_large] ...

fig.update_layout(
    template="plotly_white",
    # Fixed range prevents the diagram from shrinking
    xaxis=dict(range=[-2.5, 2.5], zeroline=True, zerolinecolor='black', showgrid=True),
    yaxis=dict(range=[-2, 2], zeroline=True, zerolinecolor='black', showgrid=True, scaleanchor="x"),
    # Add margins so labels don't get cut off
    margin=dict(l=40, r=40, t=40, b=40),
    height=700, 
    showlegend=False
)
