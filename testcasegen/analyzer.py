"""Code analysis module for extracting testable components."""

import ast
import inspect
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class FunctionInfo:
    name: str
    args: List[str]
    return_type: str
    docstring: str
    complexity: int
    line_number: int

@dataclass
class AnalysisResult:
    functions: List[FunctionInfo]
    classes: List[str]
    imports: List[str]
    file_path: Path

class CodeAnalyzer:
    """Analyzes Python code to extract testable components."""
    
    def __init__(self, config):
        self.config = config
    
    def analyze(self, source_path: Path) -> AnalysisResult:
        """Analyze source code and extract function information."""
        if source_path.is_file():
            return self._analyze_file(source_path)
        elif source_path.is_dir():
            return self._analyze_directory(source_path)
        else:
            raise ValueError(f"Invalid source path: {source_path}")
    
    def _analyze_file(self, file_path: Path) -> AnalysisResult:
        """Analyze a single Python file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code)
        visitor = FunctionVisitor()
        visitor.visit(tree)
        
        return AnalysisResult(
            functions=visitor.functions,
            classes=visitor.classes,
            imports=visitor.imports,
            file_path=file_path
        )
    
    def _analyze_directory(self, dir_path: Path) -> AnalysisResult:
        """Analyze all Python files in a directory."""
        all_functions = []
        all_classes = []
        all_imports = []
        
        for py_file in dir_path.rglob('*.py'):
            if py_file.name.startswith('test_'):
                continue
            
            result = self._analyze_file(py_file)
            all_functions.extend(result.functions)
            all_classes.extend(result.classes)
            all_imports.extend(result.imports)
        
        return AnalysisResult(
            functions=all_functions,
            classes=list(set(all_classes)),
            imports=list(set(all_imports)),
            file_path=dir_path
        )

class FunctionVisitor(ast.NodeVisitor):
    """AST visitor to extract function and class information."""
    
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
    
    def visit_FunctionDef(self, node):
        args = [arg.arg for arg in node.args.args]
        return_type = "Any"
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        docstring = ast.get_docstring(node) or ""
        complexity = self._calculate_complexity(node)
        
        func_info = FunctionInfo(
            name=node.name,
            args=args,
            return_type=return_type,
            docstring=docstring,
            complexity=complexity,
            line_number=node.lineno
        )
        
        self.functions.append(func_info)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
    
    def visit_ImportFrom(self, node):
        if node.module:
            for alias in node.names:
                self.imports.append(f"{node.module}.{alias.name}")
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity