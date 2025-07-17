#!/usr/bin/env python3
"""
Basic CCC functionality test
Verifies the system is working correctly
"""

import sys
import subprocess
from pathlib import Path

def test_imports():
    """Test that CCC can be imported"""
    print("Testing imports...")
    try:
        import casewise_coordination
        print(f"✅ CCC v{casewise_coordination.__version__} imported successfully")
        
        from casewise_coordination import SessionOrchestrator, ClaudeSession
        print("✅ Core classes imported")
        
        from casewise_coordination.cli import main as cli_main
        print("✅ CLI imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli_commands():
    """Test CLI commands work"""
    print("\nTesting CLI commands...")
    
    # Test help
    result = subprocess.run([sys.executable, "-m", "casewise_coordination.cli", "--help"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ CLI help works")
    else:
        print(f"❌ CLI help failed: {result.stderr}")
        return False
    
    # Test version
    result = subprocess.run([sys.executable, "-m", "casewise_coordination.cli", "version"], 
                          capture_output=True, text=True)
    if result.returncode == 0 and "0.1.0" in result.stdout:
        print("✅ Version command works")
    else:
        print(f"❌ Version command failed")
        return False
    
    return True

def test_orchestrator_creation():
    """Test creating an orchestrator"""
    print("\nTesting orchestrator creation...")
    try:
        from casewise_coordination import SessionOrchestrator
        
        workspace = Path("./test_workspace")
        orchestrator = SessionOrchestrator(
            workspace_root=workspace,
            max_parallel_sessions=2
        )
        
        print("✅ Orchestrator created successfully")
        
        # Get status
        status = orchestrator.get_status()
        print(f"✅ Orchestrator status: {status['total_sessions']} sessions")
        
        # Cleanup
        orchestrator.terminate_all()
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator creation failed: {e}")
        return False

def test_templates():
    """Test session templates"""
    print("\nTesting session templates...")
    try:
        from casewise_coordination.templates import (
            FrontendTemplate, BackendTemplate, TestingTemplate
        )
        
        # Test each template
        templates = [
            ("Frontend", FrontendTemplate()),
            ("Backend", BackendTemplate()),
            ("Testing", TestingTemplate())
        ]
        
        for name, template in templates:
            prompt = template.create_prompt("Test task", {})
            if len(prompt) > 100:  # Should create substantial prompts
                print(f"✅ {name} template works")
            else:
                print(f"❌ {name} template failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 CCC Basic Functionality Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_cli_commands,
        test_orchestrator_creation,
        test_templates
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! CCC is ready to use.")
        print("\nNext steps:")
        print("1. Run './quickstart.sh' for interactive setup")
        print("2. Or run 'ccc demo' to see it in action")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)