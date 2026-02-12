#!/usr/bin/env python3
"""Command-line interface for TestCaseGen."""

import argparse
import sys
from pathlib import Path
from .analyzer import CodeAnalyzer
from .generator import TestGenerator
from .config import Config

def main():
    parser = argparse.ArgumentParser(description="Generate test cases automatically")
    parser.add_argument("source", help="Source file or directory to analyze")
    parser.add_argument("-o", "--output", default="tests", help="Output directory for tests")
    parser.add_argument("-f", "--framework", choices=["pytest", "unittest"], default="pytest", help="Test framework")
    parser.add_argument("-c", "--config", help="Configuration file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    config = Config()
    if args.config:
        config.load_from_file(args.config)
    
    config.framework = args.framework
    config.output_dir = Path(args.output)
    config.verbose = args.verbose
    
    analyzer = CodeAnalyzer(config)
    generator = TestGenerator(config)
    
    try:
        source_path = Path(args.source)
        if not source_path.exists():
            print(f"Error: Source path '{source_path}' does not exist")
            sys.exit(1)
        
        print(f"Analyzing {source_path}...")
        analysis_result = analyzer.analyze(source_path)
        
        print(f"Generating tests for {len(analysis_result.functions)} functions...")
        generator.generate_tests(analysis_result)
        
        print(f"Tests generated successfully in {config.output_dir}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()