# 🚀 RetentionAI: Employee Churn Prediction System

**RetentionAI** is a full-stack machine learning application developed to help HR departments identify employees at risk of leaving. This project uses a **Monorepo** structure, containerized with Docker for easy setup and deployment.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
* **Backend:** FastAPI (Python 3.11)
* **Machine Learning:** Scikit-learn, Imbalanced-learn (SMOTE), Pandas, Joblib
* **Database:** PostgreSQL 15
* **DevOps:** Docker, Docker Compose, Ubuntu 24.04 LTS

---

## 📁 Project Structure

RetentionAI/
├── backend/            # FastAPI, ML Models, and Database Logic
│   ├── app/            # Main application code
│   ├── ml/             # Trained .joblib models
│   └── requirements.txt # Python dependencies (v1.2.2 Scikit-learn)
├── frontend/           # UI Files (HTML/CSS/JS)
├── docker-compose.yml  # Orchestration for the whole stack
└── README.md

---

## 🚀 Getting Started (Docker)

To run the entire application (Database, API, and Frontend) on your local machine, follow these steps:

1. Clone the repository
git clone https://github.com/chaimoma/RetentionAiFullstack.git
cd RetentionAiFullstack

2. Configure Environment Variables
Create a .env file in the backend/ directory with your database credentials. Ensure they match the settings in docker-compose.yml.

3. Launch the Stack
Run the following command to build and start all containers:
docker-compose up --build

---

## 🔗 Access Points

Once the containers are running, you can access the services at:

* Frontend UI: http://localhost:5501
* API Documentation (Swagger): http://localhost:8082/docs
* Database Port: 5433 (External mapping)

---

## 🤖 Machine Learning Highlights

This project addresses the class imbalance problem common in HR data using SMOTE-ENN techniques. The model is built with scikit-learn (v1.2.2) to ensure compatibility and high-performance predictions.

Developed by **Chaima Zbairi** as part of the **Développement AI** curriculum at Simplon Academy.
