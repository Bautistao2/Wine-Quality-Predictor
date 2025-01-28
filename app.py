import streamlit as st
import pickle
import pandas as pd
import os
from pyspark.sql import SparkSession

# Set Spark environment variables
os.environ["PYSPARK_PYTHON"] = "c:/Users/ostab/Documents/PROYECTO VINO/Wine-Quality-Predictor/venv/Scripts/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "c:/Users/ostab/Documents/PROYECTO VINO/Wine-Quality-Predictor/venv/Scripts/python.exe"

# Function to create Spark session
def create_spark_session():
    return SparkSession.builder \
        .appName("Wine Quality Predictor") \
        .master("local[1]") \
        .config("spark.executor.memory", "1g") \
        .config("spark.hadoop.fs.defaultFS", "file:///") \
        .getOrCreate()

# Streamlit app layout
st.set_page_config(page_title="🍷 Wine Quality Predictor", layout="wide", page_icon="🍷")

# Title and description with custom styling
st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #7B3F00;
    }
    .description {
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
        color: #444444;
    }
    </style>
    <div class="title">🍷 Wine Quality Predictor 🍷</div>
    <div class="description">Use this app to predict the quality of wine based on its physicochemical properties.</div>
    """,
    unsafe_allow_html=True
)


# Load the trained Random Forest model
@st.cache_resource
def load_model():
    try:
        model_path = "Models/wine_quality_model.pkl"
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

model = load_model()
spark = create_spark_session()

# Sidebar for wine type selection
st.sidebar.header("Wine Type Selection")
wine_type = st.sidebar.radio("Select Wine Type:", options=["Red", "White"], index=0)
# Encode wine type: Red = 0, White = 1
wine_type_encoded = 0 if wine_type == "Red" else 1

# Input fields for wine properties with two columns
st.markdown("<h3 style='text-align: center;'>Enter Wine Properties</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fixed_acidity = st.number_input("Fixed Acidity", min_value=0.0, value=7.4, step=0.1)
    volatile_acidity = st.number_input("Volatile Acidity", min_value=0.0, value=0.7, step=0.01)
    citric_acid = st.number_input("Citric Acid", min_value=0.0, value=0.0, step=0.01)
    residual_sugar = st.number_input("Residual Sugar", min_value=0.0, value=1.9, step=0.1)
    chlorides = st.number_input("Chlorides", min_value=0.0, value=0.076, step=0.001)

with col2:
    free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", min_value=0, value=11, step=1)
    total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", min_value=0, value=34, step=1)
    density = st.number_input("Density", min_value=0.0, value=0.9978, step=0.0001)
    pH = st.number_input("pH", min_value=0.0, value=3.51, step=0.01)
    sulphates = st.number_input("Sulphates", min_value=0.0, value=0.56, step=0.01)
    alcohol = st.number_input("Alcohol", min_value=0.0, value=9.4, step=0.1)

# Prediction button with centered alignment
st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
if st.button("Predict Wine Quality"):
    if model is not None:
        try:
            # Prepare input data
            input_data = pd.DataFrame({
                "fixed acidity": [fixed_acidity],
                "volatile acidity": [volatile_acidity],
                "citric acid": [citric_acid],
                "residual sugar": [residual_sugar],
                "chlorides": [chlorides],
                "free sulfur dioxide": [free_sulfur_dioxide],
                "total sulfur dioxide": [total_sulfur_dioxide],
                "density": [density],
                "pH": [pH],
                "sulphates": [sulphates],
                "alcohol": [alcohol],
                "wine_type": [wine_type_encoded]  # Add the wine_type column
            })

            # Make prediction using the loaded model
            prediction = model.predict(input_data)[0]

            # Display prediction
            st.success(f"The predicted wine quality is: {int(prediction)}")
        except Exception as e:
            st.error(f"Error during prediction: {e}")
    else:
        st.error("The Random Forest model could not be loaded. Please check the model path.")
st.markdown("</div>", unsafe_allow_html=True)
