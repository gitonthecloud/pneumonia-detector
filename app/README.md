# pneumonia-detector
An AI powered software application that predicts pneumonia from chest X-ray images

# Dataset
The machine learning model used in this software was trained using data sourced from:

Data: https://data.mendeley.com/datasets/rscbjbr9sj/2

License: https://creativecommons.org/licenses/by/4.0/ (CC BY 4.0)

Some of the test data have been bundled here for demonstration only. There is no intention
to distribute them. Therefore, a licence is not required for this scenario. If the
circumstance changes later on, then, a licence should be added.

# Provisioning
This app is currently deployed at render.com.

The following settings are used:

Build Command: pip install -r app/requirements.txt

Start Command: gunicorn pneumonia_app:server --bind 0.0.0.0:$PORT --workers=1 --threads=1 --timeout=120

Environment Variables: PORT <any number starting from 10000>

In order to instruct Render to use a specific version of Python, at the time of this writing,
there are two ways:

1. create a file called ".python-version"
in the project root directory and put the desired Python version in it e.g. 3.10.12. Ensure that this
file is NOT specified in .gitignore.

2. Inside the project in Render, add environment variable, PYTHON_VERSION, with value 3.10.12