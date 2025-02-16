import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import requests


# Load New Data (New or Updated Dataset)
df = pd.read_csv("data/new_data.csv")

# Load Fixed Test Dataset
test_df = pd.read_csv("data/test_dataset.csv")

# **Remove Overlapping Data** (Avoid Data Leakage) 
# and splitting the data 
train_df = df[~df.isin(test_df)].dropna()

X_train = train_df.drop(columns=["species"])
y_train = train_df["species"]

X_test = test_df.drop(columns=["species"])
y_test = test_df["species"]


# Load Existing Model from MLflow
prev_model = mlflow.sklearn.load_model("models:/RandomForestModel/latest")

# Start MLflow Experiment for Retraining
mlflow.set_experiment("MLOps-Pipeline")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    new_accuracy = model.score(X_test, y_test)
    prev_accuracy = prev_model.score(X_test, y_test)

    print(f" Previous Accuracy: {prev_accuracy}, New Accuracy: {new_accuracy}")

    if new_accuracy > prev_accuracy:
        print(" New model performs better! Updating.and Registering it ..")
        mlflow.log_metric("accuracy", new_accuracy)
        mlflow.sklearn.log_model(model, "random_forest_model")
        # Register the new model in the MLflow Model Registry in the same name as the previous model
        run_id = run.info.run_id
        model_uri = f"runs:/{run_id}/model"
        mlflow.register_model(model_uri=model_uri, name="RandomForestModel")
        print(" New model registered in MLflow Model Registry.")
    else:
        print("❌ New model did not improve performance. Keeping the old model.")

print("✅ Model retraining process completed.")
