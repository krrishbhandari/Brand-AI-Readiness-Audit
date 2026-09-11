"""
Universal Test Runner for Brand AI-Readiness Audit Marketplace.
Runs all test suites using Python standard library unittest.
Usage:
    python tests/run_tests.py
"""

import unittest
import sys
import os

def run_all_tests():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    sys.path.insert(0, project_root)
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n" + "="*60)
        print("ALL TESTS PASSED SUCCESSFULLY! (100% SPEC & BENCHMARK COMPLIANCE)")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print(f"TESTS FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
