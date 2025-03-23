# Fake News Detection System

A comprehensive application for detecting fake news using advanced text processing and machine learning techniques.

## Project Structure

This project is organized into two main components:

```
h1/
├── backend/            # Python backend API
│   ├── app/            # Main application modules
│   ├── models/         # Trained machine learning models
│   ├── utils/          # Utility functions including text processors
│   └── tests/          # Backend tests
├── frontend/           # React frontend application
│   ├── public/         # Static assets
│   └── src/            # Source code
│       ├── components/ # React components
│       ├── pages/      # Page components
│       └── utils/      # Frontend utilities
├── data/               # Data directories (not included in repo)
└── scripts/            # Helper scripts
```

## Features

- Machine learning-based fake news detection
- Text analysis features:
  - Language detection
  - Entity extraction
  - Readability metrics
  - Propaganda technique detection
  - Text uniqueness analysis
- Interactive frontend dashboard
- API for integration with other applications

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 14+ (for frontend)
- A modern web browser

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

### Option 1: Using the Integrated Script

You can run both backend and frontend with a single command:

```
.\run-both.ps1
```

This will:
- Start the backend server on port 8000
- Start the frontend server on port 3000
- Open the application in your default browser
- Monitor server health

### Option 2: Manual Startup

#### Start Backend

```
cd backend
python -m uvicorn fixed_backend:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend

```
cd frontend
npm start
```

## API Documentation

The API documentation is available when the backend is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development Notes

- The frontend communicates with the backend via REST API
- Backend configuration can be modified in `backend/config.py`
- Frontend configuration can be modified in `frontend/src/config.js`
- The application uses FastAPI for the backend and React for the frontend

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are installed correctly
2. Check if the backend server is running and accessible
3. Verify that the frontend is configured with the correct backend URL
4. Look for error messages in the terminal running the servers

## License

This project is licensed under the MIT License - see the LICENSE file for details. 