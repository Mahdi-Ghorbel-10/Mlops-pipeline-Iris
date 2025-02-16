# MLOps Pipeline with DVC & Git

## 🚀 Project Overview
This project demonstrates an **MLOps workflow** using **DVC (Data Version Control) and Git** to track datasets, ensuring reproducibility.

## 👤 Authors
- **Your Name** - MLOps Engineer

## 📂 Project Structure
```
📂 mlops-project/
 ┣ 📂 data/  # Stores datasets (Tracked with DVC)
 ┃ ┣ 📄 raw_dataset.csv.dvc  # DVC metadata file
 ┃ ┣ 📄 processed_dataset.csv  # Processed dataset
 ┣ 📂 src/  # Scripts for processing & training
 ┃ ┣ 📄 data_processing.py  # Data preprocessing
 ┃ ┣ 📄 train_model.py  # Model training
 ┃ ┣ 📄 drift_detection.py  # Drift detection
 ┃ ┗ 📄 evaluate_deploy.py  # Model evaluation
 ┣ 📄 .dvc  # DVC config file
 ┣ 📄 auto_retraining.py  # Airflow DAG for automation
 ┣ 📄 Jenkinsfile  # CI/CD pipeline script
 ┣ 📄 requirements.txt  # Dependencies
 ┗ 📄 README.md  # Project Documentation
```

## ✅ Features
- **Data Versioning with DVC** 🗂️
- **Experiment Tracking with MLflow** 📊
- **Drift Detection with Evidently AI** 🔎
- **Auto-Retraining with Apache Airflow** 🔄
- **Model Deployment with BentoML** 🚀
- **CI/CD Automation with Jenkins** 🛠

## 🛠 Setup Instructions

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize Git & DVC
```bash
git init
dvc init
```

### 3️⃣ Track Dataset with DVC
```bash
dvc add data/raw_dataset.csv
git add data/.gitignore data/raw_dataset.csv.dvc
git commit -m "Added dataset tracking with DVC"
dvc push
```

### 4️⃣ Train the Model
```bash
python src/train_model.py
```

### 5️⃣ Detect Drift & Retrain if Needed
```bash
python src/drift_detection.py
```

### 6️⃣ Serve Model with BentoML
```bash
bentoml serve src/predict_service.py:svc --port 3000
```

## 📁 Remote Storage (Optional)
To use a cloud storage like AWS S3 or Google Cloud Storage for dataset versioning:
```bash
dvc remote add myremote s3://your-bucket-name
dvc push
```

## 🐝 Contributing
Feel free to contribute by submitting a pull request!

## 📝 License
This project is licensed under the MIT License.

