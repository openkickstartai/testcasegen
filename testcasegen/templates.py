"""Test template classes for different frameworks."""

from abc import ABC, abstractmethod
from typing import List

class TestTemplate(ABC):
    """Abstract base class for test templates."""
    
    @abstractmethod
    def render(self, imports: str, test_functions: List[str], module_name: str) -> str:
        """Render the complete test file."""
        pass
    
    @abstractmethod
    def render_test_function(self, function_name: str, test_cases: List[dict], docstring: str) -> str:
        """Render a single test function."""
        pass

class PytestTemplate(TestTemplate):
    """Template for pytest framework."""
    
    def render(self, imports: str, test_functions: List[str], module_name: str) -> str:
        """Render the complete pytest test file."""
        header = f'"""Tests for {module_name} module."""\n\n'
        content = header + imports + "\n\n" + "\n\n".join(test_functions)
        return content
    
    def render_test_function(self, function_name: str, test_cases: List[dict], docstring: str) -> str:
        """Render a pytest test function."""
        test_name = f"test_{function_name}"
        
        # Generate test body
        test_body = []
        test_body.append(f'    """Test {function_name} function."""')
        
        for i, case in enumerate(test_cases):
            test_body.append(f"    # Test case {i + 1}: {case['name']}")
            
            # Generate function call
            if case['args']:
                args_str = ", ".join([f"{k}={repr(v)}" for k, v in case['args'].items()])
                test_body.append(f"    result = {function_name}({args_str})")
            else:
                test_body.append(f"    result = {function_name}()")
            
            test_body.append(f"    assert result is not None  # TODO: Add proper assertion")
            test_body.append("")
        
        return f"def {test_name}():\n" + "\n".join(test_body)

class UnittestTemplate(TestTemplate):
    """Template for unittest framework."""
    
    def render(self, imports: str, test_functions: List[str], module_name: str) -> str:
        """Render the complete unittest test file."""
        header = f'"""Tests for {module_name} module."""\n\n'
        class_header = f"class Test{module_name.title()}(unittest.TestCase):\n"
        class_header += '    """Test cases for the module."""\n\n'
        
        # Indent test functions for class
        indented_functions = []
        for func in test_functions:
            indented_func = "\n".join(["    " + line for line in func.split("\n")])
            indented_functions.append(indented_func)
        
        footer = "\n\nif __name__ == '__main__':\n    unittest.main()"
        
        content = header + imports + "\n\n" + class_header + "\n\n".join(indented_functions) + footer
        return content
    
    def render_test_function(self, function_name: str, test_cases: List[dict], docstring: str) -> str:
        """Render a unittest test method."""
        test_name = f"test_{function_name}"
        
        # Generate test body
        test_body = []
        test_body.append(f'"""Test {function_name} function."""')
        
        for i, case in enumerate(test_cases):
            test_body.append(f"# Test case {i + 1}: {case['name']}")
            
            # Generate function call
            if case['args']:
                args_str = ", ".join([f"{k}={repr(v)}" for k, v in case['args'].items()])
                test_body.append(f"result = {function_name}({args_str})")
            else:
                test_body.append(f"result = {function_name}()")
            
            test_body.append(f"self.assertIsNotNone(result)  # TODO: Add proper assertion")
            test_body.append("")
        
        return f"def {test_name}(self):\n    " + "\n    ".join(test_body)