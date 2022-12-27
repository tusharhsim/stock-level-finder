import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

df = pd.read_csv('ohlc.csv', index_col=None)
df['change'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
df = df.drop(columns = ['open', 'high', 'low', 'close'])
print(df.head())
print()

df.change = df.change.pct_change()*100
df = df.fillna(0)
print(df.head())
print()
labels = df['change'].copy()

train_features = df[:int(0.7*len(df))]
test_features = df.drop(train_features.index)

labels.drop(0, inplace = True)
labels.loc[len(labels)+1] = 0
train_labels = labels[:int(0.7*len(labels))]
test_labels = labels.drop(train_labels.index)

devil = train_features.describe().T
mean = devil['mean']
std = devil['std']

def normalize(data):
    data = (data-mean)/std

normalize(train_features)
normalize(test_features)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.4),
    #tf.keras.layers.Dense(64, activation='relu'),
    #tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(32, activation='relu'),
    #tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
    ])

model.compile(optimizer=tf.keras.optimizers.Adam(0.1),
              loss='mse',
              metrics=['accuracy'])

history = model.fit(
    train_features, train_labels,
    verbose=2, epochs=100, validation_split=0.2)

print(pd.DataFrame(history.history))
model.summary()
model.evaluate(test_features, test_features, verbose=2)

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, label='Training loss')
plt.plot(epochs, val_loss, label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

print(model.predict(test_features[:11]))
print(test_labels[:11])

