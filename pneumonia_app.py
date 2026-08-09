
import dash_bootstrap_components as dbc
from dash import Dash
from src.pneumonia_ml import ML
import os


# Incorporate data
ml = ML()

layout = ml.run()

# Initialize the src
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# App layout
app.layout = dbc.Container(layout)

if __name__ == '__main__':
  app.run(debug=False, port=os.getenv('PORT', 55006))
