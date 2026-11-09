"""
Unit test for apx.config.apphome function
"""

import pytest
import pytest_asyncio


import os
import tempfile


import apx.config
import apx.exceptions




@pytest_asyncio.fixture
async def testRoot():
    """Temporary directory for test purposes"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir



@pytest.mark.asyncio
async def test_apphome_env_not_set():
    """Test that app home environmental variable not set raises an exception"""

    # -- stage

    # - check for existing config
    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            assert False, "App home environment variable should not be set for this test"


    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.apphome()


    # -- assertions
    assert "App home environment variable is not set" in str(ex_details.value)



@pytest.mark.asyncio
async def test_apphome_env_multiple_vars():
    """Test that multiple app home environmental variables set raises an exception"""

    # -- stage

    # - check for existing config
    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            assert False, "App home environment variable should not be set for this test"


    # - multiple app home environmental variable

    os.environ["APP_HOME"] = "some random value"
    os.environ["APPHOME"] = "some other value"


    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.apphome()


    # -- assertions
    assert "Multiple app home environment variables are set" in str(ex_details.value)


    # -- clean up
    del os.environ["APP_HOME"]
    del os.environ["APPHOME"]



@pytest.mark.asyncio
async def test_apphome_dir_not_exist(testRoot):
    """Test that app home directory does not exist raises an exception"""

    # -- stage

    # - check for existing config
    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            assert False, "App home environment variable should not be set for this test"

    # - test directory
    test_path = testRoot + "/non_existent_directory"
    assert not os.path.exists(test_path), "Test directory should not exist"


    # - set app home environmental variable to a non-existent directory
    os.environ["APP_HOME"] = test_path

    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.apphome()

    # -- assertions
    assert "App home directory does not exist" in str(ex_details.value)

    # -- clean up
    del os.environ["APP_HOME"]


@pytest.mark.asyncio
async def test_apphome_dir_isfile(testRoot):

    # -- stage
    
    # - check for existing config
    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            assert False, "App home environment variable should not be set for this test"

    # - test file

    test_path = testRoot + "/test_file"
    with open(test_path, "w") as f:
        f.write("test content")

    assert os.path.isfile(test_path), "Test file should exist"

    # - set app home environmental variable to a file
    os.environ["APP_HOME"] = test_path

    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.apphome()

    # -- assertions
    assert "App home directory does not exist or is not a directory" in str(ex_details.value)

    # -- clean up
    del os.environ["APP_HOME"]



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "envvarname", ["APP_HOME", "app_home", "App_Home", "APPHOME", "apphome", "appHome", "AppHome"]
)
async def test_apphome_dir(testRoot, envvarname):

    # -- stage
    
    # - check for existing config
    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            assert False, "App home environment variable should not be set for this test"


    # - set app home environmental variable to a file
    os.environ[envvarname] = testRoot

    # -- test
    result = apx.config.apphome()

    # -- assertions
    assert result == testRoot


    # -- clean up
    del os.environ[envvarname]



