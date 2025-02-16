from django.shortcuts import render
import json
import numpy as np
import mlflow.sklearn
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Prediction

#  Set MLflow tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Define model URI
MODEL_URI = "models:/RandomForestModel/latest"

model = None

def load_model():
    """ Load the latest MLflow model if available, else handle first-time startup gracefully """
    global model
    try:
        model = mlflow.sklearn.load_model(MODEL_URI)
        print(" Model loaded successfully!")
    except Exception as e:
        print(f" No model found in MLflow. Waiting for first training. Error: {e}")
        model = None  # Keep model as None until first training completes

# ✅ Load the model at startup
load_model()

@api_view(["POST"])
def predict(request):
    """ Make predictions using the latest loaded model """
    try:
        if model is None:
            return JsonResponse({"error": "No model available. Train a model first!"}, status=500)

        # Parse input JSON
        data = json.loads(request.body)
        features = np.array(data["features"]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)[0]

        # ✅ Store prediction in the database
        Prediction.objects.create(input_features=data["features"], prediction=prediction)

        return JsonResponse({"prediction": prediction})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(["POST"])
def deploy_model(request):
    """ API endpoint to reload the latest MLflow model after retraining """
    try:
        global model
        model = mlflow.sklearn.load_model(MODEL_URI)  # ✅ Force model reload
        print(" Model reloaded successfully!")
        return JsonResponse({"status": "success", "message": "Model reloaded successfully!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
