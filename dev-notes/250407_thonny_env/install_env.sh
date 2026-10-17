# Create a virtual environment
python3 -m venv .env

# Activate the virtual environment
source .env/bin/activate

# Install the required libraries
pip install -r requirements.txt

echo "Environment setup complete. To activate the environment, run 'source .env/bin/activate'."
