from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# Config for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define DB model for storing prediction results
class PredictionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    features = db.Column(db.Text)  # Store JSON serialized features as string
    result = db.Column(db.Float)

# Create DB tables
@app.before_first_request
def create_tables():
    db.create_all()

# Load your pre-trained TensorFlow model
MODEL_PATH = 'dyslexia_detection_model.h5'
if not os.path.exists(MODEL_PATH):
    raise Exception(f"Model file {MODEL_PATH} not found. Train and save your model first.")
model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = np.array(data['features'])

        # Reshape or preprocess features as per your model input requirements
        features = features.reshape(1, -1)

        prediction = model.predict(features)
        dyslexia_prob = float(prediction[0][0])  # Assuming binary classification with probability output

        # Save prediction and features to DB
        record = PredictionResult(features=str(features.tolist()), result=dyslexia_prob)
        db.session.add(record)
        db.session.commit()

        return jsonify({'dyslexia_probability': dyslexia_prob})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)