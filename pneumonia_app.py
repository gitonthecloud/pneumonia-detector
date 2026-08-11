
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
  # NOTE:
  # 1. If using containerized deployment (e.g. docker), must set the host to "0.0.0.0".
  #    It tells the (flask) server to listen on all network interfaces / public IPs,
  #    making it accessible externally.
  #
  # 2. If using non-containerized deployment (e.g. a production WSGI server like Gunicorn),
  #    the host and port settings here will be ignored. The WSGI server will handle the host
  #    and port configuration in the deployment setting e.g.
  #    gunicorn pneumonia_app:server --bind 0.0.0.0:$PORT --workers=1 --threads=1 --timeout=120
  #
  # Whichever way you choose, set it explicitly as these two methods do not conflict.
  
  app.run(debug=False, host="0.0.0.0", port=os.getenv('PORT', 55006))
