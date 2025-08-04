# inspector.py (Updated to ignore itself and agent files more broadly)
import os
import argparse
from pathlib import Path
import pathspec

# --- Constants for styling the output ---
HEADER_LINE = "*" * 100
FILE_SEPARATOR = "\n\n"

# --- Default patterns to ALWAYS ignore, in addition to .gitignore ---
# This provides a robust baseline for any project.
DEFAULT_IGNORE_PATTERNS = [
    # Version control
    ".git/",
    # Python virtual environments
    ".venv/",
    "venv/",
    # Python caches
    "__pycache__/",
    "*.pyc",
    # Environment variables
    ".env",
    ".env.*",
    # Dependency lock files
    "uv.lock",
    "poetry.lock",
    "Pipfile.lock",
    "package-lock.json",
    "yarn.lock",
    ".pytest_cache/",
    ".ruff_cache/",
    "bug_fixer_agent/",
    "BOT_REQUIREMENTS.md",
    ".pre-commit-config.yml",
    "tests/",
    "inspector.py",
    "README.md",
    "pyproject.toml",
    "uv.lock",
    ".cz.toml",
    "requirements.txt",
    # Markdown and other supported script (do not ignore if they are project docs like BOT_REQUIREMENTS.md)
    # "README.md", # Keep README as it might contain setup instructions
    "inspector.py", # Add inspector.py itself to ignore
    "bug_fix_report.txt", # Add report file to ignore
    "codebase_content.txt", # Add generated context file to ignore

    # Common metadata/config
    ".gitignore",
    "LICENSE",
    "license",
    # IDE folders
    ".vscode/",
    ".idea/",
    
    # Exclude the entire bug_fixer_agent directory and its content
    "bug_fixer_agent/", 
    "node_modules/", # Common for frontend
    "db.sqlite3", # Django default DB

    
]


def get_gitignore_spec(
    directory: Path, output_filename: str
) -> pathspec.PathSpec:
    """
    Combines default ignore patterns with patterns from the project's
    .gitignore file.
    """
    gitignore_file = directory / ".gitignore"
    project_patterns = []
    if gitignore_file.is_file():
        with open(gitignore_file, "r", encoding="utf-8") as f:
            project_patterns = f.readlines()

    # Combine default patterns with project-specific .gitignore patterns
    # Ensure the script's own output file is ignored.
    all_patterns = DEFAULT_IGNORE_PATTERNS + [output_filename] + project_patterns
    return pathspec.PathSpec.from_lines("gitwildmatch", all_patterns)


def process_directory(
    root_dir: str, output_file: str, spec: pathspec.PathSpec
):
    """
    Walks through the directory, reads non-ignored files, and writes their
    content to the output file.
    """
    root_path = Path(root_dir).resolve()
    output_path = Path(output_file).resolve()
    files_processed = 0

    print(f"Starting to process directory: {root_path}")
    print(f"Output will be saved to: {output_path}")
    print("Ignoring files based on .gitignore and a default list.")

    with open(output_path, "w", encoding="utf-8") as outfile:
        for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
            current_path = Path(dirpath)

            # Filter out ignored directories so os.walk doesn't descend into them
            # Must modify dirnames in place
            dirnames[:] = [d for d in dirnames if not spec.match_file(str((current_path / d).relative_to(root_path)).replace("\\", "/") + "/")]

            for filename in filenames:
                full_file_path = current_path / filename
                relative_file_path = full_file_path.relative_to(root_path)
                relative_file_path_str = str(relative_file_path).replace(
                    "\\", "/"
                )

                if not spec.match_file(relative_file_path_str):
                    try:
                        with open(
                            full_file_path, "r", encoding="utf-8"
                        ) as infile:
                            content = infile.read()

                        outfile.write(f"{HEADER_LINE}\n")
                        outfile.write(f"File: {relative_file_path_str}\n")
                        outfile.write(f"{HEADER_LINE}\n\n")
                        outfile.write(content)
                        outfile.write(FILE_SEPARATOR)

                        print(f"  [+] Added: {relative_file_path_str}")
                        files_processed += 1

                    except UnicodeDecodeError:
                        print(
                            f"  [!] Skipped (binary file): {relative_file_path_str}"
                        )
                    except Exception as e:
                        print(
                            f"  [!] Error reading {relative_file_path_str}: {e}"
                        )

    print("\nProcessing complete.")
    print(f"Total files added to {output_file}: {files_processed}")


def main():
    """Main function to parse arguments and start the process."""
    parser = argparse.ArgumentParser(
        description="Reads all files in a directory (respecting .gitignore and a default ignore list) and concatenates them into a single text file.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--directory",
        default=".",
        help="The root directory of the codebase to process.\n(default: current directory)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="codebase_content.txt",
        help="The name of the output file.\n(default: codebase_content.txt)",
    )
    args = parser.parse_args()

    root_directory = Path(args.directory)
    if not root_directory.is_dir():
        print(f"Error: Directory not found at '{args.directory}'")
        return

    # Get the combined spec of default ignores and .gitignore
    gitignore_spec = get_gitignore_spec(root_directory, args.output)
    process_directory(args.directory, args.output, gitignore_spec)


if __name__ == "__main__":
    main()