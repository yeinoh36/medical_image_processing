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
from open3d import *

'''

file_name=[]
file_name2=[]
ground_truth =[]
ground_truth_crown=[]
ground_truth_frap=[]

ground_truth_data =[]
ground_truth_crown_data=[]
ground_truth_frap_data=[]

ground_truth_crown_label=[]
ground_truth_ground_truth_label=[]
ground_truth_frap_data_label=[]


def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        #print(full_filename)
        file_name.append(full_filename)

search('./normal_373ea/')

def search2(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        #print(full_filename)
        file_name2.append(full_filename)

for i in range(0,len(file_name)):
    search2(file_name[i])

#print(file_name2[0])
print(len(file_name2))


for i in range(0,len(file_name2)):
    file_path=file_name2[i].split('/')
    dd=file_path[2].split('\\')
    dd=dd[1].split('.')
    #print(dd)
    ff=dd[0].split(' ')
    try:
        #print(ff[1])
        if ff[1] =='0':
            print('c')
            ground_truth_crown.append(file_name2[i])
    except:
        pass
    
    if dd[0] == 'antagonist_reduce':
       ground_truth.append(file_name2[i])
       print('a')
    elif dd[0]== 'preparation_reduce':
       print('m')
       ground_truth_frap.append(file_name2[i])
    
print(len(ground_truth))
print(len(ground_truth_frap))
print(len(ground_truth_crown))


ground_truth_pv=[]
ground_truth_ground_truth_label_no_conversion=[]
ground_truth_points=[]

data_set1=[]
data_set2=[]
data_set3=[]
data_set4=[]

#Frap + Normal  
for i in range(0,100):
    print('Frap normal')
    tri_mesh = trimesh.load(ground_truth[i]) # base.Trimesh
    tri_mesh2 = trimesh.load(ground_truth_frap[i])
    
    for i in range(0,150):
        data_set1.append([tri_mesh.vertices[i][0],tri_mesh.vertices[i][1],tri_mesh.vertices[i][2]])
    for i in range(0,150):
        data_set1.append([tri_mesh2.vertices[i][0],tri_mesh2.vertices[i][1],tri_mesh2.vertices[i][2]])

np.save('./ground_truth_frap_normal_dataset.npy',data_set1)

mdic ={'ground_truth_frap_normal_dataset':np.array(data_set1),"label":"ground_truth_frap_normal_dataset"}
scipy.io.savemat('./ground_truth_frap_normal_dataset.mat',mdic)

#Crown
for i in range(0,300):
    print('crown')
    tri_mesh3 = trimesh.load(ground_truth_crown[i])
    for i in range(0,len(ground_truth_frap)):
        data_set2.append([tri_mesh3.vertices[i][0],tri_mesh3.vertices[i][1],tri_mesh3.vertices[i][2]])

    #tri_mesh3=uniform_down_sample(data_set3, 2000)
    
np.save('./ground_truth_crown_dataset.npy',data_set2)

mdic2 ={'ground_truth_crown_dataset':np.array(data_set2),"label":"ground_truth_crown_dataset"}
scipy.io.savemat('./ground_truth_crown_dataset.mat',mdic2)

#Frap+Normal+Crown
for i in range(0,100):
    print('Frap normal crown')
    tri_mesh = trimesh.load(ground_truth[i]) # base.Trimesh
    tri_mesh2 = trimesh.load(ground_truth_frap[i])
    tri_mesh3 = trimesh.load(ground_truth_crown[i])

    for i in range(0,100):
        data_set3.append([tri_mesh.vertices[i][0],tri_mesh.vertices[i][1],tri_mesh.vertices[i][2]])
    for i in range(0,100):
        data_set3.append([tri_mesh2.vertices[i][0],tri_mesh2.vertices[i][1],tri_mesh2.vertices[i][2]])
    for i in range(0,100):
        data_set3.append([tri_mesh3.vertices[i][0],tri_mesh3.vertices[i][1],tri_mesh3.vertices[i][2]])


np.save('./ground_truth_frap_normal_crown_dataset.npy',data_set3)
mdic3 ={'ground_truth_frap_normal_crown_dataset':np.array(data_set3),"label":"ground_truth_frap_normal_crown_dataset"}
scipy.io.savemat('./ground_truth_frap_normal_crown_dataset.mat',mdic3)
'''
print('finish preparing dataset')

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
