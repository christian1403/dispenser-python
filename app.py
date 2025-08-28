"""
Flask API Application Entry Point
"""

import os
from dotenv import load_dotenv
from app import create_app
from app.utils.extension import socketio

# Load environment variables
load_dotenv()

# Create Flask application instance
app = create_app()

# Setup flask socket
socketio.init_app(app,  cors_allowed_origins="*")
    
from app.event import sensor_event

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    mode = os.getenv("FLASK_ENV", "production").lower()
    if mode == "development":
        socketio.run(app,host=host, port=port, debug=debug)
    else:
        socketio.run(app=app,debug=debug)
