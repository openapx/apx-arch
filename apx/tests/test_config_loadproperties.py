"""
Unit tests for apx.config.load_properties function
"""


import pytest
import pytest_asyncio

import os
import tempfile
import random
import string

import apx.config
import apx.exceptions



@pytest_asyncio.fixture
async def testRoot():
    """Temporary directory for test purposes"""

    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir




@pytest.mark.asyncio
async def test_load_filenotexist(testRoot):
    """Test that loading a non-existent file raises an exception"""

    # -- stage
    test_file = os.path.join(testRoot, "i_do_not_exist.properties")
    assert not os.path.exists(test_file), "Test file should not exist"

    # -- test

    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.load_properties(test_file)

    # -- assertions
    assert "Properties file does not exist" in str(ex_details.value)



@pytest.mark.asyncio
async def test_load_empty_file(testRoot):
    """Test that loading an empty properties file returns an empty dictionary"""

    # -- stage
    test_file = os.path.join(testRoot, "empty.properties")
    with open(test_file, "w") as f:
        pass  # create an empty file

    # -- test
    result = apx.config.load_properties(test_file)

    # -- assertions
    assert result == {}, "Loading an empty properties file should return an empty dictionary"



@pytest.mark.asyncio
async def test_load_only_comments(testRoot):
    """Test that loading a properties file with only comments returns an empty dictionary"""

    # -- stage
    test_file = os.path.join(testRoot, "only_comments.properties")
    with open(test_file, "w") as f:
        f.write("# key1 = value1\n")
        f.write("     # key2 = value2\n")

    # -- test
    result = apx.config.load_properties(test_file)

    # -- assertions
    assert result == {}, "Loading a properties file with only comments should return an empty dictionary"



@pytest.mark.asyncio
async def test_load_simpleprops(testRoot):
    """Test that loading a simple properties file returns the correct dictionary"""

    # -- stage
    test_file = os.path.join(testRoot, "simple.properties")

    # note: same set of properties as for commented scenario before
    with open(test_file, "w") as f:
        f.write("key1=value1\n")
        f.write("key2=value2\n")

    # -- test
    result = apx.config.load_properties(test_file)

    # -- assertions
    assert result == {"key1": "value1", "key2": "value2"}, "Loading a simple properties file should return the correct dictionary"




@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_key",
    ["a", ".abc", "abc.", "ab-c", "-abc", "ab_c", "_abc", "1", "!abc"]
)
async def test_load_invalid_key(testRoot, test_key):
    """Test that loading a properties file with an invalid key raises an exception"""

    # -- stage
    test_file = os.path.join(testRoot, "invalid_key.properties")
    with open(test_file, "w") as f:
        f.write(f"{test_key}={''.join(random.choices(string.ascii_letters + string.digits, k=25))}\n") 

    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
         apx.config.load_properties(test_file)

    # -- assertions
    assert "Invalid property name" in str(ex_details.value)



@pytest.mark.asyncio
async def test_load_value_with_equalsign(testRoot):
    """Test that loading a properties file with a value containing an equal sign works correctly"""

    # -- stage
    test_file = os.path.join(testRoot, "value_with_equalsign.properties")
    with open(test_file, "w") as f:
        f.write("key1=value=with=equals\n")

    # -- test
    result = apx.config.load_properties(test_file)

    # -- assertions
    assert result == {"key1": "value=with=equals"}, "Loading a properties file with a value containing an equal sign should work correctly"



@pytest.mark.asyncio
async def test_load_repeated_key(testRoot):
    """Test that loading a properties file with a repeated key raises an exception"""

    # -- stage

    # - test key
    test_key = ''.join(random.choices(string.ascii_letters + string.digits, k=25))

    # - test value
    test_value_1 = ''.join(random.choices(string.ascii_letters + string.digits, k=55))
    test_value_2 = ''.join(random.choices(string.ascii_letters + string.digits, k=55))


    # - test file
    test_file = os.path.join(testRoot, "repeated_key.properties")

    with open(test_file, "w") as f:
        f.write(f"{test_key}={test_value_1}\n")
        f.write(f"{test_key}={test_value_2}\n")

    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
         apx.config.load_properties(test_file)

    # -- assertions
    assert "Duplicate property definition" in str(ex_details.value)

