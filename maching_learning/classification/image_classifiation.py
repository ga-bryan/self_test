#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/23
@des:   机遇keras的图像分类
"""

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

# 使用keras的图片数据集，28*28大小的numpy数组像素值介于0~255
fashion_mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 预处理数据
## 查看数据
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid()
plt.show()

## 将数据处理成0~1之间的数
train_images, test_images = train_images / 255.0, test_images / 255.0

## 验证数据格式是否正确并显示图片分类
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

# 构建模型
model = keras.Sequential(
    [
        # 展平层
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation="relu"),
        # 10个类别的输出
        keras.layers.Dense(10)
    ]
)

# 编译模型
model.compile(
    optimizer="adam",
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"]
)

# 训练
model.fit(train_images, train_labels, epochs=10)

# 评估
# test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
test_loss, test_acc = model.evaluate(test_images, test_labels)

# 预测
probability_model = keras.Sequential([model, keras.layers.Softmax()])
predictions = probability_model.predict(test_images)
