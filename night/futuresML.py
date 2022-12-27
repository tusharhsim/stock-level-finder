import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('night_futures.csv')

train_dataset = df.sample(frac=0.5, random_state=0)
test_dataset = df.drop(train_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('Nifty50')
test_labels = test_features.pop('Nifty50')

devil = train_dataset.describe().T
mean = devil['mean']
std = devil['std']

def normalize(data):
    data = (data-mean)/std

normalize(train_features)
normalize(test_features)


model = tf.keras.Sequential([
    #tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    #tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(64, activation='relu'),
    #tf.keras.layers.Dropout(0.4),
    #tf.keras.layers.Dense(32, activation='relu'),
    #tf.keras.layers.Dropout(0.2),
    #tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
    ])

model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
              loss='mean_absolute_error')

history = model.fit(
    train_features, train_labels,
    validation_split=0.2,
    verbose=2, epochs=40)

model.summary()
model.evaluate(test_features, test_labels, verbose=2)

'''
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
'''

print('model pedction ', model.predict(test_features))
print('real data ', test_labels)
