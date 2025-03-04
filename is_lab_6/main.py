#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image

def main():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32') / 255.0
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32') / 255.0

    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    model = Sequential([
        Flatten(input_shape=(28, 28, 1)),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    print("Начинаем обучение модели...")
    model.fit(
        x_train, y_train,
        epochs=5,
        batch_size=32,
        validation_split=0.2
    )

    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"\nТочность на тестовых данных MNIST: {test_acc:.4f}")
    
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        img_path = r"1.png"

    def prepare_image(path):
        img = image.load_img(path, target_size=(28, 28), color_mode='grayscale')
        img_arr = image.img_to_array(img)
        img_arr = np.expand_dims(img_arr, axis=0)
        img_arr = 1.0 - img_arr / 255.0

        return img_arr

    try:
        custom_img = prepare_image(img_path)
        prediction = model.predict(custom_img)
        predicted_class = np.argmax(prediction, axis=1)[0]
        print(f"\nПуть к изображению: {img_path}")
        print(f"Распознанная сетью цифра: {predicted_class}")

        plt.imshow(custom_img.reshape(28, 28), cmap='gray')
        plt.title(f'Распознанная цифра: {predicted_class}')
        plt.axis('off')
        plt.show()
    except Exception as e:
        print("\nОшибка при загрузке и распознавании изображения!")
        print(e)

if __name__ == "__main__":
    main()
