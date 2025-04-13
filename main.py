import logging
from app import app

# Configure logging for easier debugging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# This file is a simple entrypoint for Render.com or other hosting services
# The app instance is imported from app.py
