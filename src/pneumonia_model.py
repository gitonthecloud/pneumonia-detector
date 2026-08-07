from fastai.vision.all import load_learner
import os


class PneumoniaModel:
  def __init__(self, model=None):
    if model is None:
      self.model = self.load_model()
    else:
      if isinstance(model, str):
        self.model = self.load_model(model)


  def load_model(self, model_name='pneumonia_detector.pkl'):
    # WARNING: load_learner uses Python's insecure pickle. Only load the models you trust.
    return load_learner(os.getcwd() + '/model/' + model_name)

  def predict(self, img):
    pred, pred_idx, probs = self.model.predict(img)
    return pred, float(probs[pred_idx])

