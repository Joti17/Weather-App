# Weather App - Real-Time Weather Visualization with PyQt5

## Overview

This Weather App is a dynamic desktop application built with PyQt5 that delivers real-time weather information, leveraging the WeatherAPI service. The application provides a visually intuitive user interface featuring updated weather icons, temperature readings, and city-based queries.

Designed with responsiveness and user experience in mind, the app integrates asynchronous data fetching with a sleek, scalable UI to ensure optimal performance across screen configurations.

---

## Key Features

- **Real-time Weather Data**: Fetches up-to-date weather conditions based on user-specified cities using the WeatherAPI.
- **Dynamic UI Scaling**: Automatically adjusts font sizes and icon dimensions relative to window size, enhancing readability and aesthetics.
- **Background Image Support**: Displays randomized background imagery for visual appeal.
- **Robust Error Handling**: Gracefully manages API request failures and invalid inputs without crashing.
- **Multi-threaded Data Refresh**: Periodically updates weather information asynchronously to maintain UI responsiveness.

---

## Technology Stack

- **Python 3.x**
- **PyQt5**: GUI framework for building native desktop applications.
- **Requests**: HTTP library to handle API calls.
- **WeatherAPI**: External weather data provider.
- **screeninfo**: For multi-monitor screen detection and placement.
- **Threading**: To perform periodic background data fetching without blocking the UI.

---

## Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Joti17/weather-app.git
   cd weather-app
