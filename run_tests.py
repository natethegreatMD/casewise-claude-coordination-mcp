#!/usr/bin/env python3
"""
CCC Test Runner
Run all tests and generate coverage report
"""

import sys
import unittest
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def run_all_tests():
    """Run all tests and display results"""
    print("🧪 CCC Comprehensive Test Suite")
    print("=" * 50)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed! CCC is fully tested.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1


def run_coverage():
    """Run tests with coverage report"""
    try:
        import coverage
    except ImportError:
        print("Coverage not installed. Install with: pip install coverage")
        return
    
    print("\n📊 Running tests with coverage...")
    print("=" * 50)
    
    # Initialize coverage
    cov = coverage.Coverage(source=['src/casewise_coordination'])
    cov.start()
    
    # Run tests
    run_all_tests()
    
    # Stop coverage
    cov.stop()
    cov.save()
    
    # Generate report
    print("\n📈 Coverage Report:")
    print("=" * 50)
    cov.report()
    
    # Generate HTML report
    html_dir = Path(__file__).parent / 'htmlcov'
    cov.html_report(directory=str(html_dir))
    print(f"\n📄 HTML coverage report generated in: {html_dir}")


if __name__ == "__main__":
    # Check if coverage is requested
    if "--coverage" in sys.argv:
        run_coverage()
    else:
        # Just run tests
        exit_code = run_all_tests()
        sys.exit(exit_code)