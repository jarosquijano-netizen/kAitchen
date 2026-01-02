#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to run all tests
"""
import sys
import subprocess
import os


def run_backend_tests():
    """Run backend tests"""
    print("=" * 60)
    print("Running Backend Tests")
    print("=" * 60)
    
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short'],
        cwd=os.getcwd()
    )
    
    return result.returncode == 0


def run_frontend_tests():
    """Run frontend tests"""
    print("\n" + "=" * 60)
    print("Running Frontend Tests")
    print("=" * 60)
    
    # Check if Node.js is available
    try:
        result = subprocess.run(
            ['node', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Run frontend tests
            result = subprocess.run(
                ['node', 'tests/test_frontend.js'],
                cwd=os.getcwd()
            )
            return result.returncode == 0
        else:
            print("Node.js not found, skipping frontend tests")
            return True
    except FileNotFoundError:
        print("Node.js not found, skipping frontend tests")
        return True


def main():
    """Run all tests"""
    print("\nRunning Test Suite\n")
    
    backend_ok = run_backend_tests()
    frontend_ok = run_frontend_tests()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Backend Tests: {'PASSED' if backend_ok else 'FAILED'}")
    print(f"Frontend Tests: {'PASSED' if frontend_ok else 'FAILED'}")
    print("=" * 60)
    
    if backend_ok and frontend_ok:
        print("\nAll tests passed!")
        return 0
    else:
        print("\nSome tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
