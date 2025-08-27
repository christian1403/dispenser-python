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

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
<<<<<<< HEAD
    mode = os.getenv("FLASK_ENV", "production").lower()
    if mode == "development":
        app.run(host=host, port=port, debug=debug)
    else:
        app.run(debug=debug)
=======
    
    socketio.run(app=app, host=host, port=port, debug=debug)
>>>>>>> bfe3dd4 (integration flask socket io to project)
