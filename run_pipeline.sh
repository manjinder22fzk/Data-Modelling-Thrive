#!/bin/bash

# Checking if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Virtual environment not found. Creating one..."
  python -m venv venv
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Step 3: Install requirements
echo "Installing required Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Run the pipeline
echo "Running the ETL pipeline..."
python src/load_consolidated_messages.py

# Step 5: Done
echo "Pipeline execution completed successfully!"
