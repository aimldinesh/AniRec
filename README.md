![MLOps](https://img.shields.io/badge/MLOps-Enabled-blue)
![Made With Python](https://img.shields.io/badge/Made%20with-Python%203.10-blue.svg)
![Deployed on GCP](https://img.shields.io/badge/Deployed-GCP-ff69b4)
![Comet ML](https://img.shields.io/badge/Experiment_Tracking-Comet--ML-orange)
![DVC](https://img.shields.io/badge/Data_Versioning-DVC-purple)
![CI/CD](https://img.shields.io/badge/CI/CD-Jenkins-yellow)
![Status](https://img.shields.io/badge/status-Deployed-brightgreen)
![Repo Size](https://img.shields.io/github/repo-size/aimldinesh/AniRec)
![Last Commit](https://img.shields.io/github/last-commit/aimldinesh/AniRec)
# 🎬 AniRec: Personalized Anime Recommendation System
AniRec is a full-scale end-to-end **Anime Recommendation System** that combines content-based filtering, collaborative filtering, and hybrid techniques. This project demonstrates the power of **MLOps**, incorporating tools like **Comet-ML**, **DVC**, **Jenkins**, **Docker**, and **Kubernetes** to deliver a scalable, reproducible, and production-grade recommendation system.

---
## 📑 Table of Contents
* [🧱 Project Architecture](#-project-architecture)
* [🚀 Key Features](#-key-features)
* [🛠️ Project Workflow](#️-project-workflow)
  * [1. 📦 Database Setup](#1--database-setup)
  * [2. ⚙️ Project Setup](#2--project-setup)
  * [3. 📥 Data Ingestion](#3--data-ingestion-via-gcp-bucket)
  * [4. 📒 Jupyter Notebook Testing](#4--jupyter-notebook-testing)
  * [5. 🧹 Data Processing](#5--data-processing)
  * [6. 🧠 Model Architecture](#6--model-architecture)
  * [7. 🎯 Model Training](#7--model-training)
  * [8. 📊 Experiment Tracking](#8--experiment-tracking)
  * [9. 🔁 Training Pipeline](#9--training-pipeline)
  * [10. 📦 Data & Code Versioning](#10--data--code-versioning)
  * [11. 🧩 Prediction Helper Functions](#11--prediction-helper-functions)
  * [12. 🌐 User App with Prediction Pipeline](#12--user-app-with-prediction-pipeline)
  * [13. 🚀 CI/CD Deployment](#13--cicd-deployment)
* [🧰 Tech Stack](#-tech-stack)
* [🧪 Local Setup Instructions](#-local-setup-instructions)
* [🌐 Run with Docker](#-run-with-docker)
* [📸 Project Screenshots](#-project-screenshots)
* [📦 Future Improvements](#-future-improvements)
* [📚 Datasets](#-datasets)
* [📄 License](#-license)
* [🤝 Contributors](#-contributors)

---
## 🧱 Project Architecture
```mermaid
graph TD
    A[📂 Database Setup<br>GCP Bucket] --> B[⚙️ Project Setup]
    B --> C[🛢️ Data Ingestion<br>via GCP]
    C --> D[📓 Jupyter Notebook Testing]
    D --> E[🧹 Data Processing]
    E --> F[🏗️ Model Architecture]
    F --> G[🧠 Model Training]
    G --> H[📊 Experiment Tracking<br>Comet-ML]
    H --> I[🚀 Training Pipeline]
    I --> J[📦 Data & Code Versioning<br>DVC + GitHub]
    J --> K[🌐 User App Flask<br>Prediction Pipeline]
    K --> L[⚙️ CI/CD with Jenkins & Kubernetes<br>Deployment on GCP]
```
---

## 🚀 Key Features

- 🔍 **Content-Based Filtering** using genres and synopsis embeddings
- 👥 **Collaborative Filtering** using user-anime interaction embeddings
- 🤝 **Hybrid Recommender** that combines both strategies
- 📊 **Experiment Tracking** using **Comet-ML**
- 📦 **Data and Model Versioning** using **DVC**
- 🔧 **CI/CD Pipeline** using **Jenkins + Kubernetes**
- 🌐 **Web App Interface** using **Flask**

---

## 🛠️ Project Workflow

### 1. 📦 Database Setup
- Centralized dataset storage using **Google Cloud Storage (GCP Bucket)**

### 2. ⚙️ Project Setup
- Structured codebase with modular components and dependencies

### 3. 📥 Data Ingestion (via GCP Bucket) 
- Raw datasets (`anime.csv`, `anime_with_synopsis.csv`, `animelist.csv`) stored in a Google Cloud Storage bucket.
- Ingested using Python scripts directly from GCS into the pipeline.

### 4. 📒 Jupyter Notebook Testing
- Conducted EDA, preprocessing, and recommendation logic development in notebooks.
- Tested multiple recommendation strategies:
    - Content-based filtering
    - Collaborative filtering
    - Hybrid approach

### 5. 🧹 Data Processing
- Cleaned anime metadata and user ratings.
- Merged multiple datasets (anime.csv, anime_with_synopsis.csv, animelist.csv).
- Extracted text features (synopsis) and encoded categorical features.

### 6. 🧠 Model Architecture
- Developed content-based, collaborative, and hybrid models

### 7. 🎯 Model Training  
- Trained machine learning models using anime-user interaction data to capture preferences and generate recommendations.
   - Implemented a **Collaborative Filtering** approach using cosine similarity on user-anime rating matrix.
   - Preprocessed the interaction matrix by filling missing values with zeros and normalizing scores.
   - Encoded anime and user IDs, then computed similarity-based embeddings.
   - Evaluated recommendation quality using **RMSE** and cosine similarity metrics.
   - Saved trained model artifacts and associated encoders for inference integration in the prediction pipeline.

### 8. 📊 Experiment Tracking
- Used **Comet-ML** for logging metrics, hyperparameters, and artifacts

### 9. 🔁 Training Pipeline
- Modular training pipeline to automate:
   - Data loading and preprocessing
   - Model training and saving
   - Logging artifacts and metrics

### 10. 📦 Data & Code Versioning
- Used DVC (Data Version Control) to version datasets and models.
- Managed code versions and CI logs with GitHub.

### 11. 🧩 Prediction Helper Functions
- Built reusable prediction utilities to:
   - Recommend anime by user ID
   - Recommend similar anime by name
   - Combine content + collaborative recommendations

### 12. 🌐 User App with Prediction Pipeline
- Developed a Flask web application to:
   - Accept user inputs (user_id)
   - Display personalized recommendations with titles and genres
   - Call backend prediction functions via HTTP

### 13. 🚀 CI/CD Deployment
- Built production-ready pipeline using:
   - Jenkins for automated CI/CD
   - Docker for containerization
   - Kubernetes on GCP for scalable deployment

---

## 🧰 Tech Stack

| Category              | Tools & Frameworks                                    |
|-----------------------|--------------------------------------------------------|
| Language              | Python                                                 |
| Data Storage          | GCP Bucket                                             |
| Web Framework         | Flask                                                  |
| Recommender Methods   | Collaborative Filtering, Content-Based, Hybrid        |
| Experiment Tracking   | Comet-ML                                               |
| Data Versioning       | DVC                                                    |
| Containerization      | Docker                                                 |
| Orchestration         | Kubernetes (Minikube / GKE)                            |
| CI/CD Pipeline        | Jenkins                                                |
| Deployment Platform   | Google Cloud Platform                                  |

---

## 🧪 Local Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/your-username/anirec.git
cd anirec

# 2. Create virtual environment & activate
python -m venv venv
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate     # for Windows

# 3. Install dependencies
pip install -e .

# 4. Run the Flask app
python app.py

```
---
## 🌐 Run with Docker
```
# Build the Docker image
docker build -t anirec-app .

# Run the container
docker run -p 5000:5000 anirec-app

```
---
## 📸 Project Screenshots

### 🚀 Jenkins CI/CD Pipeline Execution

<p float="left">
  <img src="https://github.com/aimldinesh/AniRec/blob/main/screenshots/Jenkins_CICD%20Pipeline%20_Execution/Jenkins_pipeline_build_start.PNG" width="350"/>
  <img src="https://github.com/aimldinesh/AniRec/blob/main/screenshots/Jenkins_CICD%20Pipeline%20_Execution/Jenkins_pipeline_build_success.PNG" width="350"/>
</p>

---

### ☁️ AniRec Web App Running on GCP

<p float="left">
  <img src="https://github.com/aimldinesh/AniRec/blob/main/screenshots/AniRec%20_Web%20App%20_Running%20_on%20_GCP/AniRec_Web_App_Running_on%20_GCP_Active%20revisions_Managed%20pods_Exposing%20services.png" width="700"/>
</p>

---

### 🎨 AniRec Web App UI

<p float="left">
  <img src="https://github.com/aimldinesh/AniRec/blob/main/screenshots/App_ui/deploy_app_ui_using_gcp_1.PNG" width="350"/>
  <img src="https://github.com/aimldinesh/AniRec/blob/main/screenshots/App_ui/deploy_app_ui_using_gcp_2.png" width="350"/>
</p>

---

## 📦 Future Improvements
- Integrate user login and personalized dashboards.
- Incorporate NLP-based synopsis analysis for improved content similarity.
- Use embeddings from models like BERT or Sentence Transformers.
- Deploy with auto-scaling via GKE Ingress and HPA.

---
## 📚 Datasets
* [Anime Data](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020)

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributors
- [Dinesh Chaudhary](https://github.com/aimldinesh)
