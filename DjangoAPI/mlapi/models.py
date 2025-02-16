from django.db import models

# Create your models here.
from django.db import models

class Prediction(models.Model):
    input_features = models.JSONField()  # Store input features as JSON
    prediction = models.FloatField()     # Store prediction result
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for logging

    def __str__(self):
        return f"Prediction {self.id}: {self.prediction}"
