#!/usr/bin/env python3
"""
Setup script for the Fake News Detection project.
This script guides the user through setting up the project.
"""

import os
import subprocess
import sys
import platform
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {title.center(76)} ")
    print("=" * 80 + "\n")

def run_command(command, description=None, check=True):
    """Run a shell command and print its output."""
    if description:
        print(f"➡️  {description}...")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout.strip())
    
    if result.stderr and check:
        print(f"❌ Error: {result.stderr.strip()}")
        return False
    
    return result.returncode == 0

def check_prerequisites():
    """Check if required tools are installed."""
    print_header("Checking Prerequisites")
    
    # Check Python
    python_version = platform.python_version()
    print(f"✅ Python version: {python_version}")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    # Check Node.js
    if not run_command("node --version", "Checking Node.js", check=False):
        print("❌ Node.js is not installed. Please install Node.js and npm.")
        return False
    
    return True

def setup_frontend():
    """Set up the frontend."""
    print_header("Setting up Frontend")
    
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found")
        return False
    
    # Install frontend dependencies
    os.chdir(frontend_dir)
    if not run_command("npm install", "Installing frontend dependencies"):
        return False
    
    # Go back to the project root
    os.chdir("..")
    return True

def setup_backend():
    """Set up the backend."""
    print_header("Setting up Backend")
    
    backend_dir = os.path.join(os.getcwd(), "backend")
    
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    if not os.path.exists(os.path.join(backend_dir, "venv")):
        print("➡️  Creating virtual environment...")
        os.chdir(backend_dir)
        
        if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            os.chdir("..")
            return False
        
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
        os.chdir(backend_dir)
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    if not run_command(f"{activate_cmd} && pip install -r requirements.txt", "Installing backend dependencies"):
        os.chdir("..")
        return False
    
    # Go back to project root
    os.chdir("..")
    return True

def download_dataset():
    """Download the dataset."""
    print_header("Downloading Dataset")
    
    backend_dir = os.path.join(os.getcwd(), "backend")
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    os.chdir(backend_dir)
    
    if not run_command(f"{activate_cmd} && python download_dataset.py", "Downloading dataset"):
        print("❗ Automatic download failed. You may need to download the dataset manually.")
        print("   Please follow the instructions in the README.md file.")
    
    os.chdir("..")
    return True

def train_model():
    """Train the model."""
    print_header("Training Model")
    
    backend_dir = os.path.join(os.getcwd(), "backend")
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    os.chdir(backend_dir)
    
    if not run_command(f"{activate_cmd} && python train_model.py", "Training model"):
        print("❌ Model training failed")
        os.chdir("..")
        return False
    
    os.chdir("..")
    return True

def main():
    """Main function."""
    print_header("Fake News Detection System Setup")
    
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install the required tools and try again.")
        return
    
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        return
    
    if not setup_backend():
        print("\n❌ Backend setup failed")
        return
    
    if not download_dataset():
        print("\n❗ Dataset download may have failed, but you can continue.")
    
    if not train_model():
        print("\n❌ Model training failed")
        return
    
    print_header("Setup Complete")
    print("You can now run the application:")
    print("\nFrontend:")
    print("  cd frontend")
    print("  npm run dev")
    print("\nBackend:")
    print("  cd backend")
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    print("  python app.py")
    print("\nOr use Docker Compose:")
    print("  docker-compose up")
    print("\nVisit http://localhost:3000 in your browser")

if __name__ == "__main__":
    main() 