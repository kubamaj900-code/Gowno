"""
Simple tests for the Bramka access code system.
Tests only the core logic without requiring external dependencies.
"""
import sys
import os
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Optional

# Mock the access code storage and functions
access_codes: Dict[str, dict] = {}

def generate_access_code(length: int = 8) -> str:
    """Generate a random access code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def cleanup_expired_codes():
    """Remove expired codes from storage."""
    now = datetime.now()
    expired_codes = [
        code for code, data in access_codes.items()
        if now - data['created_at'] > timedelta(minutes=10)
    ]
    for code in expired_codes:
        del access_codes[code]

def get_code_status(code: str) -> dict:
    """Get the status of an access code."""
    if code not in access_codes:
        return {'status': 'invalid', 'message': 'Kod nie istnieje lub wygasł'}
    
    code_data = access_codes[code]
    
    # Check if expired
    time_left = timedelta(minutes=10) - (datetime.now() - code_data['created_at'])
    if time_left.total_seconds() <= 0:
        del access_codes[code]
        return {'status': 'expired', 'message': 'Kod wygasł'}
    
    if code_data['used']:
        return {'status': 'used', 'message': 'Kod został już użyty'}
    
    # Clean up other expired codes
    cleanup_expired_codes()
    
    return {
        'status': 'valid',
        'message': 'Kod jest aktywny',
        'username': code_data['username'],
        'time_left': int(time_left.total_seconds()),
        'created_at': code_data['created_at'].strftime('%H:%M:%S')
    }

def mark_code_as_used(code: str) -> Optional[dict]:
    """Mark a code as used and return user data."""
    cleanup_expired_codes()
    
    if code not in access_codes:
        return None
    
    code_data = access_codes[code]
    
    # Check if expired
    if datetime.now() - code_data['created_at'] > timedelta(minutes=10):
        del access_codes[code]
        return None
    
    # Check if already used
    if code_data['used']:
        return None
    
    # Mark as used
    code_data['used'] = True
    
    return code_data

def test_generate_access_code():
    """Test access code generation."""
    code1 = generate_access_code()
    code2 = generate_access_code()
    
    # Codes should be 8 characters
    assert len(code1) == 8, f"Code should be 8 characters, got {len(code1)}"
    assert len(code2) == 8, f"Code should be 8 characters, got {len(code2)}"
    
    # Codes should be unique
    assert code1 != code2, "Generated codes should be unique"
    
    # Codes should only contain uppercase letters and digits
    assert code1.isalnum(), "Code should only contain alphanumeric characters"
    assert code1.isupper() or code1.isdigit(), "Code should be uppercase"
    
    print("✓ test_generate_access_code passed")

def test_code_storage_and_retrieval():
    """Test storing and retrieving access codes."""
    # Clear any existing codes
    access_codes.clear()
    
    # Create a test code
    code = "TEST1234"
    access_codes[code] = {
        'user_id': 12345,
        'username': 'testuser',
        'created_at': datetime.now(),
        'used': False
    }
    
    # Retrieve code status
    status = get_code_status(code)
    assert status['status'] == 'valid', f"Code should be valid, got {status['status']}"
    assert status['username'] == 'testuser', "Username should match"
    
    print("✓ test_code_storage_and_retrieval passed")

def test_code_expiration():
    """Test that codes expire after 10 minutes."""
    # Clear any existing codes
    access_codes.clear()
    
    # Create an expired code
    code = "EXPIRED1"
    access_codes[code] = {
        'user_id': 12345,
        'username': 'testuser',
        'created_at': datetime.now() - timedelta(minutes=11),
        'used': False
    }
    
    # Check status
    status = get_code_status(code)
    assert status['status'] == 'expired', f"Code should be expired, got {status['status']}"
    
    # Code should be removed from storage
    assert code not in access_codes, "Expired code should be removed from storage"
    
    print("✓ test_code_expiration passed")

def test_code_usage():
    """Test marking a code as used."""
    # Clear any existing codes
    access_codes.clear()
    
    # Create a valid code
    code = "VALID123"
    access_codes[code] = {
        'user_id': 12345,
        'username': 'testuser',
        'created_at': datetime.now(),
        'used': False
    }
    
    # Mark code as used
    result = mark_code_as_used(code)
    assert result is not None, "Should return user data"
    assert result['user_id'] == 12345, "User ID should match"
    
    # Code should now be marked as used
    assert access_codes[code]['used'] == True, "Code should be marked as used"
    
    # Check status
    status = get_code_status(code)
    assert status['status'] == 'used', f"Code should be used, got {status['status']}"
    
    # Try to use again - should fail
    result2 = mark_code_as_used(code)
    assert result2 is None, "Already used code should not be reusable"
    
    print("✓ test_code_usage passed")

def test_cleanup_expired_codes():
    """Test cleanup of expired codes."""
    # Clear any existing codes
    access_codes.clear()
    
    # Add some codes
    access_codes["VALID001"] = {
        'user_id': 1,
        'username': 'user1',
        'created_at': datetime.now(),
        'used': False
    }
    access_codes["EXPIRED1"] = {
        'user_id': 2,
        'username': 'user2',
        'created_at': datetime.now() - timedelta(minutes=11),
        'used': False
    }
    access_codes["EXPIRED2"] = {
        'user_id': 3,
        'username': 'user3',
        'created_at': datetime.now() - timedelta(minutes=15),
        'used': False
    }
    
    # Run cleanup
    cleanup_expired_codes()
    
    # Only valid code should remain
    assert "VALID001" in access_codes, "Valid code should remain"
    assert "EXPIRED1" not in access_codes, "Expired code should be removed"
    assert "EXPIRED2" not in access_codes, "Expired code should be removed"
    assert len(access_codes) == 1, "Only one code should remain"
    
    print("✓ test_cleanup_expired_codes passed")

def run_tests():
    """Run all tests."""
    print("\nRunning Bramka Access Code Tests...\n")
    
    try:
        test_generate_access_code()
        test_code_storage_and_retrieval()
        test_code_expiration()
        test_code_usage()
        test_cleanup_expired_codes()
        
        print("\n✅ All tests passed!\n")
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
