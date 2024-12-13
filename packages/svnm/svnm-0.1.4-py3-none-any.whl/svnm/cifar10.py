
from svnm.config import modelinfo
from svnm.utils import download_model
from tensorflow.keras.models import load_model
from svnm.preprocessing import load_and_preprocess_image
import os
import numpy as np
from svnm.basemodels import ImageClassificationbaseModel
class Cifar10(ImageClassificationbaseModel):
    def __init__(self):
        """
        Initialize the CIFAR-10 model by downloading and loading the pre-trained model.
        """
        try:
            filepath = modelinfo["Cifar10"]["filename"]
            repoid = modelinfo["Cifar10"]["repoid"]
            modelpath = download_model(repoid, filepath)
            print(modelpath)
            self.model = load_model(modelpath)
            self.metrics = modelinfo["Cifar10"]["metrics"]
            self.classes = modelinfo["Cifar10"]["classes"]
        except KeyError as e:
            raise KeyError(f"Missing key in modelinfo configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error initializing the Cifar10 model: {e}")

    def predict(self, filepath):
        """
        Predicts the class of a single image.

        Args:
            filepath (str): Path to the input image.

        Returns:
            tuple: Predicted label and confidence score.

        Raises:
            FileNotFoundError: If the image file does not exist.
            ValueError: If the prediction cannot be processed.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")

        try:
            image = load_and_preprocess_image(filepath)
            image=np.expand_dims(image,axis=0)
            output = self.model.predict(image)
            id = np.argmax(output[0])
            conf = output[0][id]
            label = self.classes.get(id, "Unknown")
            return label, conf
        except Exception as e:
            raise ValueError(f"Error during prediction: {e}")

    
