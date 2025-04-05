from dash import Dash
from layout import create_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc
import os

external_scripts = [
    'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.min.js',
    "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js",
    'https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.3.2/jspdf.min.js',
]

external_stylesheets = dbc.themes.YETI

app = Dash(__name__, external_stylesheets=[external_stylesheets], external_scripts=external_scripts)

app.title = "ED Simulation"

app.layout = create_layout()

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True)