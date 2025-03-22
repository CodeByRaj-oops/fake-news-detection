# Fake News Detection System

A web application for analyzing and detecting fake news articles and social media posts using advanced machine learning techniques.

## Project Overview

This system uses natural language processing and machine learning to analyze text content and determine its credibility. The application provides:

- Text analysis for detecting fake news
- Visual credibility ratings
- Detailed analysis reports
- History tracking of past analyses
- Saved reports functionality

## Technology Stack

### Frontend
- React.js
- React Router for navigation
- Tailwind CSS for styling
- Axios for API requests
- Chart.js for data visualization

### Backend
- Python FastAPI
- Machine Learning models for text analysis
- SQLite for data storage

## Running the Application

### Frontend

```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000.

### Backend

```bash
cd backend
pip install -r requirements.txt
python app_new.py
```

The backend API will be available at http://localhost:8000.

## Project Structure

- `frontend/`: React application with components and pages
  - `src/components/`: Reusable UI components
  - `src/pages/`: Page components for routing
  - `src/contexts/`: State management
  - `src/api/`: API service for backend communication

- `backend/`: Python FastAPI backend
  - `app_new.py`: Main application entry point
  - `improved_predict.py`: ML prediction functionality
  - `improved_train_model.py`: Model training code
  - `utils/`: Helper functions and utilities
  - `models/`: Trained machine learning models

## Features

- **Text Analysis**: Input text directly or via URL for analysis
- **Credibility Assessment**: Get a credibility score and classification
- **Detailed Reports**: View detailed analysis of content including sentiment, bias, and factual consistency
- **History Tracking**: Review past analyses
- **Data Visualization**: Visual representation of analysis results

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Prerequisites

- Node.js (v14+)
- npm (v6+)
- Python (v3.8+)

## Setup Instructions

### Frontend Setup

```powershell
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

### Backend Setup

```powershell
# Navigate to the backend directory
cd backend

# Install Python dependencies (if Python is installed)
pip install -r requirements.txt
```

## Running the Application

### Using PowerShell Scripts (Recommended for Windows)

1. Run only the frontend:
   ```powershell
   ./run-frontend.ps1
   ```

2. Run both frontend and backend (if Python is installed):
   ```powershell
   ./run-full-app.ps1
   ```

### Manual Method

#### Frontend

```powershell
# Navigate to the frontend directory
cd frontend

# Start the development server
npm run dev
# or
npm start
```

#### Backend

```powershell
# Navigate to the backend directory
cd backend

# Start the backend server
python app_new.py
# or if you have Python 3 explicitly
python3 app_new.py
```

## Troubleshooting

### Python Not Found

If you see the error "Python was not found", you need to install Python:

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. Restart your terminal after installation

### npm Missing Script Error

If you see "Missing script" errors:
1. Check the package.json file in the relevant directory
2. Make sure the script exists in the "scripts" section
3. Run `npm install` to ensure all dependencies are installed

## Application Structure

- `frontend/`: React application with Tailwind CSS
- `backend/`: Python FastAPI backend with machine learning models
- `data/`: Training data and resources for the models

## Features

- **Machine Learning Model**: Trained on the Kaggle Fake and Real News Dataset
- **Modern UI**: Built with React and Tailwind CSS
- **Real-time Analysis**: Instant feedback on news text
- **Confidence Scores**: Percentage-based confidence in the prediction
- **Analysis History**: Track and review previous analyses
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- React.js
- Tailwind CSS
- React Router
- Axios for API calls

### Backend
- Python
- Flask
- Scikit-learn for machine learning
- NLTK for natural language processing

## Installation and Setup

### Prerequisites
- Node.js and npm
- Python 3.7 or higher
- Kaggle account (for downloading the dataset)

### Clone the Repository

```bash
git clone https://github.com/yourusername/fake-news-detection.git
cd fake-news-detection
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000.

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Download the Dataset and Train the Model

```bash
# Download the dataset
python download_dataset.py

# Train the model
python train_model.py
```

This will download the Fake and Real News dataset from Kaggle and train a model. If automatic download fails, follow the instructions provided by the script to download the dataset manually.

### Running the Backend Server

```bash
# Start the Flask server
python app.py
```

The backend API will be available at http://localhost:5000.

## Usage

1. Open the web application in your browser at http://localhost:3000
2. Enter or paste news text into the analysis form
3. Click "Analyze" to process the text
4. View the results showing whether the news is likely "REAL" or "FAKE"
5. Check the confidence score and view your analysis history

## Deployment

### Frontend Deployment

The frontend is built with Vite and can be built for production using:

```bash
cd frontend
npm run build
```

This will create a `dist` directory with production-ready static files that can be deployed to any static hosting service like Netlify, Vercel, or GitHub Pages.

### Backend Deployment

The backend can be deployed to various platforms:

#### Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add a Procfile for Heroku
echo "web: gunicorn app:app" > Procfile

# Deploy to Heroku
git push heroku main
```

#### AWS Elastic Beanstalk

```bash
# Install the EB CLI
pip install awsebcli

# Initialize EB application
eb init

# Create an environment and deploy
eb create
```

## Testing

### Backend Tests

```bash
cd backend
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Kaggle Fake and Real News Dataset](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset) by Clément Bisaillon
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Tailwind CSS](https://tailwindcss.com/) - A utility-first CSS framework
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [Scikit-learn](https://scikit-learn.org/) - Machine learning library for Python 