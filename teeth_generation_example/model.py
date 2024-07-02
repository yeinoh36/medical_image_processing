from stl import mesh
import pyvista as pv
import trimesh
import pandas as pd
import random
import itertools
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from pytictoc import TicToc

# TicToc 클래스 생성
t = TicToc()

data_set1 = np.load('./ground_truth_crown_dataset.npy',allow_pickle=True)
data_set2 = np.load('./ground_truth_frap_normal_crown_dataset.npy',allow_pickle=True)
data_set3 = np.load('./ground_truth_frap_normal_dataset.npy',allow_pickle=True)

#check dataset size
#print(data_set1.shape)
#print(data_set2.shape)
#print(data_set3.shape)

#check dataset size
print(data_set1.shape)
print(data_set2.shape)
print(data_set3.shape)

#data_set1=data_set1.reshape(373,373,3)
#data_set2= data_set2.reshape(373,1119,3)
#data_set3= data_set3.reshape(373,746,3)


#373=373*1
#373=373*3
#746=373*2

#data_set1=data_set1.reshape(373,373,1,3)
#data_set2= data_set2.reshape(373,373,3,3)
#data_set3= data_set3.reshape(373,373,2,3)
#data_set2 = data_set2.reshape(373,373*3,3)

print('cchheecckkk')
#check dataset size
print(data_set1.shape)
print(data_set2.shape)
print(data_set3.shape)

#print(data_set2[0].shape)

'''
Reference :
https://github.com/kdj842969/3D-Autoencoder
'''
from time import time
import tensorflow as tf
from tensorflow import keras

import tensorflow_addons as tfa
import os
import numpy as np
import csv

from keras.layers import Input
from keras.models import Model
from keras.layers.convolutional import Convolution2D, MaxPooling2D, UpSampling2D
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
from keras import backend as K

K.clear_session()

train = data_set3
train_label = data_set2

input_shape=(3,1)
n_classes= 3
epochs = 10

#Transformer 모델에 들어가는 encoder 첫번째
def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
    # Attention and Normalization
    x = keras.layers.MultiHeadAttention(
        key_dim=head_size, num_heads=num_heads, dropout=dropout
    )(inputs, inputs)
    print(x)
    x = keras.layers.Dropout(dropout)(x)
    x1 = keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x2 = tfa.layers.InstanceNormalization()(x)
    x= (0.7*x1)+(0.3*x2)
    res = x + inputs

    # Feed Forward Part
    x = keras.layers.Conv1D(filters=ff_dim, kernel_size=1, activation="LeakyReLU")(res)
    x1 = keras.layers.Dropout(dropout)(x)
    x = keras.layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    x1 = keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x2 = tfa.layers.InstanceNormalization()(x)
    x = (0.7*x1)+(0.3*x2)
    return x + res

#Transformer 모델에 들어가는 encoder 두번째
def transformer_encoder2(inputs, head_size, num_heads, ff_dim, dropout=0):
    # Attention and Normalization
    x = keras.layers.MultiHeadAttention(
        key_dim=head_size, num_heads=num_heads, dropout=dropout
    )(inputs, inputs)

    x = keras.layers.Dropout(dropout)(x)
    x1 = keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x2 = tfa.layers.InstanceNormalization()(x)
    x= (0.7*x1)+(0.3*x2)
    res = x + inputs

    # Feed Forward Part
    x = keras.layers.Conv1D(filters=ff_dim, kernel_size=1, activation="LeakyReLU")(res)
    x1 = keras.layers.Dropout(dropout)(x)
    x = keras.layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    x1 = keras.layers.LayerNormalization(epsilon=1e-6)(x)
    x2 = tfa.layers.InstanceNormalization()(x)
    x = (0.7*x1)+(0.3*x2)
    return x + res


#Transformer 모델 설계 부분
def build_model(
    input_shape,
    head_size,
    num_heads,
    ff_dim,
    num_transformer_blocks,
    mlp_units,
    dropout=0,
    mlp_dropout=0,
):
    print(head_size)
    print(num_heads)
    print(ff_dim)
    inputs = keras.Input(shape=input_shape)
    x = inputs

    for _ in range(num_transformer_blocks):
        x1 = transformer_encoder(x, head_size, num_heads, ff_dim, dropout)
    print(x)
    for _ in range(num_transformer_blocks):
        x2 = transformer_encoder2(x, head_size, num_heads, ff_dim, dropout)
    print(x2)
    x = (0.5*x1) + (0.5*x2)
    x = keras.layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    for dim in mlp_units:
        x = keras.layers.Dense(dim, activation="LeakyReLU")(x)
        x = keras.layers.Dropout(mlp_dropout)(x)
    outputs = keras.layers.Dense(n_classes)(x)
    return keras.Model(inputs, outputs)

#모델 학습 부분
model = build_model(
    input_shape,
    head_size=256,
    num_heads=4,
    ff_dim=4,
    num_transformer_blocks=2,
    mlp_units=[128],
    mlp_dropout=0.4,
    dropout=0.25,
)

opt2 = tf.keras.optimizers.Nadam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, name="Nadam")
opt2 = tf.keras.mixed_precision.LossScaleOptimizer(opt2)

model.compile(optimizer = opt2, loss = tf.keras.losses.MeanAbsolutePercentageError(),metrics=[tf.keras.metrics.MeanSquaredError(),tf.keras.metrics.CosineSimilarity(),tf.keras.metrics.MeanAbsolutePercentageError(),tf.keras.metrics.RootMeanSquaredError(),tf.keras.metrics.LogCoshError()])
model.summary()

path_checkpoint = "teeth.h5"
es_callback = keras.callbacks.EarlyStopping(monitor="val_loss", min_delta=0, patience=5)

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=True,
    save_best_only=True,
)


history = model.fit(
    train,
    train_label,
    epochs=epochs)

#모델 save 부분
model.save(path_checkpoint)

print("Training finished...")


#Model inference 부분

t.tic() # 시작 시간
 
model_predict=[]
print(len(data_set3))
#for i in range(0,len(test_data)):
for i in range(0,len(data_set3)):
  print('test data inference'+str(i))
  test_data_batch= data_set3
  # 모델 재평가
  predict_value = model.predict(test_data_batch)
  predict_data = predict_value[i]
  print(predict_data)
  model_predict.append(predict_data)

np.save('./model_predict_result.npy',model_predict)

import csv
f = open('model_predict_result.csv','w')
writer = csv.writer(f)
writer.writerows(model_predict)
f.close()

t.toc() # 종료 시간
print("Testing finished...")



