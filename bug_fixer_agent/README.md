# Bug Fixer Agent

A tool to automatically detect and generate solutions for planted bugs in a codebase using AI.

# Updated Project Folder Structure
```bash
SAMPLE_PROJECT-MASTER/
├── .pytest_cache/
├── .ruff_cache/
├── backend/
├── bug_fixer_agent/
│   ├── __pycache__/
│   ├── tools/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── bug_detector.py
│   │   ├── code_analyzer.py
│   │   ├── fix_applier.py
│   │   ├── static_analyzer.py
│   ├── __init__.py
│   ├── .env
│   ├── agent.py
│   ├── bug_definitions.py
│   ├── config.py
│   ├── logger.py
│   ├── prompts.py
│   ├── README.md
│   ├── requirements.txt
│   └── run.py
├── frontend/
├── tests/
├── venv/
├── .cz.toml
├── .gitignore
├── .pre-commit-config.yml
├── .python-version
├── BOT_REQUIREMENTS.md
├── bug_fix_report.txt
├── inspector.py
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## Installation and Run Process

Follow these step-by-step instructions to set up and run the Bug Fixer Agent:

### 1. Create a Virtual Environment
- Open a terminal in the project root directory (`C:\Users\ASUS\Downloads\sample_project-master`).
- Run the following command to create a virtual environment:
  ```
  python -m venv venv
  ```

### 2. Activate the Virtual Environment
- On Windows, activate the virtual environment by running:
  ```
  .\venv\Scripts\activate
  ```
  - You should see `(venv)` prefixed to your terminal prompt, e.g., `(venv) PS C:\Users\ASUS\Downloads\sample_project-master>`.

### 3. Install Requirements
- Ensure the `requirements.txt` file is located in the `bug_fixer_agent` folder within the root directory.
- Install the dependencies listed in `requirements.txt` by running:
  ```
  pip install -r bug_fixer_agent/requirements.txt
  ```

### 4. Set API Key
- Set your Google GenAI API key as an environment variable in the active virtual environment:
  ```
  set GOOGLE_API_KEY=your_api_key_here
  ```
  - Replace `your_api_key_here` with your actual API key.

### 5. Run the Project
- Execute the script using the module command from the root directory:
  ```
  python -m bug_fixer_agent.run
  ```
- The project will start processing, and you should see logs similar to the following:
  ```
  (venv) PS C:\Users\ASUS\Downloads\sample_project-master-updated\sample_project-master-updated> python -m bug_fixer_agent.run
  2025-08-03 20:44:18 - BugFixerAgent - INFO - Configuring Google GenAI client...
  2025-08-03 20:44:18 - BugFixerAgent - INFO - Google GenAI client configured successfully.
  2025-08-03 20:44:18 - BugFixerAgent - INFO - Bug Fixer Agent process started.
  2025-08-03 20:44:18 - BugFixerAgent - INFO - Setting up environment...
  2025-08-03 20:44:18 - BugFixerAgent - INFO - Installing agent dependencies from C:\Users\ASUS\Downloads\sample_project-master-updated\sample_project-master-updated\bug_fixer_agent\requirements.txt...
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Agent dependencies installed successfully.
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Inspecting the codebase to create context file ('codebase_content.txt')...
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Codebase inspection complete.
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Loaded codebase content (29333 characters)
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Starting to process 5 planted bugs...

  --- Processing: State Management Bug ---
  Generating Solutions:   0%|                                                                                                      | 0/5 [00:00<?, ?it/s]2025-08-03 20:44:22 - BugFixerAgent - INFO - Processing bug: State Management Bug
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Generating fix for bug: 'State Management Bug'
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Analyzing bug: 'State Management Bug'
  2025-08-03 20:44:22 - BugFixerAgent - INFO - Calling Gemini API (Attempt 1/5)...
  2025-08-03 20:44:40 - BugFixerAgent - INFO - Successfully generated a valid code snippet from the API.
  Status: SOLUTION_GENERATED
  Successfully generated a code solution.

  --- Processing: CSRF Token Bug ---
  Generating Solutions:  20%|██████████████████▊                                                                           | 1/5 [00:18<01:12, 18.15s/it]2025-08-03 20:44:40 - BugFixerAgent - INFO - Processing bug: CSRF Token Bug
  2025-08-03 20:44:40 - BugFixerAgent - INFO - Generating fix for bug: 'CSRF Token Bug'
  2025-08-03 20:44:40 - BugFixerAgent - INFO - Analyzing bug: 'CSRF Token Bug'
  2025-08-03 20:44:40 - BugFixerAgent - INFO - Calling Gemini API (Attempt 1/5)...
  2025-08-03 20:44:53 - BugFixerAgent - INFO - Successfully generated a valid code snippet from the API.
  Status: SOLUTION_GENERATED
  Successfully generated a code solution.

  --- Processing: Permission Bug ---
  Generating Solutions:  40%|█████████████████████████████████████▌                                                        | 2/5 [00:30<00:44, 14.88s/it]2025-08-03 20:44:53 - BugFixerAgent - INFO - Processing bug: Permission Bug
  2025-08-03 20:44:53 - BugFixerAgent - INFO - Generating fix for bug: 'Permission Bug'
  2025-08-03 20:44:53 - BugFixerAgent - INFO - Analyzing bug: 'Permission Bug'
  2025-08-03 20:44:53 - BugFixerAgent - INFO - Calling Gemini API (Attempt 1/5)...
  2025-08-03 20:44:57 - BugFixerAgent - INFO - Successfully generated a valid code snippet from the API.
  Status: SOLUTION_GENERATED
  Successfully generated a code solution.

  --- Processing: React useEffect Bug ---
  Generating Solutions:  60%|████████████████████████████████████████████████████████▍                                     | 3/5 [00:34<00:19,  9.92s/it]2025-08-03 20:44:57 - BugFixerAgent - INFO - Processing bug: React useEffect Bug
  2025-08-03 20:44:57 - BugFixerAgent - INFO - Generating fix for bug: 'React useEffect Bug'
  2025-08-03 20:44:57 - BugFixerAgent - INFO - Analyzing bug: 'React useEffect Bug'
  2025-08-03 20:44:57 - BugFixerAgent - INFO - Calling Gemini API (Attempt 1/5)...
  2025-08-03 20:45:05 - BugFixerAgent - INFO - Successfully generated a valid code snippet from the API.
  Status: SOLUTION_GENERATED
  Successfully generated a code solution.

  --- Processing: API Integration Bug ---
  Generating Solutions:  80%|███████████████████████████████████████████████████████████████████████████▏                  | 4/5 [00:42<00:09,  9.12s/it]2025-08-03 20:45:05 - BugFixerAgent - INFO - Processing bug: API Integration Bug
  2025-08-03 20:45:05 - BugFixerAgent - INFO - Generating fix for bug: 'API Integration Bug'
  2025-08-03 20:45:05 - BugFixerAgent - INFO - Analyzing bug: 'API Integration Bug'
  2025-08-03 20:45:05 - BugFixerAgent - INFO - Calling Gemini API (Attempt 1/5)...
  2025-08-03 20:45:12 - BugFixerAgent - INFO - Successfully generated a valid code snippet from the API.
  Status: SOLUTION_GENERATED
  Successfully generated a code solution.
  Generating Solutions: 100%|██████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:50<00:00, 10.09s/it] 
  2025-08-03 20:45:12 - BugFixerAgent - INFO - Bug solution generation process complete. Report saved to 'C:\Users\ASUS\Downloads\sample_project-master-updated\sample_project-master-updated\bug_fix_report.txt'.
  2025-08-03 20:45:12 - BugFixerAgent - INFO - Total time: 54.00 seconds
  2025-08-03 20:45:12 - BugFixerAgent - INFO - Success rate (solution generation): 100.0%
  2025-08-03 20:45:13 - BugFixerAgent - INFO - Cleaned up codebase_content.txt

  🎉 ALL BUG SOLUTIONS SUCCESSFULLY GENERATED! Review 'bug_fix_report.txt'.
  ```

- After successful execution, review the generated `bug_fix_report.txt` in the root directory for detailed bug fixes and suggestions.

### Notes
- Ensure the Google GenAI API key is valid and properly set before running the script.
- If any step fails, check the terminal output or logs for specific error messages and troubleshoot accordingly.