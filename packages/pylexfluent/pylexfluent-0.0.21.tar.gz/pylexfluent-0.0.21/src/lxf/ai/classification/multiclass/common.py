

import itertools
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

random_seed_base=13

# params for learning
embedding_dim=32
lr_base = 5e-3
epochs=200

# global variables
concatenate_col = True
X_col_key_phrases ='PhrasesCles'
X_col_key_words='MotsCles'
y_col='Classification'
drop_columns_for_concatenate_col=['Classification','Libelle']
drop_columns=['Classification','Libelle','MotsCles']
# Set maximum_sequence length as all samples are not of the same length.
# Vocabulary size and number of words in a sequence.
vocab_size = 10000
sequence_length = 512
if concatenate_col ==False :
  ngrams = 4
else :
  ngrams=None
batch_size=32

import tensorflow as tf


def vectorize_text(vectorize_layer,text, label):
  text = tf.expand_dims(text, -1)
  return vectorize_layer(text), label

def create_model(class_names,model_name,vectorize_layer):
    #define tensorboard callback
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs/"+model_name)
    # Create a learning rate scheduler callback
    lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: lr_base * 10**(epoch/epochs))
    #set seed 
    tf.random.set_seed(random_seed_base)
    #create the model
    model=tf.keras.Sequential(name=model_name,layers=[
        vectorize_layer,
        tf.kerasEmbedding(vocab_size,embedding_dim,name='embedding'),
        tf.keras.GlobalAveragePooling1D(),
        tf.kereas.Dense(embedding_dim,activation='relu'),
        tf.keras.Dense(len(class_names),activation='softmax')
    ])
    #compile the model 
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics=["accuracy"])
    return model, [tensorboard_callback,lr_scheduler]


# Note: The following confusion matrix code is a remix of Scikit-Learn's 
# plot_confusion_matrix function - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.plot_confusion_matrix.html
# and Made with ML's introductory notebook - https://github.com/GokuMohandas/MadeWithML/blob/main/notebooks/08_Neural_Networks.ipynb
# Our function needs a different name to sklearn's plot_confusion_matrix
def make_confusion_matrix(y_true, y_pred, classes=None, figsize=(10, 10), text_size=20): 
  """Makes a labelled confusion matrix comparing predictions and ground truth labels.

  If classes is passed, confusion matrix will be labelled, if not, integer class values
  will be used.

  Args:
    y_true: Array of truth labels (must be same shape as y_pred).
    y_pred: Array of predicted labels (must be same shape as y_true).
    classes: Array of class labels (e.g. string form). If `None`, integer labels are used.
    figsize: Size of output figure (default=(10, 10)).
    text_size: Size of output figure text (default=15).
  
  Returns:
    A labelled confusion matrix plot comparing y_true and y_pred.

  Example usage:
    make_confusion_matrix(y_true=test_labels, # ground truth test labels
                          y_pred=y_preds, # predicted labels
                          classes=class_names, # array of class label names
                          figsize=(15, 15),
                          text_size=10)
  """  
  # Create the confustion matrix
  cm = confusion_matrix(y_true, y_pred)
  cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] # normalize it
  

  # Plot the figure and make it pretty
  fig, ax = plt.subplots(figsize=figsize)
  cax = ax.matshow(cm, cmap=plt.cm.Greens) # colors will represent how 'correct' a class is, darker == better
  fig.colorbar(cax)

  # Are there a list of classes?
  if classes.any():
    labels = classes
    n_classes = len(labels) # find the number of classes we're dealing with
  else:
    labels = np.arange(cm.shape[0])
    n_classes = cm.shape[0] # find the number of classes we're dealing with
  
  # Label the axes
  ax.set(title="Confusion Matrix",
         xlabel="Predicted label",
         ylabel="True label",
         xticks=np.arange(n_classes), # create enough axis slots for each class
         yticks=np.arange(n_classes), 
         xticklabels=labels, # axes will labeled with class names (if they exist) or ints
         yticklabels=labels)
  
  # Make x-axis labels appear on bottom
  ax.xaxis.set_label_position("bottom")
  ax.xaxis.tick_bottom()

  # Set the threshold for different colors
  threshold = (cm.max() + cm.min()) / 2.
  print(f"Threashold : {threshold:.2f}\n")
  # Plot the text on each cell
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, f"{cm_norm[i, j]*100:.1f}% ({cm[i,j]})",
             horizontalalignment="center",
             color="white" if cm[i, j] >= threshold else "red",
             size=text_size)