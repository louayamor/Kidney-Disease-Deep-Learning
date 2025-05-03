# 🧠 Kidney Disease Classification using Deep Learning

This project uses a Convolutional Neural Network (CNN) to identify whether a kidney is diseased or healthy based on medical images. The training pipeline is built using Python and integrates with **MLflow** for experiment tracking.

---

## 📂 Project Structure

```
kidney-disease-classification/
├── data/                 # Image dataset
├── models/               # Saved trained models
├── researchs/            # Jupyter notebooks for EDA and prototyping
├── src/                  # Source code: data loading, training, evaluation
│   ├── data_utils.py
│   ├── model.py
│   └── train.py
├── main.py               # Main training script
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- 🔍 Image classification of kidney disease using CNNs  
- 📊 Real-time experiment tracking and metrics logging with **MLflow**  
- 📁 Organized project structure for scalability  
- 🧪 Easily extendable for hyperparameter tuning and model experimentation  

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kidney-disease-classification.git
   cd kidney-disease-classification
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 📈 MLflow Tracking

We use [MLflow](https://mlflow.org/) to track experiments, parameters, metrics, and artifacts.

### Launch MLflow UI locally:

```bash
mlflow ui
```

### Or use DAGsHub for online tracking:

[🔗 DAGsHub Project Page](https://dagshub.com/louayamor/Kidney-Disease-Deep-Learning.mlflow/)

Set environment variables for DAGsHub MLflow integration:

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/louayamor/Kidney-Disease-Deep-Learning.mlflow/
export MLFLOW_TRACKING_USERNAME=louayamor
export MLFLOW_TRACKING_PASSWORD=
```

---

## 🧠 Model Summary

- **Architecture:** Convolutional Neural Networks (CNNs)  
- **Input:** Preprocessed medical kidney images  
- **Output:** Binary classification — Healthy or Diseased  

---

## 👨‍🔬 Author

**Louay Amor**  
🔗 [LinkedIn](https://www.linkedin.com/in/louayamor)

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for more details.
