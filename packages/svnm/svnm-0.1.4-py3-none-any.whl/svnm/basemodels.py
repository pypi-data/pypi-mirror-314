from tensorflow.keras.models import load_model
import numpy as np
import os
from svnm.preprocessing import load_and_preprocess_image
from svnm.config import modelinfo
from svnm.utils import download_model
class ImageClassificationbaseModel:
    def __init__():
        print_svnm_intro()
    def __init__(self,modelname):
        """
        Initialize the model by downloading and loading the pre-trained model.
        """
        try:
            filepath = modelinfo[modelname]["filename"]
            repoid = modelinfo[modelname]["repoid"]
            modelpath = download_model(repoid, filepath)
            self.model = load_model(modelpath)
            self.metrics = modelinfo[modelname]["metrics"]
            self.classes = modelinfo[modelname]["classes"]
        except KeyError as e:
            raise KeyError(f"Missing key in modelinfo configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error initializing the model: {e}")

    def predict(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")
        
        try:
            image = load_and_preprocess_image(filepath)
            image = np.expand_dims(image, axis=0)
            output = self.model.predict(image)
            id = np.argmax(output[0])
            conf = output[0][id]
            label = self.classes.get(id, "Unknown")
            return label, conf
        except Exception as e:
            raise ValueError(f"Error during prediction: {e}")

    def predict_batch(self, filepaths):
        for filepath in filepaths:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Image file not found: {filepath}")

        try:
            images = [load_and_preprocess_image(fp) for fp in filepaths]
            images = np.stack(images)
            outputs = self.model.predict(images)

            predictions = []
            for output in outputs:
                id = np.argmax(output)
                conf = output[id]
                label = self.classes.get(id, "Unknown")
                predictions.append((label, conf))

            return predictions
        except Exception as e:
            raise ValueError(f"Error during batch prediction: {e}")
    def visualize_prediction(self, filepath):
        try:
            import matplotlib.pyplot as plt
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Image file not found: {filepath}")

            label, conf = self.predict(filepath)
            image = tf.keras.preprocessing.image.load_img(filepath)
            plt.imshow(image)
            plt.title(f"Prediction: {label} ({conf:.2f})")
            plt.axis('off')
            plt.show()
        except Exception as e:
            raise RuntimeError(f"Error visualizing prediction: {e}")
