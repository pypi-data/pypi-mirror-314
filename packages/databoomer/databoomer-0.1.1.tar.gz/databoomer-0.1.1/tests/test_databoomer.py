import pytest
import dill
import codecs
import pandas as pd
import numpy as np
from databoomer import DataBoomer
import pyperclip

# Fixtures for common test objects
@pytest.fixture
def sample_dict():
    return {"test": 42}

@pytest.fixture
def sample_df():
    return pd.DataFrame({'a': [1, 2, 3]})

# Mock clipboard for testing
@pytest.fixture
def mock_clipboard(monkeypatch):
    clipboard_content = []
    def mock_copy(content):
        clipboard_content.append(content)
    
    monkeypatch.setattr(pyperclip, 'copy', mock_copy)
    return clipboard_content

# Basic functionality tests
def test_basic_serialization(sample_dict, mock_clipboard):
    """Test if basic object gets serialized and copied to clipboard"""
    DataBoomer(sample_dict)
    assert len(mock_clipboard) == 1
    assert 'dill.loads' in mock_clipboard[0]
    assert 'payload' in mock_clipboard[0]

def test_comment_inclusion(sample_dict, mock_clipboard):
    """Test if comments are properly included in output"""
    test_comment = "Test comment"
    DataBoomer(sample_dict, comment=test_comment)
    assert f"# comment: {test_comment}" in mock_clipboard[0]

def test_custom_name(sample_dict, mock_clipboard):
    """Test if custom object names are properly used"""
    custom_name = "my_dict"
    DataBoomer(sample_dict, obj_name=custom_name)
    assert f"{custom_name} = " in mock_clipboard[0]

# Template tests
def test_custom_template(sample_dict, mock_clipboard):
    """Test if custom templates work"""
    from string import Template
    custom_template = Template("# $comment\n$obj_name = dill.loads(codecs.decode('$payload', 'base64'))")
    DataBoomer(sample_dict, template=custom_template)
    assert mock_clipboard[0].startswith("# ")

# Complex object tests
def test_dataframe_serialization(sample_df, mock_clipboard):
    """Test if pandas DataFrame gets properly serialized"""
    DataBoomer(sample_df)
    code = mock_clipboard[0]
    # Execute the generated code and verify the result
    namespace = {}
    exec(code, globals(), namespace)
    result_df = namespace.get('obj')  # Using default name
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.equals(sample_df)

def test_numpy_array():
    """Test if numpy arrays are handled correctly"""
    arr = np.array([1, 2, 3])
    clipboard_before = pyperclip.paste()
    DataBoomer(arr)
    clipboard_after = pyperclip.paste()
    assert clipboard_before != clipboard_after

# Error handling tests
def test_non_serializable_object(mock_clipboard):
    """Test handling of non-serializable objects"""
    class NonSerializable:
        def __reduce__(self):
            raise TypeError("Not serializable")
    
    with pytest.raises(Exception):
        DataBoomer(NonSerializable())

# Variable name detection tests
def test_variable_naming(mock_clipboard):
    """Test variable naming behavior"""
    # Test with explicit name
    obj = [1, 2, 3]
    DataBoomer(obj, obj_name="my_var")
    assert "my_var = " in mock_clipboard[0]
    
    # Test fallback behavior
    mock_clipboard.clear()
    DataBoomer(obj)
    assert "obj = " in mock_clipboard[0]

# Integration tests
def test_full_roundtrip():
    """Test full serialization and deserialization cycle"""
    original_data = {
        'numbers': [1, 2, 3],
        'text': 'test',
        'nested': {'a': 1}
    }
    
    # Boom it
    DataBoomer(original_data)
    
    # Get the code from clipboard
    code = pyperclip.paste()
    
    # Execute the code in a new namespace
    namespace = {}
    exec(code, globals(), namespace)
    
    # Get the reconstructed object
    reconstructed = namespace.get('obj')
    
    # Verify it matches the original
    assert reconstructed == original_data
    assert reconstructed['nested']['a'] == original_data['nested']['a']

# Performance test
def test_large_object_handling():
    """Test handling of larger objects"""
    large_df = pd.DataFrame(np.random.randn(1000, 5))
    DataBoomer(large_df)  # Should complete within reasonable time