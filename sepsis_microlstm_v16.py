import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# 1. Load the training data
X_train = np.load('X_train.npy')  # shape: (num_samples, time_steps, num_features)
y_train = np.load('y_train.npy')  # shape: (num_samples,)

# 2. Sample 1% of the data
sample_size = int(X_train.shape[0] * 0.01)  # 1% of the total data size
indices = np.random.choice(X_train.shape[0], size=sample_size, replace=False)

# 3. Apply the sampling to the data
X_train_sampled = X_train[indices]
y_train_sampled = y_train[indices]

# 4. Build the Micro-LSTM model
model = Sequential()

# LSTM layer - use a small number of units for a lightweight model
model.add(LSTM(32, activation='relu', input_shape=(X_train_sampled.shape[1], X_train_sampled.shape[2]), return_sequences=False))

# Dropout layer to prevent overfitting (can be adjusted based on performance)
model.add(Dropout(0.2))

# Dense output layer for binary classification (can be changed if you have more classes)
model.add(Dense(1, activation='sigmoid'))

# 5. Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# 6. Train the model with the 1% sampled data
model.fit(X_train_sampled, y_train_sampled, epochs=10, batch_size=32, validation_split=0.2)

# Optionally, save the model
model.save('microlstm_sepsis_model_sampled.h5')
