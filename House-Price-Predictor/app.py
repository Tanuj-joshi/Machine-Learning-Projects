# reuired libraries
import pickle
import pandas as pd
import requests
from flask import Flask, render_template, request
import numpy as np


# Initialize the Flask application
app = Flask(__name__)
# Load the dataset
data = pd.read_csv('Dataset/Cleaned_data.csv')
# Load the trained Ridge regression model
pipe = pickle.load(open("RidgeModel.pkl", "rb"))
# Define the home route
@app.route('/')

def index():
    # Get a sorted list of unique locations from the dataset
    locations = sorted(data['location'].unique())
     # Render the index.html template with the locations data
    return render_template('index.html', locations=locations)

# Define the prediction route, which accepts POST requests
@app.route('/predict', methods=['POST'])

def predict():
    # Get user input from the form
    location = request.form.get('location')
    bhk = request.form.get('bhk')
    bath = request.form.get('bath')
    sqft = request.form.get('total_sqft')

    # Create a DataFrame with the input data
    input = pd.DataFrame([[location,sqft,bath,bhk]],columns=['location','total_sqft','bath','bhk'])
    # Make a prediction using the loaded model
    prediction = pipe.predict(input)[0] * 1e3
    # Return the prediction as a string, rounded to 2 decimal places
    return str(np.round(prediction,2))


# Run the application
if __name__== "__main__":
    app.run(debug=True, port=5001)