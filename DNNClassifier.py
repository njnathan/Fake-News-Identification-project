import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn import model_selection

SENTIMENT_LABELS = [
    0, 1
]

# Add a column with readable values representing the sentiment.w
def add_readable_labels_column(df, sentiment_value_column):
  df["label"] = df[sentiment_value_column].replace(
      range(2), SENTIMENT_LABELS)

# The data does not come with a validation set so we'll create one from the
# training set.
def get_data(validation_set_ratio=0.01):
  train_df = pd.read_csv("inputs/UseCase1TrainShuffled.csv", keep_default_na=False, header=0, delimiter='\t', quoting=3)
  test_df = pd.read_csv("inputs/UseCase1TestShuffled.csv", keep_default_na=False, header=0, delimiter='\t', quoting=3)

  # Add a human readable label.
  add_readable_labels_column(train_df, "label")

  # We split by sentence ids, because we don't want to have phrases belonging
  # to the same sentence in both training and validation set.
  train_indices, validation_indices = model_selection.train_test_split(
      np.unique(train_df["id"]),
      test_size=validation_set_ratio,
      random_state=0)

  validation_df = train_df[train_df["id"].isin(validation_indices)]
  train_df = train_df[train_df["id"].isin(train_indices)]
  print("Split the training data into %d training and %d validation examples." %
        (len(train_df), len(validation_df)))

  return train_df, validation_df, test_df

print("Split data")

train_df, validation_df, test_df = get_data()
train_df.head()

# Training input on the whole training set with no limit on training epochs.
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["label"], num_epochs=20, shuffle=True)

# Prediction on the whole training set.
predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["label"], shuffle=False)
# Prediction on the validation set.
predict_validation_input_fn = tf.estimator.inputs.pandas_input_fn(
    validation_df, validation_df["label"], shuffle=False)
# Prediction on the test set.
predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
    test_df, shuffle=False)
embedded_text_feature_column = hub.text_embedding_column(
    key="text",
    module_spec="https://tfhub.dev/google/nnlm-en-dim128/1",
    trainable=True)
# We don't need to keep many checkpoints.
run_config = tf.estimator.RunConfig(keep_checkpoint_max=1)

estimator = tf.estimator.DNNClassifier(
    hidden_units=[250, 500],
    feature_columns=[embedded_text_feature_column],
    n_classes=5,
    config=run_config,
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.003))

estimator.train(input_fn=train_input_fn, steps=1000);
train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
validation_eval_result = estimator.evaluate(input_fn=predict_validation_input_fn)

print("Training set accuracy: {accuracy}".format(**train_eval_result))
print("Validation set accuracy: {accuracy}".format(**validation_eval_result))

def get_predictions(estimator, input_fn):
  return [x["class_ids"][0] for x in estimator.predict(input_fn=input_fn)]

test_df["Predictions"] = get_predictions(estimator, predict_test_input_fn)
test_df.to_csv(
    'outputs/OptimumDNNOutput.csv',
    columns=["id", "Predictions"],
    header=["id", "label"],
    index=False)

