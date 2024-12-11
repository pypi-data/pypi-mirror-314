# llmchatlinker/main.py

import os
import threading
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from .orchestrator import Orchestrator
from .api import app

# Configure CORS settings for the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins
    allow_credentials=True,    # Allow credentials
    allow_methods=["*"],       # Allow all HTTP methods
    allow_headers=["*"],       # Allow all HTTP headers
)

def start_orchestrator():
    """Initialize and start the orchestrator."""
    orchestrator = Orchestrator()
    orchestrator.start()

if __name__ == "__main__":
    # Start the orchestrator in a separate daemon thread
    orchestrator_thread = threading.Thread(target=start_orchestrator, daemon=True)
    orchestrator_thread.start()

    print("Starting FastAPI server")
    
    # Run the FastAPI app with Uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)