"""Test case generation module."""

from pathlib import Path
from typing import List
from .analyzer import AnalysisResult, FunctionInfo
from .templates import PytestTemplate, UnittestTemplate

class TestGenerator:
    """Generates test cases based on code analysis."""
    
    def __init__(self, config):
        self.config = config
        self.template = self._get_template()
    
    def _get_template(self):
        """Get the appropriate test template based on framework."""
        if self.config.framework == "pytest":
            return PytestTemplate()
        elif self.config.framework == "unittest":
            return UnittestTemplate()
        else:
            raise ValueError(f"Unsupported framework: {self.config.framework}")
    
    def generate_tests(self, analysis_result: AnalysisResult):
        """Generate test files based on analysis results."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py in test directory
        init_file = self.config.output_dir / "__init__.py"
        init_file.write_text("")
        
        # Generate test file
        test_filename = f"test_{analysis_result.file_path.stem}.py"
        test_file_path = self.config.output_dir / test_filename
        
        test_content = self._generate_test_content(analysis_result)
        test_file_path.write_text(test_content)
        
        if self.config.verbose:
            print(f"Generated {test_file_path}")
    
    def _generate_test_content(self, analysis_result: AnalysisResult) -> str:
        """Generate the content of a test file."""
        imports = self._generate_imports(analysis_result)
        test_functions = self._generate_test_functions(analysis_result.functions)
        
        return self.template.render(
            imports=imports,
            test_functions=test_functions,
            module_name=analysis_result.file_path.stem
        )
    
    def _generate_imports(self, analysis_result: AnalysisResult) -> str:
        """Generate import statements for the test file."""
        imports = []
        
        if self.config.framework == "pytest":
            imports.append("import pytest")
        elif self.config.framework == "unittest":
            imports.append("import unittest")
        
        # Import the module being tested
        module_name = analysis_result.file_path.stem
        imports.append(f"from {module_name} import *")
        
        return "\n".join(imports)
    
    def _generate_test_functions(self, functions: List[FunctionInfo]) -> List[str]:
        """Generate test functions for each analyzed function."""
        test_functions = []
        
        for func in functions:
            if func.name.startswith('_'):  # Skip private functions
                continue
            
            test_func = self._generate_single_test(func)
            test_functions.append(test_func)
        
        return test_functions
    
    def _generate_single_test(self, func_info: FunctionInfo) -> str:
        """Generate a single test function."""
        test_cases = self._generate_test_cases(func_info)
        return self.template.render_test_function(
            function_name=func_info.name,
            test_cases=test_cases,
            docstring=func_info.docstring
        )
    
    def _generate_test_cases(self, func_info: FunctionInfo) -> List[dict]:
        """Generate test cases for a function based on its signature."""
        test_cases = []
        
        # Generate basic test case
        basic_case = {
            "name": "basic",
            "args": self._generate_basic_args(func_info.args),
            "expected": "None"  # Placeholder
        }
        test_cases.append(basic_case)
        
        # Generate edge cases based on argument types
        if func_info.args:
            edge_case = {
                "name": "edge_case",
                "args": self._generate_edge_args(func_info.args),
                "expected": "None"  # Placeholder
            }
            test_cases.append(edge_case)
        
        return test_cases
    
    def _generate_basic_args(self, args: List[str]) -> dict:
        """Generate basic argument values for testing."""
        arg_values = {}
        for arg in args:
            if arg == "self":
                continue
            # Simple heuristic for argument types
            if "num" in arg.lower() or "count" in arg.lower():
                arg_values[arg] = 1
            elif "str" in arg.lower() or "name" in arg.lower():
                arg_values[arg] = "test"
            elif "list" in arg.lower() or "items" in arg.lower():
                arg_values[arg] = [1, 2, 3]
            else:
                arg_values[arg] = None
        return arg_values
    
    def _generate_edge_args(self, args: List[str]) -> dict:
        """Generate edge case argument values."""
        arg_values = {}
        for arg in args:
            if arg == "self":
                continue
            # Edge cases
            if "num" in arg.lower() or "count" in arg.lower():
                arg_values[arg] = 0
            elif "str" in arg.lower() or "name" in arg.lower():
                arg_values[arg] = ""
            elif "list" in arg.lower() or "items" in arg.lower():
                arg_values[arg] = []
            else:
                arg_values[arg] = None
        return arg_values