#!/usr/bin/env python
"""
Script to run the FastAPI server.
Execute: python run.py
"""

import uvicorn
import os

if __name__ == "__main__":
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )
