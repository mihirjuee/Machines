import plotly.graph_objects as go

def create_meter(value, min_val, max_val, unit, title, color):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': f"{title} ({unit})"},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, max_val*0.8], 'color': "lightgray"},
                {'range': [max_val*0.8, max_val], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# Example usage in Streamlit:
# st.plotly_chart(create_meter(415, 0, 500, "V", "Line Voltage", "blue"))
