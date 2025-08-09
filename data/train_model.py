import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# Load your labeled dataset (replace with your actual file)
data = pd.read_csv('reading_data.csv')

# Features & labels (adjust column names)
X = data[['feature1', 'feature2', 'feature3']].values  # example features
y = data['label'].values  # binary label: 0 (no dyslexia), 1 (dyslexia)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build a simple neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

# Save the model for inference in Flask backend
model.save('dyslexia_detection_model.h5')

# Save scaler for later use (optional)
import joblib
joblib.dump(scaler, 'scaler.save')

print("Model training complete and saved.")