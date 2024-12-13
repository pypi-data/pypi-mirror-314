# Optional: Add version or metadata
from svnm.utils import print_svnm_intro
__version__ = "0.1.4"
print_svnm_intro()
import os
import logging
import warnings
import tensorflow as tf
import absl.logging

# Suppress TensorFlow GPU-related errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Suppress absl logging
absl.logging.set_verbosity(absl.logging.ERROR)

# Suppress warnings globally
logging.getLogger('tensorflow').setLevel(logging.ERROR)

