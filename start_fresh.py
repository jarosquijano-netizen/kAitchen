import os
import sys

# Force clear any cached database connections
os.environ['DATABASE_URL'] = 'sqlite:///family_kitchen.db'

# Add current directory to Python path to ensure fresh imports
sys.path.insert(0, os.getcwd())

print("🔄 Starting fresh Flask server...")

# Import and start app
from app import app

if __name__ == '__main__':
    print("🚀 Starting k[AI]tchen with fresh database connection...")
    app.run(debug=True, host='0.0.0.0', port=7000)
