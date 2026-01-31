def test_example():
    """Simple test to verify pytest is working"""
    assert 1 + 1 == 2

def test_basic_math():
    """Another simple test"""
    assert 2 * 3 == 6

def test_string_operations():
    """Test string operations"""
    assert "hello".upper() == "HELLO"
    assert "world".lower() == "world"

def test_list_operations():
    """Test list operations"""
    my_list = [1, 2, 3]
    assert len(my_list) == 3
    assert 1 in my_list
