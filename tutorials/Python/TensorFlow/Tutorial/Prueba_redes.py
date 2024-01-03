import numpy as np
import tensorflow as tf
#import matplotlib.pyplot as plt
import pandas as pd
print (tf.__version__)

#Load data from Redes.csv
data = pd.read_csv(r'Redes.csv')
data_trial = data[data.columns[0:18]]
data_trial.rename({'ego/origin':'ego_origin','ego/residence':'ego_residence'}, axis='columns',inplace = True)
data_trial['ego_origin'] = pd.Categorical(data_trial['ego_origin'])
data_trial['ego_origin'] = data_trial.ego_origin.cat.codes
data_trial['ego_residence'] = pd.Categorical(data_trial['ego_residence'])
data_trial['ego_residence'] = data_trial.ego_residence.cat.codes
data_trial['Regime'] = pd.Categorical(data_trial['Regime'])
data_trial['Regime'] = data_trial.Regime.cat.codes

target = data_trial.pop('ego_origin')
dataset = tf.data.Dataset.from_tensor_slices((data_trial.values, target.values))
train_dataset = dataset.shuffle(len(data_trial)).batch(1)


#Convert to one_hot_encoding
#df = pd.get_dummies(data = data_trial, columns = ['ego/origin','ego/residence','Regime'])
#y_data = np.array(df[df.columns[15:25]], dtype = 'float32')
#df.drop(df.columns[15:25], axis=1, inplace=True)
#x_data = np.array(df, dtype = 'float32')
#print(data_trial.columns)
#y_data = np.array(pd.get_dummies(data_trial['ego/origin']),dtype = 'float32')
#x_data = np.array(data_trial[data_trial.columns[3:]],dtype = 'float32')
#nb_classes = len(y_data[0])
#nx_classes = len(x_data[0])

def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(1000, activation='relu'),
    tf.keras.layers.Dense(1000, activation='relu'),
    tf.keras.layers.Dense(1000, activation='relu'),
    tf.keras.layers.Dense(1,activation = 'softmax')
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
  return model

model = get_compiled_model()
model.fit(train_dataset, epochs=10)

