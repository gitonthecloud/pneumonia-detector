from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from src.pneumonia_model import PneumoniaModel
import os
import base64
from io import BytesIO
from PIL import Image
import random


class ML:
  def __init__(self):
    self.pm = PneumoniaModel()

    # Dash layout component list
    self.dcl = []

    self.df = None
    self.infer = None
    self.uploaded_contents = None
    self.sample_dir_normal = ''
    self.sample_files_normal = []
    self.sample_dir_pneumonia = ''
    self.sample_files_pneumonia = []

  def get_sample_files(self):
    # TODO: consider using generator to yield sample files instead of loading all at once

    # BASE = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.join(BASE, "data", "sample.png")
    # DATA_DIR = os.path.join(BASE_DIR, "data")
    # img_path = os.path.join(DATA_DIR, "sample.png")

    self.sample_dir_normal = os.getcwd() + '/data/NORMAL/'
    self.sample_files_normal = [f for f in os.listdir(self.sample_dir_normal) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    self.sample_dir_pneumonia = os.getcwd() + '/data/PNEUMONIA/'
    self.sample_files_pneumonia = [f for f in os.listdir(self.sample_dir_pneumonia) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]

  def get_random_sample(self):
    sample_dir = None
    sample_file = None
    condition = '?'
    num = random.randint(0, 1)

    if num == 0:
      sample_dir = self.sample_dir_normal
      if self.sample_dir_normal is not None and len(self.sample_dir_normal) > 0:
        pick = random.randint(0, len(self.sample_files_normal)-1)
        sample_file = self.sample_files_normal[pick]
        condition = 'NORMAL'
    elif num == 1:
      sample_dir = self.sample_dir_pneumonia
      if self.sample_files_pneumonia is not None and len(self.sample_files_pneumonia) > 0:
        pick = random.randint(0, len(self.sample_files_pneumonia)-1)
        sample_file = self.sample_files_pneumonia[pick]
        condition = 'PNEUMONIA'
  
    if sample_file is not None and sample_dir is not None:
      img_path = os.path.join(sample_dir, sample_file)
      img = Image.open(img_path)
      return sample_file, img_path, img, condition
    else:
      return '', '', None, condition

  def run(self):
    self.get_sample_files()
    # self.pm.load_model()

    title = html.H1('Pneumonia Detector',
                    style={
                      'textAlign': 'center'
                    })

    intro_img = html.Img(src='assets/pneumonia.jpg', alt='Pneumonia image',
                         width='100px',
                         style = {'display': 'inline-flex',
                                  'float': 'left',
                                  'padding': '0 10px'})

    background_text = '''
    This software application is powered by a Machine Learning model that specialises
    in image processing. It has been trained with chest X-ray images of normal and
    pneumonia cases. It can detect pneumonia cases with an accuracy of up to 99%.
    '''
    # Disable markdown syntax highlighting
    bg_text_md = dcc.Markdown(background_text, dangerously_allow_html=True)


    copyright = html.Div('@ 2026 - Swee Hing Lee',
                         style={'fontSize': 'xsmall',
                                'color': 'black',
                                'textAlign': 'center'})
    hdr1 = html.Div([html.Br(), title])
    hdr2 = html.Div([intro_img,bg_text_md],
                    style={'margin': '0 160px'})
    hdr3 = html.Div([html.Br(), html.Br(), copyright])

    final_hdr = html.Div([hdr1, hdr2, hdr3],
                   style={
                     'backgroundColor': 'skyblue',
                     'borderRadius': '10px',
                     'padding': '20px'
                   })

    sample_hdr = html.H2('Sample Diagnosis')

    sample_button = dbc.Button('Next sample', id='sample-button', n_clicks=0,
                                className='primary rounded-pill btn-sm',
                                style={
                                  'margin':'0 10px',
                                  'hidden': 'true',
                                  'fontSize': '20px',
                                  'padding': '2px 12px'})

    sample_res = html.Div(id='sample-res',
                  style={
                     'backgroundColor': 'white',

                     'padding': '20px',

                  })

    sample_text = '''
    The following samples is a collection of chest X-ray images of normal and
    pneumonia patients confirmed by clinicians. The Machine Learning model
    have not seen these data before but was able to predict these cases correctly
    at a very high accuracy. Click on the "Next sample" button to view how well
    the model performed in each case.
    '''
    sample_text_md = dcc.Markdown(sample_text)


    @callback(
      Output('sample-res', 'children'),
      Input('sample-button', 'n_clicks'),
      prevent_initial_call=False
    )
    def update_sample(n_clicks):
      if n_clicks is not None:
          sample_file, img_path, img, cond = self.get_random_sample()
          pred, proba = self.pm.predict(img_path)
          return [
            html.Div([
              html.Img(src=img,
                        style={'display': 'inline-flex',
                               'height':'200px',
                               'float': 'left',
                               'padding': '0 10px',
                               'objectFit': 'contain',
                               'objectPosition': 'center'}),
              html.Div([
                # html.H5(sample_file),
                html.H4(f'Actual: {cond}'),
                html.H4(f'Predicted: {round(proba*100, 3)}% - {pred}'),
                # html.H4(f'Probability: {round(proba*100, 6)}%')
              ],
                style={'padding': '2px 0'})
            ],
            style={
              # 'background-color': '#f9f9f9',
              # 'border-radius': '10px',
              # 'padding': '20px',
              'display': 'flex',
              'alignItems': 'center',
              # 'justifyContent': 'center',
              'overflow': 'hidden'
              })
          ]
      return []


    infer_text = '''
    If you are working on a very strange case and is wondering if it is normal or
    pneumonia ... why not ask AI?
    '''
    infer_text_md = dcc.Markdown(infer_text, dangerously_allow_html=True)

    infer_pred = html.Div(id='infer-pred')
    infer_pred_proba = html.Div(id='infer-pred-proba')

    infer_hdr = html.H2('Try it yourself')
    infer_upload = html.Div([
      html.Div('Upload a chest X-ray image for diagnosis.'),
      dcc.Upload(
        id='upload-image',
        children=html.Div([
          'Drag and Drop or ',
          html.A('Select Files')
        ]),
        style={
          'width': '100%',
          'height': '60px',
          'lineHeight': '60px',
          'borderWidth': '1px',
          'borderStyle': 'dashed',
          'borderRadius': '5px',
          'textAlign': 'center',
          'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
      ),
      html.Div(id='output-image-upload')
                                        
    ],
      style={
        'backgroundColor': '#f9f9f9',
        'borderRadius': '10px',
        'padding': '20px'
      })

    def parse_contents(contents, filename, date):
      return html.Div([
        html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        # html.Img(src=contents, style={'maxWidth': '100%'}),
        html.Img(src=contents,
                    style={'display': 'inline-flex',
                        'width':'200px',
                        'float': 'left',
                        'padding': '0 10px'}),
        # html.Hr(),
        # html.Pre(contents[0:200] + '...', style={'whiteSpace': 'pre-wrap'})
      ])

    def base64_to_image(contents: str) -> Image.Image:
      header, encoded = contents.split(",", 1)   # split "data:<mime>;base64,<payload>"
      # binary = base64.b64decode(encoded)

      try:
        binary = base64.b64decode(encoded, validate=True)
        img = Image.open(BytesIO(binary))
        img.load()  # Load the image to ensure it's valid
        # print("Format:", img.format)
        # print("Mode:", img.mode)
        # print("Size:", img.size)
        return img
      except Exception as e:
        print("Base64 decode error:", e)
        return None

    @callback(
      Output('output-image-upload', 'children'),
      Input('upload-image', 'contents'),
      State('upload-image', 'filename'),
      State('upload-image', 'last_modified'),
      prevent_initial_call=False
    )
    def update_output(contents, name, date):
      if contents is not None:
        children = parse_contents(contents, name, date)
        
        self.uploaded_contents = contents
        img = base64_to_image(contents)

        if img is not None:
          pred, proba = self.pm.predict(img)
          self.infer = (pred, proba)
          # return [children, infer_pred, infer_pred_proba]
          return [children, infer_button,
            html.Div([
              round(self.infer[1]*100, 3) if self.infer is not None else "N/A",
              '%',
              '  -  ',
              self.infer[0] if self.infer is not None else "N/A"
            ],
              style={
                'padding': '2px 0',
                'fontWeight': 'bold',
                'fontSize': '40px'
              })
          ]
        else:
          return ["Error decoding image"]
          # infer_pred.children = "Error decoding image"
          # infer_pred_proba.children = "N/A"  



    infer_button = dbc.Button('Inference Result', id='infer-button', n_clicks=0,
                                className='primary rounded-pill btn-sm',
                                style={
                                  'margin':'0 10px',
                                  'hidden': 'true',
                                  'fontSize': '20px',
                                  'padding': '2px 12px'})

    
    self.dcl = [
      final_hdr,
      html.Hr(), sample_hdr, sample_text_md, sample_res, sample_button,
      html.Hr(), infer_hdr, infer_text_md, infer_upload, infer_pred, infer_pred_proba,
      html.Br()
    ]

    return self.dcl
