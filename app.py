import pickle
import bz2
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, jsonify, render_template
import warnings

warnings.filterwarnings("ignore")

# Import custom modules
from app_logger import log
from postgresql import postgresqlconnection

app = Flask(__name__)

# Global variables
model_C = None
model_R = None
scaler = None

def load_models():
    """Load ML models from pickle files"""
    global model_C, model_R
    try:
        pickle_in = bz2.BZ2File('model/classification.pkl', 'rb')
        R_pickle_in = bz2.BZ2File('model/regression.pkl', 'rb')
        model_C = pickle.load(pickle_in)
        model_R = pickle.load(R_pickle_in)
        log.info('Models loaded successfully')
        return True
    except FileNotFoundError as e:
        log.error(f'Model file not found: {e}')
        return False
    except Exception as e:
        log.error(f'Error loading models: {e}')
        return False

def initialize_scaler():
    """Initialize the StandardScaler - either from database or with default values"""
    global scaler
    scaler = StandardScaler()

    try:
        # Try to connect to database and get training data
        dbcon = postgresqlconnection(host='localhost', database='fire_db', user='postgres', password='root')
        list_cursor = dbcon.getdata(tableName='ml_task')

        if list_cursor and len(list_cursor) > 0:
            df = pd.DataFrame(list_cursor)

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()

            # Try to find temperature column (case-insensitive)
            temp_col = None
            for col in df.columns:
                if 'temp' in col.lower():
                    temp_col = col
                    break

            if temp_col:
                # Clean and prepare data
                df = df[pd.to_numeric(df[temp_col], errors='coerce').notnull()]

                # Map common column names to expected feature names
                web_features = []
                column_mapping = {
                    'temperature': ['temperature', 'temp', 'temp_c'],
                    'ws': ['ws', 'wind_speed', 'windspeed', 'wind speed', 'wind'],
                    'ffmc': ['ffmc', 'fine_fuel_moisture'],
                    'dmc': ['dmc', 'duff_moisture'],
                    'isi': ['isi', 'initial_spread']
                }

                for feature, aliases in column_mapping.items():
                    for alias in aliases:
                        if alias in df.columns:
                            web_features.append(alias)
                            break

                if len(web_features) >= 5:
                    X = df[web_features].copy()

                    # Remove internal spaces and convert to numeric
                    X = X.replace(to_replace=r'\s+', value='', regex=True)
                    X = X.apply(pd.to_numeric, errors='coerce').dropna()

                    if len(X) > 0:
                        scaler.fit(X)
                        log.info(f'Scaler fitted on {len(X)} records with features: {web_features}')
                        dbcon.close()
                        return True

        dbcon.close()
    except Exception as e:
        log.error(f'Database error during scaler initialization: {e}')

    # Fallback: Use default scaler parameters based on typical forest fire data ranges
    log.warning('Using default scaler parameters')
    # Typical ranges for forest fire data:
    # Temperature: 15-42°C
    # Wind Speed: 0-30 km/h
    # FFMC: 20-100
    # DMC: 0-300
    # ISI: 0-50
    default_data = np.array([
        [25, 15, 90, 50, 10],
        [30, 20, 85, 100, 15],
        [35, 10, 95, 150, 25],
        [20, 25, 80, 30, 5],
        [28, 18, 88, 80, 12],
    ])
    scaler.fit(default_data)
    log.info('Scaler fitted with default data')
    return True

# Initialize on startup
load_models()
initialize_scaler()

@app.route('/')
def home():
    log.info('Home page loaded successfully')
    return render_template('index.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        if model_C is None:
            return jsonify({'error': 'Classification model not loaded'}), 500

        data = request.json['data']
        log.info(f'Input from API: {data}')

        new_data = [list(data.values())]
        final_data = scaler.transform(new_data)
        output = int(model_C.predict(final_data)[0])

        text = 'The Forest in Danger' if output == 1 else 'Forest is Safe'
        return jsonify({'prediction': text, 'result': output})
    except Exception as e:
        log.error(f'Error in API prediction: {e}')
        return jsonify({'error': 'Check the input again!'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model_C is None:
            log.error('Classification model not loaded')
            return render_template('index.html', prediction_text1="Classification model not loaded!")

        # Get 5 inputs from form
        data = [float(x) for x in request.form.values()]

        if len(data) != 5:
            return render_template('index.html', prediction_text1="Please provide exactly 5 input values!")

        final_features = np.array(data).reshape(1, -1)

        # Transform using the scaler
        final_features = scaler.transform(final_features)
        output = model_C.predict(final_features)[0]
        log.info('Classification prediction successful')

        # Try to store in database
        try:
            dbcon = postgresqlconnection(host='localhost', database='fire_db', user='postgres', password='root')
            db_entry = (data[0], data[1], data[2], data[3], data[4], int(output))
            dbcon.insert_prediction(db_entry)
            dbcon.close()
        except Exception as db_err:
            log.error(f"Failed to save prediction to DB: {db_err}")

        text = 'Forest is in Danger!' if output == 1 else 'Forest is Safe!'
        return render_template('index.html', prediction_text1="{} --- Chance of Fire is {}".format(text, output))
    except ValueError as e:
        log.error(f'Input validation error: {e}')
        return render_template('index.html', prediction_text1="Invalid input! Please enter numeric values.")
    except Exception as e:
        log.error(f'Classification Input error: {e}')
        return render_template('index.html', prediction_text1="Check the Input again!!!")

@app.route('/predictR', methods=['POST'])
def predictR():
    try:
        if model_R is None:
            log.error('Regression model not loaded')
            return render_template('index.html', prediction_text2="Regression model not loaded!")

        data = [float(x) for x in request.form.values()]

        if len(data) != 5:
            return render_template('index.html', prediction_text2="Please provide exactly 5 input values!")

        final_features = np.array(data).reshape(1, -1)

        # Transform using the scaler
        final_features = scaler.transform(final_features)
        output = model_R.predict(final_features)[0]
        log.info('Regression prediction successful')

        # Try to store in database
        try:
            dbcon = postgresqlconnection(host='localhost', database='fire_db', user='postgres', password='root')
            db_entry = (data[0], data[1], data[2], data[3], data[4], float(output))
            dbcon.insert_prediction(db_entry)
            dbcon.close()
        except Exception as db_err:
            log.error(f"Failed to save regression to DB: {db_err}")

        if output > 15:
            return render_template('index.html', prediction_text2="Fuel Moisture Code index is {:.4f} ---- Warning!!! High hazard rating".format(output))
        else:
            return render_template('index.html', prediction_text2="Fuel Moisture Code index is {:.4f} ---- Safe.. Low hazard rating".format(output))
    except ValueError as e:
        log.error(f'Input validation error: {e}')
        return render_template('index.html', prediction_text2="Invalid input! Please enter numeric values.")
    except Exception as e:
        log.error(f'Regression Input error: {e}')
        return render_template('index.html', prediction_text2="Check the Input again!!!")

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model_C is not None and model_R is not None,
        'scaler_ready': scaler is not None
    })

if __name__ == "__main__":
    log.info('Starting Forest Fire Prediction Flask Application')
    app.run(debug=True, host='0.0.0.0', port=5000)