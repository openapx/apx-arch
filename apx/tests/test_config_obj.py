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


@pytest_asyncio.fixture
async def testAppHome(testRoot):

    # - check for existing config
    for key, value in os.environ.items():
        if key.strip().lower() == "app_home" or key.strip().lower() == "apphome":
            assert False, "App home environment variable should not be set for this test"


    # - create config directory inside app home
    _apphome = os.path.join(testRoot, ''.join(random.choices(string.ascii_letters + string.digits, k=25)))
    os.makedirs(_apphome, exist_ok=True)

    # -- set APP_HOME environment variable
    os.environ["APP_HOME"] = _apphome

    # -- yield control 
    yield _apphome

    # -- drop APP_HOME environment variable
    del os.environ["APP_HOME"]



@pytest_asyncio.fixture
async def testAppConfigPath(testAppHome):

    # -- app home config path
    app_home_cfgpath = os.path.join(testAppHome, "config")

    os.makedirs(app_home_cfgpath, exist_ok=True)

    yield app_home_cfgpath







@pytest.mark.asyncio
async def test_app_home_not_set():

    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.AppConfiguration()

    # -- assertions
    assert "App home environment variable is not set" in str(ex_details.value)



@pytest.mark.asyncio
async def test_app_home_noconfigdir(testAppHome):

    # -- stage
    test_apphome = testAppHome

    assert os.path.exists(test_apphome), "Test app home directory should exist"

    # -- test
    with pytest.raises(apx.exceptions.ConfigurationException) as ex_details:
        apx.config.AppConfiguration()


    # -- assertions
    assert "App home config directory does not exist" in str(ex_details.value)





@pytest.mark.asyncio
async def test_app_home_nopropfiles(testAppConfigPath):

    # -- stage
    cfgpath = testAppConfigPath

    assert os.path.exists(cfgpath), "Test app home config path should exist"
    assert len(os.listdir(cfgpath)) == 0


    # -- test
    result = apx.config.AppConfiguration()

    # -- assertions
    assert result.apphome is not None
    assert result.files == []
    assert result._attr == {}



@pytest.mark.asyncio
async def test_single_configfile(testAppConfigPath):

    # -- stage

    # - config path
    test_cfgpath = testAppConfigPath

    # - generate test properties
    test_props = {}
    for _ in range(5):
        test_props[ ''.join(random.choices(string.ascii_letters + string.digits, k=10)).lower()] = ''.join(random.choices(string.ascii_letters + string.digits, k=25))

    # - create a single config file
    test_file_path = os.path.join(test_cfgpath, "test.properties")
    with open(test_file_path, "w") as f:    
        for k, v in test_props.items():
            f.write(f"{k} = {v}\n")


    # -- test
    result = apx.config.AppConfiguration()


    # -- assertions
    # - app home property
    assert result.apphome == os.path.dirname(test_cfgpath)

    # - property files
    assert set(result.files) == set([test_file_path])

    # - properties
    assert set(result._attr.keys()) == set(test_props.keys())

    for k, v in test_props.items():
        assert result._attr.get(k) == v
        assert result(k) == v




@pytest.mark.asyncio
async def test_multiple_configfiles(testAppConfigPath):

    # -- stage

    # - config path
    test_cfgpath = testAppConfigPath

    # - generate test properties for multiple files
    #   note: generate matrix of 5 props for each of 3 files
    test_props = {}
    test_propfiles = []

    for q in range(3):

        _propfile = os.path.join(test_cfgpath, f"test_{q}.properties")
        test_propfiles.append(_propfile)

        with open(_propfile, "w") as f:
            for _ in range(5):
                                
                _key = ''.join(random.choices(string.ascii_letters + string.digits, k=10)).lower()
                _value = ''.join(random.choices(string.ascii_letters + string.digits, k=10)).lower()

                f.write(f"{_key} = {_value}\n")

                test_props[_key] = _value


    # -- test
    result = apx.config.AppConfiguration()


    # -- assertions

    # - app home property
    assert result.apphome == os.path.dirname(test_cfgpath)

    # - property files
    assert set(result.files) == set(test_propfiles)

    # - properties
    assert set(result._attr.keys()) == set(test_props.keys())

    for k, v in test_props.items():
        assert result._attr.get(k) == v
        assert result(k) == v

    


