from bug_fixer_agent.config import Config

class FixApplier:
    def __init__(self):
        self.config = Config()

    def apply_fix(self, fix_patch):
        with open("codebase_content.txt", "r") as f:
            content = f.read()
        if fix_patch and any(path in fix_patch for path in ["backend/", "frontend/"]):
            with open("codebase_content.txt", "w") as f:
                f.write(content + "\n" + fix_patch)
        return True