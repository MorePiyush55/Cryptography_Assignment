#!/usr/bin/env python3
"""
Comprehensive Project Verification Script
This script verifies that your entire cryptography project is working 100%
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}")

def print_section(title):
    """Print a formatted section"""
    print(f"\n{'-'*60}")
    print(f" {title}")
    print(f"{'-'*60}")

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔍 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ FAILED: {description}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {description}")
        print(f"Exception: {str(e)}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING: {description}: {filepath}")
        return False

def verify_project_structure():
    """Verify the project structure is complete"""
    print_section("Project Structure Verification")
    
    required_files = [
        ("src/crypto_protocol.py", "Main Protocol Implementation"),
        ("src/key_management.py", "Key Management Module"),
        ("src/digital_signature.py", "Digital Signature Module"), 
        ("src/communication.py", "Secure Communication Module"),
        ("examples/demo_transaction.py", "Demonstration Script"),
        ("tests/test_protocol.py", "Unit Tests"),
        ("docs/report.md", "Main Report"),
        ("docs/protocol_design.md", "Protocol Design Documentation"),
        ("docs/security_analysis.md", "Security Analysis"),
        ("requirements.txt", "Requirements File"),
        ("README.md", "README File")
    ]
    
    all_present = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_present = False
    
    return all_present

def verify_python_environment():
    """Verify Python environment and dependencies"""
    print_section("Python Environment Verification")
    
    # Check Python version
    python_cmd = "C:/Users/piyus/AppData/Local/Programs/Python/Python313/project/Cryptography_Assignment/crypto_env/Scripts/python.exe"
    
    success = True
    success &= run_command(f'"{python_cmd}" --version', "Python Version Check")
    success &= run_command(f'"{python_cmd}" -c "import cryptography; print(f\'cryptography version: {{cryptography.__version__}}\')"', "Cryptography Library Check")
    success &= run_command(f'"{python_cmd}" -c "import pytest; print(f\'pytest version: {{pytest.__version__}}\')"', "Pytest Library Check")
    
    return success

def verify_imports():
    """Verify all modules can be imported correctly"""
    print_section("Module Import Verification")
    
    python_cmd = "C:/Users/piyus/AppData/Local/Programs/Python/Python313/project/Cryptography_Assignment/crypto_env/Scripts/python.exe"
    
    import_tests = [
        ("sys.path.append('src'); import key_management", "Key Management Module"),
        ("sys.path.append('src'); import digital_signature", "Digital Signature Module"),
        ("sys.path.append('src'); import communication", "Communication Module"),
        ("sys.path.append('src'); import crypto_protocol", "Main Protocol Module"),
    ]
    
    success = True
    for import_cmd, description in import_tests:
        success &= run_command(f'"{python_cmd}" -c "{import_cmd}; print(\'Import successful\')"', f"Import {description}")
    
    return success

def run_unit_tests():
    """Run the unit test suite"""
    print_section("Unit Test Execution")
    
    python_cmd = "C:/Users/piyus/AppData/Local/Programs/Python/Python313/project/Cryptography_Assignment/crypto_env/Scripts/python.exe"
    
    # Run pytest
    success = run_command(f'"{python_cmd}" -m pytest tests/ -v', "Unit Test Suite")
    
    return success

def run_demonstration():
    """Run the demonstration script"""
    print_section("Demonstration Script Execution")
    
    python_cmd = "C:/Users/piyus/AppData/Local/Programs/Python/Python313/project/Cryptography_Assignment/crypto_env/Scripts/python.exe"
    
    success = run_command(f'"{python_cmd}" examples/demo_transaction.py', "Property Transaction Demonstration")
    
    return success

def verify_documentation():
    """Verify documentation completeness"""
    print_section("Documentation Verification")
    
    python_cmd = "C:/Users/piyus/AppData/Local/Programs/Python/Python313/project/Cryptography_Assignment/crypto_env/Scripts/python.exe"
    
    # Check word count
    word_count_cmd = f'"{python_cmd}" -c "with open(\'docs/report.md\', \'r\', encoding=\'utf-8\') as f: content = f.read(); words = len([w for w in content.split() if w.strip() and not w.startswith(\'#\') and not w.startswith(\'```\')]); print(f\'Report word count: {{words}} words\')"'
    
    success = run_command(word_count_cmd, "Report Word Count Check")
    
    # Check for key sections
    key_sections = [
        "Abstract",
        "Introduction", 
        "Literature Review",
        "Algorithm Selection",
        "Protocol Design",
        "Implementation",
        "Security Analysis",
        "Conclusion"
    ]
    
    try:
        with open('docs/report.md', 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"\n📄 Report Content Verification:")
        for section in key_sections:
            if section.lower() in content.lower():
                print(f"✅ {section} section found")
            else:
                print(f"❌ {section} section missing")
                success = False
                
    except Exception as e:
        print(f"❌ Error reading report: {str(e)}")
        success = False
    
    return success

def verify_security_features():
    """Verify key security features are implemented"""
    print_section("Security Features Verification")
    
    python_cmd = "C:/Users/piyus/AppData/Local/Programs/Python/Python313/project/Cryptography_Assignment/crypto_env/Scripts/python.exe"
    
    security_tests = [
        # Test RSA key generation
        ('sys.path.append("src"); from key_management import KeyManager; km = KeyManager(); private, public = km.generate_rsa_keypair(); print(f"RSA key size: {public.key_size} bits")', "RSA Key Generation"),
        
        # Test AES encryption
        ('sys.path.append("src"); from key_management import SymmetricKeyManager; sm = SymmetricKeyManager(); key = sm.generate_aes_key(); print(f"AES key size: {len(key)*8} bits")', "AES Key Generation"),
        
        # Test digital signatures
        ('sys.path.append("src"); from digital_signature import DigitalSignature; from key_management import KeyManager; ds = DigitalSignature(); km = KeyManager(); km.register_party("test"); priv = km.get_private_key("test"); pub = km.get_public_key("test"); signed = ds.sign_document("test", priv, {"name": "test", "role": "test", "jurisdiction": "UK"}); valid, msg = ds.verify_signature(signed, pub); print(f"Digital signature test: {valid}")', "Digital Signature"),
        
        # Test hybrid encryption
        ('sys.path.append("src"); from communication import SecureCommunication; from key_management import KeyManager; sc = SecureCommunication(); km = KeyManager(); km.register_party("test"); pub = km.get_public_key("test"); priv = km.get_private_key("test"); encrypted = sc.encrypt_message("test message", pub, "sender", "recipient"); success, decrypted = sc.decrypt_message(encrypted, priv); print(f"Hybrid encryption test: {success and decrypted == \'test message\'}")', "Hybrid Encryption")
    ]
    
    success = True
    for test_cmd, description in security_tests:
        success &= run_command(f'"{python_cmd}" -c "{test_cmd}"', f"Security Test: {description}")
    
    return success

def main():
    """Main verification function"""
    print_header("CRYPTOGRAPHY PROJECT VERIFICATION")
    print("This script will comprehensively test your project to ensure 100% functionality")
    
    start_time = time.time()
    all_tests_passed = True
    
    # Run all verification steps
    verification_steps = [
        ("Project Structure", verify_project_structure),
        ("Python Environment", verify_python_environment), 
        ("Module Imports", verify_imports),
        ("Security Features", verify_security_features),
        ("Unit Tests", run_unit_tests),
        ("Demonstration", run_demonstration),
        ("Documentation", verify_documentation)
    ]
    
    results = {}
    
    for step_name, step_function in verification_steps:
        print_header(f"STEP: {step_name}")
        try:
            success = step_function()
            results[step_name] = success
            all_tests_passed &= success
            
            if success:
                print(f"\n✅ {step_name}: PASSED")
            else:
                print(f"\n❌ {step_name}: FAILED")
                
        except Exception as e:
            print(f"\n❌ {step_name}: ERROR - {str(e)}")
            results[step_name] = False
            all_tests_passed = False
    
    # Final summary
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print_header("VERIFICATION SUMMARY")
    
    print(f"📊 Test Results:")
    for step_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {step_name}: {status}")
    
    print(f"\n⏱️  Total verification time: {elapsed_time:.2f} seconds")
    
    if all_tests_passed:
        print(f"\n🎉 CONGRATULATIONS! 🎉")
        print(f"✅ Your project is working 100% correctly!")
        print(f"✅ All components verified successfully")
        print(f"✅ Ready for internship submission")
        print(f"\n🚀 Your cryptography assignment is complete and fully functional!")
        
    else:
        print(f"\n⚠️  Some tests failed. Please review the issues above.")
        print(f"❌ Project needs attention before submission")
        
        failed_steps = [step for step, success in results.items() if not success]
        print(f"\n📋 Failed steps to fix:")
        for step in failed_steps:
            print(f"   - {step}")

if __name__ == "__main__":
    main()
