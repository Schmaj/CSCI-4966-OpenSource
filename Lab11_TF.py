from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import ImageOps

def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

print(tf.__version__)
fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
train_images = train_images / 255.0

test_images = test_images / 255.0
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5)
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)
predictions = model.predict(test_images)
# Plot the first X test images, their predicted label, and the true label
# Color correct predictions in blue, incorrect predictions in red
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i+9000, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i+9000, predictions, test_labels)
plt.show()

im0 = PIL.Image.open("TFtest.png")
im1 = PIL.Image.open("TFtest2.png")
im2 = PIL.Image.open("TFtest3.png")
im0 = im0.resize((28, 28))
im1 = im1.resize((28, 28))
im2 = im2.resize((28, 28))
im0 = im0.convert('L')
im1 = im1.convert('L')
im2 = im2.convert('L')
im0 = PIL.ImageOps.invert(im0)
im1 = PIL.ImageOps.invert(im1)
im2 = PIL.ImageOps.invert(im2)
np_im0 = np.array(im0) / 255.0
np_im1 = np.array(im1) / 255.0
np_im2 = np.array(im2) / 255.0
im0 = (np.expand_dims(np_im0, 0))
im1 = (np.expand_dims(np_im1, 0))
im2 = (np.expand_dims(np_im2, 0))

prediction_im0 = model.predict(im0)
print(prediction_im0)
plot_value_array(0, prediction_im0, test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)
plt.show()
print("")

prediction_im1 = model.predict(im1)
print(prediction_im1)
plot_value_array(0, prediction_im1, test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)
plt.show()
print("")

prediction_im2 = model.predict(im2)
print(prediction_im2)
plot_value_array(0, prediction_im2, test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)
plt.show()
print("")
