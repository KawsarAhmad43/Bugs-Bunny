# bug_fixer_agent/config.py
import os
from datetime import datetime
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not found. Please set it in the .env file.")
        
        # Updated to use a stable and available model with correct prefix
        self.model_name = "models/gemini-2.5-flash"
        self.max_retries = 5
        self.timeout = 120
        self.run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Enhanced configuration for better performance
        self.temperature = 0.1  # Low temperature for consistent code generation
        self.max_output_tokens = 16384  # Increased for larger patches
        self.top_p = 0.8
        self.top_k = 40
        
        # Project paths
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.backend_path = os.path.join(self.project_root, "backend")
        self.frontend_path = os.path.join(self.project_root, "frontend")