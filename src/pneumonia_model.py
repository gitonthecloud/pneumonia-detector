
import os


class PneumoniaModel:
  _instance = None

  def __new__(cls, model=None):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self, model=None):
    self.model = None

  def load_model(self, model_name='pneumonia_detector.pkl'):
      # Only load this memory-intensive model when needed. Python caches the model in memory,
      # so subsequent calls to load_model will not reload the model unless the process is restarted.
      # At the time of writing, this model takes up 1.2GB of memory. Ensure that the provisioning
      # service has enough memory before deployment.
      from fastai.vision.all import load_learner

      model_path = os.path.join(os.getcwd(), "assets", model_name)
      if os.path.exists(model_path):
        print(f'Loading {model_path}')

        if self.model is None:
          # WARNING: load_learner uses Python's insecure pickle. Only load the models you trust.
          self.model = load_learner(model_path)
        return self.model
      else:
        raise FileNotFoundError(f"Model file '{model_path}' not found. Please ensure the model file exists.")



  def predict(self, img):
    try:
      if self.model is None:
        # print('Model is not loaded. Please load the model before making predictions.')
        # return "Error", 0.0
        self.load_model()  # Load the model if it hasn't been loaded yet

      pred, pred_idx, probs = self.model.predict(img)
      return pred, float(probs[pred_idx])
    except Exception as e:
      print(f"Error occurred while making prediction: {e}")
      return "Error", 0.0
