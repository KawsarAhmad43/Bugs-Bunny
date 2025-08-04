# bug_fixer_agent/tools/code_analyzer.py
import os
import ast
import re
from typing import Dict, List
from bug_fixer_agent.logger import Logger

class CodeAnalyzer:
    def __init__(self, logger: Logger):
        self.logger = logger

    def analyze_file(self, file_path: str) -> Dict:
        """
        Performs static analysis on a file to extract useful information.
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File {file_path} does not exist"}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.py']:
                return self._analyze_python_file(content, file_path)
            elif file_ext in ['.ts', '.tsx', '.js', '.jsx']:
                return self._analyze_typescript_file(content, file_path)
            else:
                return {"error": f"Unsupported file type: {file_ext}"}
                
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return {"error": str(e)}

    def _analyze_python_file(self, content: str, file_path: str) -> Dict:
        """
        Analyzes Python files for imports, functions, classes, and syntax errors.
        """
        result = {
            "file_type": "python",
            "imports": [],
            "functions": [],
            "classes": [],
            "syntax_errors": [],
            "file_path": file_path
        }
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        result["imports"].append(f"{module}.{alias.name}")
                elif isinstance(node, ast.FunctionDef):
                    result["functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    result["classes"].append(node.name)
                    
        except SyntaxError as e:
            result["syntax_errors"].append(f"Syntax error at line {e.lineno}: {e.msg}")
        except Exception as e:
            result["syntax_errors"].append(f"Analysis error: {str(e)}")
        
        return result

    def _analyze_typescript_file(self, content: str, file_path: str) -> Dict:
        """
        Analyzes TypeScript/JavaScript files for imports, functions, and basic structure.
        """
        result = {
            "file_type": "typescript",
            "imports": [],
            "functions": [],
            "components": [],
            "syntax_errors": [],
            "file_path": file_path
        }
        
        try:
            # Extract imports using regex
            import_patterns = [
                r'import\s+{([^}]+)}\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'import\s+[\'"]([^\'"]+)[\'"]'
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if isinstance(match, tuple):
                        result["imports"].extend([m.strip() for m in match[0].split(',')])
                    else:
                        result["imports"].append(match)
            
            # Extract function names
            function_patterns = [
                r'function\s+(\w+)\s*\(',
                r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
                r'(\w+)\s*:\s*React\.FC',
                r'export\s+(?:default\s+)?(?:function\s+)?(\w+)'
            ]
            
            for pattern in function_patterns:
                matches = re.findall(pattern, content)
                result["functions"].extend(matches)
            
            # Extract React components
            component_patterns = [
                r'function\s+(\w+)\s*\([^)]*\)\s*{',
                r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
                r'export\s+default\s+function\s+(\w+)'
            ]
            
            for pattern in component_patterns:
                matches = re.findall(pattern, content)
                result["components"].extend(matches)
            
            # Basic syntax validation
            if not self._validate_typescript_syntax(content):
                result["syntax_errors"].append("Potential syntax issues detected")
                
        except Exception as e:
            result["syntax_errors"].append(f"Analysis error: {str(e)}")
        
        return result

    def _validate_typescript_syntax(self, content: str) -> bool:
        """
        Basic TypeScript syntax validation.
        """
        # Check for balanced braces and parentheses
        brace_count = content.count('{') - content.count('}')
        paren_count = content.count('(') - content.count(')')
        bracket_count = content.count('[') - content.count(']')
        
        return brace_count == 0 and paren_count == 0 and bracket_count == 0

    def analyze_dependencies(self, file_path: str) -> Dict:
        """
        Analyzes dependencies and imports for a file.
        """
        analysis = self.analyze_file(file_path)
        if "error" in analysis:
            return analysis
        
        return {
            "file_path": file_path,
            "imports": analysis.get("imports", []),
            "dependencies": self._extract_dependencies(analysis.get("imports", []))
        }

    def _extract_dependencies(self, imports: List[str]) -> List[str]:
        """
        Extracts main dependencies from import statements.
        """
        dependencies = []
        for imp in imports:
            # Extract the main package name
            if '.' in imp:
                main_package = imp.split('.')[0]
                if main_package not in dependencies:
                    dependencies.append(main_package)
            else:
                if imp not in dependencies:
                    dependencies.append(imp)
        
        return dependencies 