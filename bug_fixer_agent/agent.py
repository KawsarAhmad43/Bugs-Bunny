# bug_fixer_agent/agent.py
import time
import os
from typing import Dict, Tuple
from google import genai
from google.genai import types
from bug_fixer_agent.config import Config
from bug_fixer_agent.logger import Logger
from bug_fixer_agent.prompts import Prompts
from bug_fixer_agent.tools.code_analyzer import CodeAnalyzer
import re

class BugFixerAgent:
    def __init__(self, config: Config, logger: Logger, prompts: Prompts):
        self.config = config
        self.logger = logger
        self.prompts = prompts
        self.code_analyzer = CodeAnalyzer(logger) # Still useful for analysis context

        try:
            self.logger.info("Configuring Google GenAI client...")
            self.client = genai.Client(api_key=self.config.api_key)
            self.logger.info("Google GenAI client configured successfully.")
        except Exception as e:
            self.logger.error(f"Failed to configure Google GenAI client: {e}")
            raise

    def analyze_bug(self, bug_name: str, codebase_content: str) -> Dict:
        """
        Performs comprehensive bug analysis including static analysis and context understanding.
        """
        self.logger.info(f"Analyzing bug: '{bug_name}'")
        
        bug_info = self.prompts.bug_defs.get_bug_by_name(bug_name) # This correctly retrieves bug details
        if not bug_info:
            return {"error": f"Bug '{bug_name}' not found in definitions"}
        
        # Perform static analysis on affected files
        analysis_results = {}
        for file_path in bug_info.get("files", []):
            try:
                # Use absolute path to file for analysis, as code_analyzer expects it
                abs_file_path = os.path.join(self.config.project_root, file_path)
                analysis_results[file_path] = self.code_analyzer.analyze_file(abs_file_path)
            except Exception as e:
                self.logger.warning(f"Could not analyze file {file_path}: {e}")
                analysis_results[file_path] = {"error": str(e)}
        
        return {
            "bug_info": bug_info, # This is correctly packaged here
            "static_analysis": analysis_results,
            "context": codebase_content
        }

    def generate_fix(self, bug_name: str, codebase_content: str) -> Tuple[str, Dict]:
        """
        Generates a code solution for a given bug using the Gemini 2.5 Flash model.
        Returns the corrected code snippet(s) as a string and analysis metadata.
        """
        self.logger.info(f"Generating fix for bug: '{bug_name}'")
        
        # First, analyze the bug
        analysis = self.analyze_bug(bug_name, codebase_content) # This returns the dict with 'bug_info'
        if "error" in analysis:
            return "", {"error": analysis["error"]}
        
        # Generate enhanced prompt with analysis context
        try:
            prompt = self.prompts.generate_enhanced_prompt(bug_name, codebase_content, analysis)
        except Exception as e:
            self.logger.error(f"Error generating prompt for {bug_name}: {e}")
            return "", {"error": f"Error generating prompt: {e}"}
        
        if "Error:" in prompt or not prompt.strip():
            self.logger.error(f"Could not generate a valid prompt for {bug_name}: {prompt}")
            return "", {"error": "Invalid prompt generated"}

        generated_code_snippet = ""
        for attempt in range(self.config.max_retries):
            try:
                self.logger.info(f"Calling Gemini API (Attempt {attempt + 1}/{self.config.max_retries})...")
                
                response = self.client.models.generate_content(
                    model=self.config.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=self.config.temperature,
                        max_output_tokens=self.config.max_output_tokens,
                        top_p=self.config.top_p,
                        top_k=self.config.top_k,
                    )
                )
                
                if not response or not response.text:
                    self.logger.warning(f"Empty response from API for '{bug_name}' on attempt {attempt + 1}")
                    if attempt == self.config.max_retries - 1:
                        self.logger.error("Max retries reached. No response from API.")
                        return "", {"error": "No response from API after max retries"}
                    time.sleep(2)
                    continue
                
                generated_code_snippet = response.text.strip()
                
                # Basic validation: ensure it looks like a code snippet with file headers
                if not self._validate_code_snippet_format(generated_code_snippet):
                    self.logger.warning(f"Invalid code snippet format for '{bug_name}' on attempt {attempt + 1}")
                    if attempt == self.config.max_retries - 1:
                        self.logger.error("Max retries reached. No valid code snippet generated.")
                        return "", {"error": "No valid code snippet generated after max retries"}
                    time.sleep(2)
                    continue
                
                self.logger.info("Successfully generated a valid code snippet from the API.")
                
                return generated_code_snippet, {
                    "bug_name": bug_name,
                    "analysis": analysis, # <-- This 'analysis' is the full dict containing 'bug_info'
                    "attempts": attempt + 1,
                    "model_used": self.config.model_name
                }

            except Exception as e:
                self.logger.error(f"API call error on attempt {attempt + 1} for bug '{bug_name}': {e}")
                if attempt < self.config.max_retries - 1:
                    self.logger.info("Retrying...")
                    time.sleep(2)
                else:
                    self.logger.error("Max retries reached. Failed to generate fix.")
                    return "", {"error": f"API call failed: {str(e)}"}
        
        return "", {"error": "Failed to generate fix after all retries"}

    def _validate_code_snippet_format(self, code_content: str) -> bool:
        """
        Basic validation to ensure the generated content looks like the expected code snippet format.
        Checks for "File: <path>" and code block markers.
        """
        if not code_content.strip():
            return False
        
        # Check for at least one "File: <path>" line
        if not re.search(r'^File: .*', code_content, re.MULTILINE):
            return False
        
        # Check for presence of markdown code blocks
        if not (code_content.count('```') >= 2):
            # This is a soft check. If the model sometimes omits them, it's still code.
            # But the prompt explicitly asks for them, so we prefer to enforce this.
            self.logger.warning("Generated code snippet might be missing markdown code block fences.")

        return True


    def get_fix_summary(self, bug_name: str, corrected_code_snippet: str, analysis_metadata: Dict) -> Dict: # Renamed 'analysis' to 'analysis_metadata' for clarity
        """
        Generates a comprehensive summary of the fix including root cause analysis.
        This now includes the corrected code snippet directly.
        """
        # Retrieve the original analysis dict (which contains 'bug_info') from analysis_metadata
        original_analysis_dict = analysis_metadata.get("analysis", {})
        bug_info = original_analysis_dict.get("bug_info", {}) # <-- CORRECTED RETRIEVAL HERE
        
        # Extract files affected from the code snippet itself, if not already in bug_info
        files_affected = bug_info.get("files", [])
        if not files_affected:
            # Try to parse from the snippet if bug_info was missing it (fallback)
            detected_files = re.findall(r'^File: (.*)', corrected_code_snippet, re.MULTILINE)
            files_affected = list(set(detected_files))

        return {
            "bug_name": bug_name,
            "description": bug_info.get("description", ""),
            "root_cause": bug_info.get("root_cause", ""), # Will now be correctly populated
            "fix_summary": bug_info.get("fix_summary", "Solution provided as code snippet."),
            "files_affected": files_affected,
            "corrected_code_snippet": corrected_code_snippet,
            "analysis_metadata": analysis_metadata # Keep the full metadata
        }

    def generate_failure_analysis_and_suggestions(self, bug_name: str, original_error_message: str, previous_ai_generated_code: str, codebase_content: str) -> Dict:
        """
        Consults the LLM to get an analysis and possible solutions for a failed bug fix.
        """
        self.logger.info(f"Generating failure analysis for bug '{bug_name}'...")
        
        # Extract relevant code from the codebase_content for the prompt
        bug_info = self.prompts.bug_defs.get_bug_by_name(bug_name)
        files_to_check = bug_info["files"] if bug_info else []
        relevant_context = self.prompts._extract_relevant_files(codebase_content, files_to_check)

        prompt = self.prompts.generate_failure_analysis_prompt(
            bug_name=bug_name,
            original_error_message=original_error_message,
            previous_ai_generated_code=previous_ai_generated_code,
            relevant_context_code=relevant_context
        )

        for attempt in range(self.config.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.config.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3, # Slightly higher temperature for more creative suggestions
                        max_output_tokens=self.config.max_output_tokens, # Allow full code solution
                        top_p=self.config.top_p,
                        top_k=self.config.top_k,
                    )
                )

                if response and response.text:
                    self.logger.info(f"Generated failure analysis for {bug_name} (Attempt {attempt + 1}).")
                    return {"analysis": response.text.strip(), "success": True}
                
                self.logger.warning(f"Empty response for failure analysis on attempt {attempt + 1}")
                time.sleep(1) # Short delay before retry

            except Exception as e:
                self.logger.error(f"API call error for failure analysis on attempt {attempt + 1}: {e}")
                time.sleep(1) # Short delay before retry

        self.logger.error(f"Failed to generate failure analysis after {self.config.max_retries} attempts.")
        return {"analysis": "Failed to generate intelligent suggestions due to API error."}