
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
    # Only load this memory-intensive model when needed.
    from fastai.vision.all import load_learner

    # WARNING: load_learner uses Python's insecure pickle. Only load the models you trust.
    return load_learner(os.getcwd() + '/model/' + model_name)

  def predict(self, img):
    if self.model is None:
      self.model = self.load_model()

    pred, pred_idx, probs = self.model.predict(img)
    return pred, float(probs[pred_idx])

