import tensorflow as tf
from tensorflow import keras
from keras import metrics
import pandas as pd
import numpy as np
from tensorflow.keras import layers

#load data to train model from
Traindf = pd.read_csv("ishigami_training_data.txt", delim_whitespace=True, header = None)
data = Traindf.values

#split labels from train data
Y_train = data[:,3]
X_train = data[:,:3]

print(X_train.shape)
print(Y_train.shape)

#Regression FFNN build function
def build_ffnn(activation, nodes):
    tf.keras.backend.clear_session()
    #tf.random.set_seed(105545)
    #layers
    model = keras.Sequential([
        layers.Dense(nodes, activation=activation),
        layers.Dense(nodes, activation=activation),
        layers.Dense(1)
    ])
    #model compilation
    model.compile(loss='mean_squared_error',
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
                  metrics=["mean_squared_error"])


    return model

#load model with hyper-params
ffnn_model = build_ffnn("gelu", 80)

ffnn_model.fit(X_train,
               Y_train,
               epochs = 300,
               verbose = 1)

ffnn_model.summary()
mse = ffnn_model.evaluate(X_train, Y_train)[0]

#if accurate enough export model
if mse < 0.01:
    print("Exported Model!")
    ffnn_model.save("./exported_tfk_model.keras")
