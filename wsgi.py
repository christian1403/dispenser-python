"""
WSGI Entry Point for Production Deployment
"""

from app import create_app

# Create application instance
application = create_app()

if __name__ == "__main__":
    application.run()
