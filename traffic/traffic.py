import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):

    images = []
    labels = []

    for subcat in range(NUM_CATEGORIES):
        path = os.path.join(data_dir, str(subcat))
        for category in os.listdir(path):
            image = cv2.imread(os.path.join(path, category))
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            images.append(image)
            labels.append(subcat)
    return images, labels


def get_model():
    model = tf.keras.models.Sequential([

        # 2xConvolutional layer, 32 filters, 3x3 kernel
        tf.keras.layers.Conv2D(
            32,  (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        tf.keras.layers.Conv2D(
            32,  (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        # Max-pooling layer, using 3x3 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # 256 units took 237 seconds to run with 97.32 accuracy
        # 128 units took 165 seconds to run with 97.38 accuracy
        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.25),

        # Add another hidden layer with dropout
        # tf.keras.layers.Dense(128, activation="relu"),
        # tf.keras.layers.Dropout(0.25),

        # Add Dense Output layer with 43 output units
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Return model for training and testing
    return model


if __name__ == "__main__":
    main()
