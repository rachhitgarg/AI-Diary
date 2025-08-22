#!/bin/bash

echo "========================================"
echo "   AI Student Diary - Quick Start"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Python found! Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo
echo "Dependencies installed successfully!"
echo "Starting the application..."
echo
echo "The app will open in your default browser"
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo
echo "Press Ctrl+C to stop the application"
echo

streamlit run app.py
