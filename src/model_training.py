import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

# Load processed data
df = pd.read_csv("data/processed_dataset.csv")
X = df.drop(columns=["species"])
y = df["species"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate Model
accuracy = model.score(X_test, y_test)
print(f" Model trained with accuracy: {accuracy}")

# Prepare input example
input_example = np.array(X_test.iloc[0]).reshape(1, -1)
signature = infer_signature(X_test, model.predict(X_test))

# Start MLflow Experiment
mlflow.set_experiment("MLOps-Pipeline")

with mlflow.start_run() as run:
    # Log Model with input example and signature
    mlflow.sklearn.log_model(
        sk_model=model, 
        artifact_path="model",
        input_example=input_example,
        signature=signature
    )
    
    # Log Accuracy Metric
    mlflow.log_metric("accuracy", accuracy)

    # Get the run ID
    run_id = run.info.run_id

# Register Model in MLflow Model Registry
model_uri = f"runs:/{run_id}/model"
model_version = mlflow.register_model(model_uri=model_uri, name="RandomForestModel")

print(f"✅ Model registered with name: 'RandomForestModel' and version: {model_version.version}")
