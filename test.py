from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np

tf.logging.set_verbosity(tf.logging.INFO)
# Data sets
IRIS_TRAINING = "poker-hand-training-true.data"
IRIS_TEST = "poker-hand-testing.data"

# Load datasets.
training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
    filename=IRIS_TRAINING,
    target_dtype=np.int,
    features_dtype=np.int)
test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
    filename=IRIS_TEST,
    target_dtype=np.int,
    features_dtype=np.int)

# Specify that all features have real-value data
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=10)]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[20, 120,10,20,10],
                                            n_classes=10,
                                            model_dir="/tmp/poker_model_7",
                                            config=tf.contrib.learn.RunConfig(save_checkpoints_secs=50))
validation_monitor = tf.contrib.learn.monitors.ValidationMonitor(
    training_set.data,
    training_set.target,
    every_n_steps=50)
# Fit model.
classifier.fit(x=training_set.data,
               y=training_set.target,
               steps=500000,monitors=[validation_monitor])

# Evaluate accuracy.
accuracy_score = classifier.evaluate(x=test_set.data,
                                     y=test_set.target)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))

# Classify two new flower samples.
new_samples = np.array(
    [[2,9,2,13,2,5,2,4,2,3], [2,5,2,9,4,9,2,3,3,3]], dtype=int)
y = list(classifier.predict(new_samples, as_iterable=True))
print('Predictions: {}'.format(str(y)))