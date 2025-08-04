from bug_fixer_agent.bug_definitions import BugDefinitions

class BugDetector:
    def __init__(self):
        self.bug_defs = BugDefinitions()

    def detect_bugs(self, codebase_content):
        bugs = []
        for bug in self.bug_defs.get_all_bugs():
            bug_full_name = f"{bug['name']}: {bug['description']}"
            if any(pattern in codebase_content for pattern in bug['patterns']):
                bugs.append(bug_full_name)
        return bugs