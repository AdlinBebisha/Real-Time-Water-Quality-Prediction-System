# Real-Time Water Quality Prediction System

This project is designed to fetch real-time water quality data from the ThingSpeak cloud, perform water quality prediction using a K-Nearest Neighbors (KNN) classifier, and compare the accuracy of IoT sensor data with laboratory test results.

## Features

- Fetch water quality data (pH, Turbidity, TDS, Temperature) from ThingSpeak using a cloud API.
- Predict whether the water is suitable for drinking using a trained KNN classifier.
- Compare the accuracy of IoT data with laboratory results using metrics such as Mean Absolute Error, Root Mean Squared Error, and R-squared.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Hardware Setup](#hardware-setup)
- [Software](#software)
- [How It Works](#how-it-works)
- [Results](#results)

## Installation

1. Clone the repository from GitHub:

    ```bash
    git clone https://github.com/AdlinBebisha/Real-Time-Water-Quality-Prediction-System.git
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have the following libraries installed:
    - `numpy`
    - `pandas`
    - `requests`
    - `tkinter`
    - `scikit-learn`
    - `Pillow`

4. Update the ThingSpeak API credentials in `fetch_data` function.

5. Run the project by executing the Python script:

    ```bash
    python app.py
    ```

## Usage

### GUI Features

1. **Fetch Data from Cloud:**  
   Click the "Fetch Data From Cloud" button to fetch the latest water quality data (Temperature, pH, Turbidity, TDS) from the ThingSpeak channel.

2. **Predict Water Suitability:**  
   The "Predict the water is good for use or not" button allows you to predict if the water is suitable for drinking based on the fetched data using a KNN model.

3. **Compare Lab and IoT Data:**  
   The "Calculate Accuracy between the Lab result and IoT result of collected samples" button compares lab data with IoT sensor data using error metrics and displays the accuracy.

### Arduino and ESP Configuration

To upload the code to the respective microcontrollers:
- Arduino Uno: Refer to the `Ardiuno_Uno.ino` file.
- ESP-12E: Refer to the `ESP-12E.ino` file.

Ensure that the hardware is properly connected and configured to send sensor data to ThingSpeak.

## Hardware Setup

- **Arduino Uno** and **ESP-12E** microcontroller boards
- pH sensor
- Turbidity sensor
- TDS sensor
- Temperature sensor
- IoT-enabled communication to send data to ThingSpeak

## Software

- The `Arduino_Uno.ino` and `ESP-12E.ino` files contain the code to collect sensor data and send it to the cloud via the ThingSpeak API.

## How It Works

1. **Data Collection:**  
   The hardware collects water quality parameters such as pH, Turbidity, TDS, and Temperature from sensors and uploads the data to ThingSpeak.

2. **Prediction Algorithm:**  
   A K-Nearest Neighbors (KNN) classifier is trained on a dataset of water quality readings to predict whether the water is suitable for drinking. Missing values in the dataset are handled using mean imputation.

3. **Accuracy Calculation:**  
   The system calculates the accuracy between IoT-collected data and lab-tested data using Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and R-squared values.

## Results

- The system provides real-time predictions on water quality based on sensor data.
- It offers comparative metrics to determine how close IoT measurements are to lab results.

