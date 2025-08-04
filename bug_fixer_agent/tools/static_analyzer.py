import subprocess
import os
from bug_fixer_agent.config import Config

class StaticAnalyzer:
    def __init__(self):
        self.config = Config()

    def analyze(self, codebase_content):
        try:
            with open("temp_code.py", "w") as f:
                f.write(codebase_content)
            result = subprocess.run([self.config.static_analysis_tools["python"], "temp_code.py"], capture_output=True, text=True)
            os.remove("temp_code.py")
            return result.returncode == 0
        except Exception:
            return False