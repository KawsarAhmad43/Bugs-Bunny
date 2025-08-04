import os
import subprocess
import sys
from datetime import datetime
from tqdm import tqdm
from typing import Dict, List

# Adjust path to import from the agent's directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bug_fixer_agent.bug_definitions import BugDefinitions
from bug_fixer_agent.agent import BugFixerAgent
from bug_fixer_agent.config import Config
from bug_fixer_agent.logger import Logger
from bug_fixer_agent.prompts import Prompts
# Removed imports for FilePatcher and TestRunner

class BugFixerRunner:
    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.prompts = Prompts()
        self.agent = BugFixerAgent(self.config, self.logger, self.prompts)
        # self.patcher = FilePatcher(self.config, self.logger) # Removed
        # self.code_analyzer = CodeAnalyzer(self.logger) # No longer need a separate instance here
        self.bug_defs = BugDefinitions() # <-- Re-added this line
        
        # Results tracking
        self.results = {
            "start_time": datetime.now().isoformat(),
            "bugs_processed": 0,
            "bugs_fixed": 0, # Renamed to solutions_generated
            "bugs_failed": 0,
            "total_time": 0,
            "solutions": [] # Renamed from 'fixes' to 'solutions'
        }

    def setup_environment(self) -> bool:
        """
        Sets up the environment and ensures necessary context files are generated.
        """
        try:
            self.logger.info("Setting up environment...")
            
            # Install agent dependencies
            req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
            self.logger.info(f"Installing agent dependencies from {req_path}...")
            # Use --no-warn-script-location to suppress warnings about scripts not being in PATH
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path, "--upgrade", "--no-warn-script-location"], 
                          check=True, capture_output=True)
            self.logger.info("Agent dependencies installed successfully.")
            
            # Inspect codebase to create context file
            self.logger.info("Inspecting the codebase to create context file ('codebase_content.txt')...")
            inspector_path = os.path.join(self.config.project_root, "inspector.py")
            # Ensure the inspector.py is run from the project root directory
            subprocess.run([sys.executable, inspector_path, "-d", "."], 
                           check=True, capture_output=True, cwd=self.config.project_root)
            self.logger.info("Codebase inspection complete.")
            
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.logger.error(f"Failed to setup environment: {e}")
            self.logger.error(f"Stdout/Stderr:\n{getattr(e, 'stdout', 'N/A')}\n{getattr(e, 'stderr', 'N/A')}")
            return False

    def load_codebase_content(self) -> str:
        """
        Loads the codebase content from the generated file.
        """
        codebase_content_path = os.path.join(self.config.project_root, "codebase_content.txt")
        
        if not os.path.exists(codebase_content_path):
            self.logger.error(f"Codebase content file not found: {codebase_content_path}")
            return ""
        
        try:
            with open(codebase_content_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.logger.info(f"Loaded codebase content ({len(content)} characters)")
            return content
        except Exception as e:
            self.logger.error(f"Error loading codebase content: {e}")
            return ""

    def process_bug(self, bug: Dict, codebase_content: str) -> Dict:
        """
        Processes a single bug by generating a code solution.
        """
        bug_name = bug["name"]
        self.logger.info(f"Processing bug: {bug_name}")
        
        result_payload = {
            "bug_name": bug_name,
            "status": "initial", # Will be updated
            "error": "",
            "generated_code_solution": "", # New field for the generated code
            "ai_suggestions": "" 
        }

        try:
            # Generate code solution
            corrected_code_snippet, analysis_metadata = self.agent.generate_fix(bug_name, codebase_content)
            result_payload["generated_code_solution"] = corrected_code_snippet
            
            if not corrected_code_snippet:
                result_payload["status"] = "failed_to_generate_solution"
                result_payload["error"] = analysis_metadata.get("error", "No code solution generated.")
            else:
                result_payload["status"] = "solution_generated"
                # For this new mode, "fixed" means a solution was successfully generated.
                result_payload["fix_summary"] = self.agent.get_fix_summary(bug_name, corrected_code_snippet, analysis_metadata)
                
        except Exception as e:
            self.logger.error(f"Error processing bug {bug_name}: {e}")
            result_payload["status"] = "error"
            result_payload["error"] = str(e)

        # If fix failed for any reason, generate AI-driven suggestions
        if result_payload["status"] != "solution_generated":
            suggestion_response = self.agent.generate_failure_analysis_and_suggestions(
                bug_name=bug_name,
                original_error_message=result_payload["error"],
                previous_ai_generated_code=result_payload["generated_code_solution"],
                codebase_content=codebase_content # Pass full content for broader context
            )
            if suggestion_response["success"]:
                result_payload["ai_suggestions"] = suggestion_response["analysis"]
            else:
                result_payload["ai_suggestions"] = "Could not generate intelligent suggestions due to API error."

        return result_payload

    def generate_report(self, bug_results: List[Dict]) -> str:
        """
        Generates a comprehensive bug fix report.
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("BUG FIXER AGENT REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Model Used: {self.config.model_name}")
        report_lines.append(f"Total Bugs Processed: {len(bug_results)}")
        report_lines.append("")
        
        # Summary statistics
        solution_generated_count = sum(1 for r in bug_results if r["status"] == "solution_generated")
        failed_count = len(bug_results) - solution_generated_count
        
        report_lines.append("SUMMARY:")
        report_lines.append(f"- Solutions Successfully Generated: {solution_generated_count}")
        report_lines.append(f"- Failures (No Solution/Invalid Solution): {failed_count}")
        report_lines.append(f"- Success Rate (Solution Generation): {(solution_generated_count/len(bug_results)*100):.1f}%")
        report_lines.append("")
        
        # Detailed results for each bug
        for i, result in enumerate(bug_results, 1):
            report_lines.append(f"BUG {i}: {result['bug_name']}")
            report_lines.append(f"Status: {result['status'].upper()}")
            report_lines.append("-" * 40)
            
            if result["status"] == "solution_generated":
                fix_summary = result.get("fix_summary", {})
                report_lines.append(f"Root Cause: {fix_summary.get('root_cause', 'Not specified')}")
                report_lines.append(f"Proposed Fix Concept: {fix_summary.get('fix_summary', 'Not specified')}")
                report_lines.append(f"Files Affected: {', '.join(fix_summary.get('files_affected', []))}")
                report_lines.append("\n--- GENERATED CODE SOLUTION ---")
                report_lines.append(result["generated_code_solution"])
                report_lines.append("-------------------------------")

            else: # If status is failed_to_generate_solution or error
                report_lines.append(f"Error: {result.get('error', 'Unknown error')}")
                if "generated_code_solution" in result and result["generated_code_solution"]:
                    report_lines.append("\n--- ATTEMPTED CODE SOLUTION ---")
                    report_lines.append(result["generated_code_solution"])
                    report_lines.append("-------------------------------")
                else:
                    report_lines.append("\nNo code solution was generated in the initial attempt.")

                # Display AI-generated suggestions (which should contain the improved code)
                if result.get("ai_suggestions"):
                    report_lines.append("\n--- AI-GENERATED FAILURE ANALYSIS AND IMPROVED SOLUTION ---")
                    report_lines.append(result["ai_suggestions"])
                    report_lines.append("---------------------------------------------------------")
                else:
                    report_lines.append("\nNo specific AI-generated suggestions available for this failure.")

            report_lines.append("")
        
        # Technical details
        report_lines.append("TECHNICAL DETAILS:")
        report_lines.append(f"- Model: {self.config.model_name}")
        report_lines.append(f"- Temperature: {self.config.temperature}")
        report_lines.append(f"- Max Output Tokens: {self.config.max_output_tokens}")
        report_lines.append(f"- Max Retries: {self.config.max_retries}")
        report_lines.append("")
        
        # General recommendations (these are still hardcoded, as they are system-level suggestions)
        report_lines.append("GENERAL RECOMMENDATIONS:")
        if failed_count > 0:
            report_lines.append("- Review the 'AI-GENERATED FAILURE ANALYSIS AND IMPROVED SOLUTION' for failed bugs.")
            report_lines.append("- Ensure the environment is correctly set up and dependencies are met.")
            report_lines.append("- Consult agent logs for further details on API errors.")
            report_lines.append("- Refine bug definitions or prompt hints if solutions are consistently incorrect.")
        else:
            report_lines.append("- All bug solutions successfully generated! Review them for accuracy.")
            report_lines.append("- Manually apply the generated code snippets to your codebase.")
            report_lines.append("- Thoroughly test the application after applying changes.")
            report_lines.append("- Consider a code review for quality assurance before deploying.")
        
        return "\n".join(report_lines)

    def run(self) -> bool:
        """
        Main execution method for the Bug Fixer Agent.
        """
        start_time = datetime.now()
        self.logger.info("Bug Fixer Agent process started.")
        
        # Setup environment
        if not self.setup_environment():
            self.logger.error("Failed to setup environment. Exiting.")
            return False
        
        # Load codebase content
        codebase_content = self.load_codebase_content()
        if not codebase_content:
            self.logger.error("Failed to load codebase content. Exiting.")
            return False
        
        # Get bugs to process
        bugs_to_fix = self.bug_defs.get_all_bugs()
        self.logger.info(f"Starting to process {len(bugs_to_fix)} planted bugs...")
        
        # Process each bug
        bug_results = []
        for bug in tqdm(bugs_to_fix, desc="Generating Solutions"):
            bug_name = bug["name"]
            tqdm.write(f"\n--- Processing: {bug_name} ---")
            
            result = self.process_bug(bug, codebase_content)
            bug_results.append(result)
            
            # Update statistics
            self.results["bugs_processed"] += 1
            if result["status"] == "solution_generated":
                self.results["bugs_fixed"] += 1 # Accumulate successful generations
            else:
                self.results["bugs_failed"] += 1
            
            # Print immediate status
            status = result["status"].upper()
            tqdm.write(f"Status: {status}")
            
            if result["status"] == "solution_generated":
                tqdm.write("Successfully generated a code solution.")
            else:
                tqdm.write(f"Generation failed. Error: {result.get('error', 'Unknown error')}")
                if result.get("ai_suggestions"):
                    tqdm.write("AI-Generated Analysis & Suggestions provided in report.")
        
        # Calculate total time
        end_time = datetime.now()
        self.results["total_time"] = (end_time - start_time).total_seconds()
        
        # Generate and save report
        report_content = self.generate_report(bug_results)
        report_path = os.path.join(self.config.project_root, "bug_fix_report.txt")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        self.logger.info(f"Bug solution generation process complete. Report saved to '{report_path}'.")
        self.logger.info(f"Total time: {self.results['total_time']:.2f} seconds")
        self.logger.info(f"Success rate (solution generation): {(self.results['bugs_fixed']/self.results['bugs_processed']*100):.1f}%")
        
        # Cleanup
        codebase_content_path = os.path.join(self.config.project_root, "codebase_content.txt")
        if os.path.exists(codebase_content_path):
            os.remove(codebase_content_path)
            self.logger.info("Cleaned up codebase_content.txt")
        
        return self.results["bugs_failed"] == 0

def main():
    """Main execution script for the Bug Fixer Agent."""
    runner = BugFixerRunner()
    success = runner.run()
    
    if success:
        print("\n🎉 ALL BUG SOLUTIONS SUCCESSFULLY GENERATED! Review 'bug_fix_report.txt'.")
        sys.exit(0)
    else:
        print("\n❌ SOME BUG SOLUTIONS FAILED TO GENERATE. Check 'bug_fix_report.txt' for details and AI suggestions.")
        sys.exit(1)

if __name__ == "__main__":
    main()