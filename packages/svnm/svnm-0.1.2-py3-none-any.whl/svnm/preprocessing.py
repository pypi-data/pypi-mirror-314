import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img,img_to_array
# Define a function for loading and preprocessing
def load_and_preprocess_image(path):
    image = tf.keras.utils.load_img(path, target_size=(224, 224))
    image_array = tf.keras.utils.img_to_array(image)
    image_array /= 255.0  
    return image_array