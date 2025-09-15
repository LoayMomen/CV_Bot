#!/usr/bin/env python3
"""
Setup script for CV_Bot development environment
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and handle errors"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def setup_backend():
    """Set up backend environment"""
    print("Setting up backend...")
    backend_dir = Path("backend")

    # Install Python dependencies
    run_command("pip install -r requirements.txt", cwd=backend_dir)

    print("Backend setup complete!")

def setup_frontend():
    """Set up frontend environment"""
    print("Setting up frontend...")
    frontend_dir = Path("frontend")

    # Install Node dependencies
    run_command("npm install", cwd=frontend_dir)

    print("Frontend setup complete!")

def setup_database():
    """Set up database"""
    print("Setting up database...")

    # Check if Docker is available
    docker_check = run_command("docker --version", check=False)
    if docker_check.returncode == 0:
        print("Starting database with Docker...")
        run_command("docker-compose up -d postgres redis", cwd="backend")
    else:
        print("Docker not found. Please install PostgreSQL and Redis manually.")
        print("See DEVELOPMENT.md for manual setup instructions.")

def main():
    """Main setup function"""
    print("Setting up CV_Bot development environment...")

    # Check if we're in the right directory
    if not Path("mvp.md").exists():
        print("Please run this script from the CV_Bot root directory")
        sys.exit(1)

    # Setup components
    setup_backend()
    setup_frontend()
    setup_database()

    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your API keys")
    print("2. Run 'cd backend && python run.py' to start the backend")
    print("3. Run 'cd frontend && npm run dev' to start the frontend")
    print("4. Visit http://localhost:3000 to see the application")

if __name__ == "__main__":
    main()