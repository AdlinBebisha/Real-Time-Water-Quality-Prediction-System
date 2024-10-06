import numpy as np
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

def fetch_data():
    result_text.delete(1.0, tk.END)  # Clear previous results

    # ThingSpeak channel ID and API key for fetching data
    channel_id = '2421427'
    api_key = '8A6ZUK3I9ZWBLGUX'

    # URL for reading data from ThingSpeak
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}'

    # Make a GET request to the ThingSpeak API
    response = requests.get(url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract and display the current values in the GUI window
        if 'feeds' in data and len(data['feeds']) > 0:
            last_feed = data['feeds'][-1]  # Get the last feed entry
            timestamp = last_feed['created_at']
            field1_value = last_feed.get('field1')
            field2_value = last_feed.get('field2')
            field3_value = last_feed.get('field3')
            field4_value = last_feed.get('field4')


            result_text.insert(tk.END, f'Timestamp: {timestamp}, Temperature: {field1_value}, Ph:{field2_value}, Turbidity: {field3_value}, TDS(Total Dissolved Solids): {field4_value}\n')

        else:
            result_text.insert(tk.END, 'No data available.\n')
    else:
        result_text.insert(tk.END, f'Error: Unable to fetch data. Status code {response.status_code}\n')

def mean_absolute_error(actual, predicted):
    mean_error = np.mean(np.abs(actual-predicted))
    return mean_error

def root_mean_sqauer_error(actual, predicted):
    root_error = np.sqrt(np.mean((actual-predicted)**2))
    return root_error

def r_squared(actual, predicted):
    actual_mean = np.mean(actual)
    predicted_mean = np.mean(predicted)
    ss_residual = np.sum((actual-predicted)**2)
    ss_total = np.sum((actual-actual_mean)**2) +1e-8
    if ss_total<= ss_residual:
        return 0
    else:
        r = 1-(ss_residual/ss_total)
        return r

def predict_water_suitability(current_values):
    # Load training data from CSV file
    print("Loading training data...")
    training_data = pd.read_csv('water_potability.csv')
    print("Training data loaded successfully.")

    # Extract features (X_train) and labels (y_train)
    X_train = training_data[['ph', 'Turbidity', 'Total Dissolved Solids', 'Temperature']]
    y_train = training_data['suitable_for_drinking']

    # Handle missing values by imputing with mean
    X_train.fillna(X_train.mean(), inplace=True)

    # Train the KNN algorithm
    print("Training KNN model...")
    k_neighbors = 5
    knn_model = KNeighborsClassifier(n_neighbors=k_neighbors)
    knn_model.fit(X_train, y_train)
    print("KNN model trained successfully.")

    # Use the trained KNN model to predict
    print("Predicting water suitability...")
    prediction = knn_model.predict([current_values])
    print("Prediction completed.")

    # Output the prediction result
    if prediction[0] == 1:
        return "The water is suitable for drinking."
    else:
        return "The water is not suitable for drinking."


def call_prediction():
    # Sample current values
    current_values = [7.0, 1.0, 300, 25]  # Example values for pH, Turbidity, TDS, and Temperature
    prediction_result = predict_water_suitability(current_values)
    result_text.insert(tk.END, f'\nPrediction Result: {prediction_result}\n')

def calculate_accuracy(actual, predicted):
    # Calculate the percentage difference between actual and predicted values
    percentage_difference = abs(actual - predicted) / actual * 100

    # Calculate accuracy rate by subtracting the percentage difference from 100
    accuracy_rate = 100 - percentage_difference

    # Ensure accuracy rate is not negative
    accuracy_rate = max(accuracy_rate, 0)

    return accuracy_rate

def calculate_and_display_accuracy():
    result_text.delete(1.0, tk.END)  # Clear previous results

    for parameter in ['Ph', 'Turbidity', 'TDS']:
        actual_values = iot_data[parameter]
        predicted_values = lab_data[parameter]

        result_text.insert(tk.END, f"\nAccuracy between Lap Result and IoT Data of {parameter}\n")

        mae = mean_absolute_error(actual_values.mean(), predicted_values.mean())
        result_text.insert(tk.END, f"Mean Absolute Error for {parameter}: {mae:.2f}%\n")

        rmse = root_mean_sqauer_error(actual_values.mean(), predicted_values.mean())
        result_text.insert(tk.END, f"Root Mean Square Error for {parameter}: {rmse:.2f}%\n")

        r_sqr = r_squared(actual_values.mean(), predicted_values.mean())
        result_text.insert(tk.END, f"R Squared for {parameter}: {r_sqr:.2f}%\n")

        # Assuming you want to calculate average accuracy for all samples
        average_accuracy = calculate_accuracy(actual_values.mean(), predicted_values.mean())
        result_text.insert(tk.END, f"Average Accuracy for {parameter}: {average_accuracy:.2f}%\n")

# Sample data for accuracy comparison
iot_data = pd.DataFrame({
    'Ph': [7.74,7.65,7.12,6.9,6.43],
    'Turbidity': [1.72,1.5,1.49,0.51,0.31],
    'TDS': [1745.92,1662.28,1524.67,531.98,401.53],
    'Source': ['IoT', 'IoT', 'IoT', 'IoT', 'IoT']
})

lab_data = pd.DataFrame({
    'Ph': [7.64,7.4,7.36,6.74,6.54],
    'Turbidity': [1.6,1.45,1.5,0.42,0.29],
    'TDS': [1740.33,1682.44,1502.01,530.38,380.95],
    'Source': ['Lab', 'Lab', 'Lab', 'Lab', 'Lab']
})

# GUI setup
root = tk.Tk()
root.title("Real-Time Water Quality Prediction System")

# Frames
frame_image = ttk.Frame(root, padding=(10, 10, 10, 0))
frame_image.pack(fill="both")

frame_fetch = ttk.Frame(root, padding=(10, 0, 10, 0))
frame_fetch.pack(fill="both")

frame_calculate = ttk.Frame(root, padding=(10, 0, 10, 10))
frame_calculate.pack(fill="both")

frame_result = ttk.Frame(root, padding=(10, 0, 10, 10))
frame_result.pack(fill="both")

# Load and display image
image_path = 'image.jpeg'  # Use the appropriate relative or absolute path to your image file
pil_image = Image.open(image_path)

tk_image = ImageTk.PhotoImage(pil_image)
label_image = tk.Label(frame_image, image=tk_image)
label_image.pack()

# Button to fetch data
fetch_button = ttk.Button(frame_fetch, text="Fetch Data From Cloud", command=fetch_data)
fetch_button.pack(pady=5)

# Button to call prediction function
predict_button = ttk.Button(frame_calculate, text="Predict the water is good for use or not", command=call_prediction)
predict_button.pack(pady=5)

# Button to trigger calculation and display accuracy
calculate_button = ttk.Button(frame_calculate, text="Calculate Accuracy between the Lab result and Iot result of collected samples", command=calculate_and_display_accuracy)
calculate_button.pack(pady=5)

# Text widget to display results
result_text = scrolledtext.ScrolledText(frame_result, height=100, width=200, wrap=tk.WORD)
result_text.pack(fill="both", expand=True)

root.mainloop()
