# Flask API Project

A professional Flask API with environment-based configuration, API key authentication, and AI-friendly structure.

## 🚀 Features

- **Environment-based Configuration**: Uses `.env` files for configuration management
- **API Key Authentication**: Secure endpoints with API key validation
- **Rate Limiting**: Built-in rate limiting to prevent abuse
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling with standardized responses
- **Testing**: Complete test suite with pytest
- **AI-Friendly Structure**: Clean, modular architecture easy for AI to understand and modify

## 📁 Project Structure

```
dispenser-python/
├── app/
│   ├── __init__.py                 # Flask application factory
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # API route definitions
│   ├── models/
│   │   ├── __init__.py
│   │   └── example_model.py       # Data models
│   ├── services/
│   │   ├── __init__.py
│   │   └── example_service.py     # Business logic
│   └── utils/
│       ├── __init__.py
│       ├── auth.py                # Authentication utilities
│       ├── config.py              # Configuration classes
│       ├── error_handlers.py      # Error handling
│       └── helpers.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Test configuration
│   ├── test_api_routes.py         # API endpoint tests
│   └── test_example_service.py    # Service layer tests
├── .env                           # Environment variables (local)
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── app.py                         # Application entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dispenser-python
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

## 🚀 Usage

### Starting the Development Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# API Configuration
API_KEY=your_secret_api_key_here
API_VERSION=v1
HOST=0.0.0.0
PORT=5000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# CORS Settings
CORS_ORIGINS=*
```

## 📚 API Documentation

### Authentication

All protected endpoints require an API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your_api_key" http://localhost:5000/api/v1/example
```

### Endpoints

#### Health Check
- **GET** `/health`
- **Description**: Check if the API is running
- **Authentication**: Not required

#### API Status
- **GET** `/api/v1/status`
- **Description**: Get API version and status information
- **Authentication**: Not required

#### Get Examples
- **GET** `/api/v1/example`
- **Description**: Retrieve all examples
- **Authentication**: Required

#### Create Example
- **POST** `/api/v1/example`
- **Description**: Create a new example
- **Authentication**: Required
- **Body**:
  ```json
  {
    "name": "string",
    "value": "string",
    "description": "string (optional)"
  }
  ```

#### Get Example by ID
- **GET** `/api/v1/example/<id>`
- **Description**: Retrieve a specific example by ID
- **Authentication**: Required

#### Update Example
- **PUT** `/api/v1/example/<id>`
- **Description**: Update an existing example
- **Authentication**: Required
- **Body**:
  ```json
  {
    "name": "string",
    "value": "string (optional)",
    "description": "string (optional)"
  }
  ```

#### Delete Example
- **DELETE** `/api/v1/example/<id>`
- **Description**: Delete an example
- **Authentication**: Required

### Response Format

All API responses follow a consistent format:

**Success Response**:
```json
{
  "success": true,
  "message": "Success message",
  "data": { ... },
  "timestamp": "2025-08-17T10:00:00Z"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2025-08-17T10:00:00Z"
}
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

Run specific test file:

```bash
pytest tests/test_api_routes.py
```

## 🔧 Development

### Adding New Endpoints

1. **Create a new route** in `app/api/routes.py`
2. **Add business logic** in a service class in `app/services/`
3. **Create data models** if needed in `app/models/`
4. **Write tests** in the `tests/` directory

### Project Architecture

This project follows a layered architecture:

- **Routes Layer** (`app/api/`): Handles HTTP requests and responses
- **Service Layer** (`app/services/`): Contains business logic
- **Model Layer** (`app/models/`): Defines data structures
- **Utils Layer** (`app/utils/`): Shared utilities and configurations

## 📦 Deployment

### Using Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤖 AI-Friendly Features

This project is designed to be easily understood and modified by AI:

- **Clear Structure**: Modular architecture with separated concerns
- **Consistent Naming**: Predictable file and function names
- **Comprehensive Documentation**: Detailed docstrings and comments
- **Standard Patterns**: Uses common Flask patterns and best practices
- **Type Hints**: Uses dataclasses and type hints where appropriate
- **Error Handling**: Comprehensive error handling with clear messages

## 🔒 Security

- API key authentication for protected endpoints
- Rate limiting to prevent abuse
- CORS configuration for cross-origin requests
- Input validation and sanitization
- Secure error handling (no sensitive data in responses)

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
