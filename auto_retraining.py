from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Define DAG arguments
default_args = {
    'owner': 'mlops_team',
    'start_date': datetime(2025, 2, 15),
}

dag = DAG(
    "mlops_retraining_pipeline",
    default_args=default_args,
    schedule_interval=None,  # Manually triggered
)

# Task 1: Run Drift Detection
def detect_drift():
    subprocess.run(["python", "src/drift_detection.py"], check=True)

detect_drift_task = PythonOperator(
    task_id="detect_drift",
    python_callable=detect_drift,
    dag=dag,
)

#  Task 2: Retrain & Evaluate
def retrain_evaluate():
    subprocess.run(["python", "src/model_retraining_evaluating.py"], check=True)

retrain_evaluate_task = PythonOperator(
    task_id="retrain_evaluate",
    python_callable=retrain_evaluate,
    dag=dag,
)

# Task 3: Deploy Model
def deploy_model():
    subprocess.run(["python", "src/trigger_deployment.py"], check=True)

deploy_model_task = PythonOperator(
    task_id="deploy_model",
    python_callable=deploy_model,
    dag=dag,
)

#  Define Task Dependencies
detect_drift_task >> retrain_evaluate_task >> deploy_model_task
