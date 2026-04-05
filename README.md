# Forest Fire Predictor

Machine Learning Project for predicting Algerian Forest Fires and Fire Weather Index (FWI)

[**Explore the Repo**](https://github.com/Asoomkamel/forest-fire-prediction) ·
[**View Flask App Code**](https://github.com/Asoomkamel/forest-fire-prediction/blob/main/app.py) ·
[**Model Building**](https://github.com/Asoomkamel/forest-fire-prediction/blob/main/notebook/) ·
[**EDA Notebook**](https://github.com/Asoomkamel/forest-fire-prediction/blob/main/notebook/)

---

## About The Project

This project uses **Data Science** and **Machine Learning** to build a model that predicts forest fires based on weather reports. The model learns from historical fire data to detect future fire occurrences.

### Key Features

- **Binary Classification**: Predicts fire occurrence (`fire` vs `not fire`)
- **Regression**: Predicts Fire Weather Index (FWI), which is 90%+ correlated to fire occurrence
- **Data Pipeline**: Loads CSV data, stores in **PostgreSQL** database
- **Web Interface**: Flask-based web application for real-time predictions
- **Cloud Deployment**: Hosted on cloud platform

### Deployed App

> **[LINK TO DEPLOYED APP](https://your-deployed-app-url.com)** *(Update with your new deployment URL)*

---

## Introduction

This project uses the **Algerian Forest Fires Dataset** from UCI. The dataset contains forest fire observations from two regions of Algeria: **Bejaia** and **Sidi Bel-Abbes**.

**Timeline**: June 2012 to September 2012

The goal is to predict forest fires using weather features through various Machine Learning algorithms.

---

## Tech Stack

### Programming & Libraries

| Category | Technologies |
|----------|--------------|
| Language | Python 3.7+ |
| ML/AI | Scikit-learn |
| Web Framework | Flask |
| Database | **PostgreSQL** |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| DB ORM | SQLAlchemy / psycopg2 |

### Development Tools

| Category | Tools |
|----------|-------|
| **IDE** | **VSCode** |
| Version Control | Git, GitHub |
| API Testing | Postman |
| Database GUI | pgAdmin / VSCode PostgreSQL Extension |
| Cloud Hosting | Your preferred platform |

---

## Project Structure

```
forest-fire-prediction/
├── dataset/                 # Source dataset files
├── model/                   # Trained model files (.pkl)
├── notebook/                 # Jupyter notebooks for analysis
│   ├── EDA_Forest_Fire.ipynb
│   └── Model_Building.ipynb
├── static/                  # Static assets (CSS, JS, images)
├── templates/                # HTML templates for Flask app
├── .gitignore
├── app.py                   # Main Flask application
├── app_logger.py            # Application logging module
├── database.py              # PostgreSQL connection handler
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

Before running this project, ensure you have the following installed:

1. **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
2. **VSCode** - [Download VSCode](https://code.visualstudio.com/)
3. **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
4. **Git** - [Download Git](https://git-scm.com/)

### VSCode Extensions Recommended

Install these extensions in VSCode for optimal development:

- Python (Microsoft)
- PostgreSQL (Chris Kolley)
- Jupyter (Microsoft)
- Pylance (Microsoft)

### Database Setup (PostgreSQL)

1. **Install PostgreSQL** and set up your local server
2. **Create a database**:
   ```sql
   CREATE DATABASE forest_fire_db;
   ```
3. **Create a user** (optional):
   ```sql
   CREATE USER db_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE forest_fire_db TO db_user;
   ```

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/forest_fire_db
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/aravind-selvam/forest-fire-prediction.git
cd forest-fire-prediction
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Dataset

Download the dataset from [UCI Repository](https://archive.ics.uci.edu/ml/datasets/Algerian+Forest+Fires+Dataset++#) and place it in the `dataset/` folder.

### Step 5: Configure Database Connection

Update the `database.py` file with your PostgreSQL credentials:

```python
import psycopg2
from psycopg2 import sql

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'forest_fire_db',
    'user': 'your_username',
    'password': 'your_password',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
```

### Step 6: Load Data to PostgreSQL

Run the data loading script to insert CSV data into PostgreSQL:

```bash
python -c "from database import load_data_to_db; load_data_to_db('dataset/Algerian_Forest_Fires.csv')"
```

### Step 7: Run the Application

```bash
python app.py
```

The app will be available at `http://localhost:5000`

---

## Model Building

### Regression Models (FWI Prediction)

The following models are used to predict the **Fire Weather Index (FWI)**:

| Model | Description |
|-------|-------------|
| Linear Regression | Baseline linear model |
| Lasso Regression | L1 regularization |
| Ridge Regression | L2 regularization |
| Random Forest | Ensemble method |
| Decision Tree | Tree-based model |
| K-Nearest Neighbour | Distance-based model |
| Support Vector Regressor | Kernel-based model |

### Classification Models (Fire/Not Fire)

The following models predict **fire occurrence** (binary classification):

| Model | Description |
|-------|-------------|
| Logistic Regression | Linear classification |
| Decision Tree | Tree-based classification |
| Random Forest | Ensemble classification |
| XGBoost | Gradient boosting |
| K-Nearest Neighbour | Distance-based classification |

### Model Selection Strategy

**Classification:**
- Stratified K-Fold Cross-Validation
- Best Mean CV Accuracy model selected

**Regression:**
- R² Score metrics
- Randomized GridSearch CV for hyperparameter tuning

---

## Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Render home page |
| `/predict` | POST | Classification predictions (fire/not fire) |
| `/predictR` | POST | Regression predictions (FWI) |
| `/predict_api` | POST | API endpoint for Postman testing |

---

## Deployment

### Cloud Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Set up cloud hosting** (Railway, Render, Fly.io, etc.)

3. **Configure environment variables** on your hosting platform:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   ```

4. **Deploy using Git** or CI/CD pipeline

---

## Data Pipeline

### Loading CSV to PostgreSQL

```python
import pandas as pd
import psycopg2
from database import get_connection

def load_csv_to_postgres(csv_path):
    # Read CSV
    df = pd.read_csv(csv_path)

    # Clean data
    df = df.dropna()

    # Insert to PostgreSQL
    conn = get_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forest_fires (
            id SERIAL PRIMARY KEY,
            temperature DECIMAL,
            humidity DECIMAL,
            wind_speed DECIMAL,
            rain DECIMAL,
            fwi DECIMAL,
            classes VARCHAR(50),
            region VARCHAR(50),
            date DATE
        )
    """)

    # Insert data
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO forest_fires (temperature, humidity, wind_speed, rain, fwi, classes, region, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
```

---

## EDA (Exploratory Data Analysis)

The EDA notebook (`notebook/EDA_Forest_Fire.ipynb`) contains:

- Data loading and cleaning
- Univariate analysis
- Bivariate analysis
- Correlation heatmaps
- Feature importance visualization
- Outlier detection

---

## API Testing with Postman

### Classification Prediction

```http
POST /predict_api
Content-Type: application/json

{
    "Temperature": 30,
    "Humidity": 45,
    "Wind Speed": 15,
    "Rain": 0,
    "FFMC": 85,
    "DMC": 12,
    "DC": 20,
    "ISI": 5,
    "BUI": 15
}
```

### Regression Prediction (FWI)

```http
POST /predictR
Content-Type: application/json

{
    "Temperature": 30,
    "Humidity": 45,
    "Wind Speed": 15,
    "Rain": 0,
    "FFMC": 85,
    "DMC": 12,
    "DC": 20
}
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Contact

- **mutasim alkamil**
- [LinkedIn](https://www.linkedin.com/in/mutasim-al-kamil-40a29931)
- Email: asoomkamel193@gmail.com
-https://github.com/Asoomkamel 

---

## Acknowledgments

- [UCI Machine Learning Repository](https://archive.ics.uci.edu/) - For the Algerian Forest Fires Dataset
- Scikit-learn Documentation
- Flask Documentation
- PostgreSQL Documentation
