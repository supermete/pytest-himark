from pathlib import Path

current_directory = Path(__file__).parent
config_json = current_directory.joinpath('config.json')
config_disabled_json = current_directory.joinpath('config_disabled.json')


def test_json_filter1(pytester):
    """Check that only tests matching the marker from config.json is executed."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest
        
        @pytest.mark.marker1
        def test_marker1():
            assert True
            
        @pytest.mark.marker2
        def test_marker2():
            assert True
        
        def test_marker3():
            assert True
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        f'--json={config_json}',
        '-vvv'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker2 PASSED*',
    ])
    result.stdout.no_fnmatch_line(
        '*::test_marker1 PASSED*',
    )
    result.stdout.no_fnmatch_line(
        '*::test_marker3 PASSED*'
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_json_filter2(pytester):
    """Check that only tests matching the marker from config.json is executed."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest
        
        @pytest.mark.marker2
        def test_marker1():
            assert True
            
        @pytest.mark.marker1
        def test_marker2():
            assert True
            
        def test_marker3():
            assert True
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        f'--json={config_json}',
        '-vvv'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker1 PASSED*',
    ])
    result.stdout.no_fnmatch_line(
        '*::test_marker2 PASSED*'
    )
    result.stdout.no_fnmatch_line(
        '*::test_marker3 PASSED*'
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_json_filter3(pytester):
    """Check that tests that are marked with at least one disabled marker is not executed."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest
        
        @pytest.mark.marker1
        @pytest.mark.marker2
        def test_marker1():
            assert True
            
        @pytest.mark.marker2
        def test_marker2():
            assert True
            
        def test_marker3():
            assert True
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        f'--json={config_json}',
        '-vvv'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker2 PASSED*',
    ])
    result.stdout.no_fnmatch_line(
        '*::test_marker1 PASSED*'
    )
    result.stdout.no_fnmatch_line(
        '*::test_marker3 PASSED*'
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_json_filter_none(pytester):
    """Check that all tests are executed when no json is used."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest
        
        @pytest.mark.marker2
        def test_marker1():
            assert True
            
        @pytest.mark.marker1
        def test_marker2():
            assert True
        
        def test_marker3():
            assert True
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        '-vvv'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker1 PASSED*',
        '*::test_marker2 PASSED*',
        '*::test_marker3 PASSED*',
    ])

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_json_filter_disabled(pytester):
    """Check that all tests are executed when all markers are disabled."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest
        
        @pytest.mark.marker2
        def test_marker1():
            assert True
            
        @pytest.mark.marker1
        def test_marker2():
            assert True
        
        def test_marker3():
            assert True
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        f'--json={config_disabled_json}',
        '-vvv'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker1 PASSED*',
        '*::test_marker2 PASSED*',
        '*::test_marker3 PASSED*',
    ])

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_json_filter_device(pytester):
    """
    Check that markers are correctly created from 'devices' in json, and properly filters out the test collection.
    Markers 3, 4, 5 and 6 should be created since device1 and device2 have their 'used' key set to true in config.json.
    device3 has 'used' set to false in config.json so marker7 and marker8 should not be enabled.

    :param pytester: fixture
    :return: None
    """

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest

        @pytest.mark.marker3
        def test_device1_output1():
            assert True

        @pytest.mark.marker4
        def test_device1_output2():
            assert True
            
        @pytest.mark.marker5
        def test_device2_input1():
            assert True
            
        @pytest.mark.marker6
        def test_device2_input2():
            assert True
            
        @pytest.mark.marker7
        def test_device3_output1():
            assert True
            
        @pytest.mark.marker8
        def test_device3_input1():
            assert True
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        f'--json={config_json}',
        '-vvv'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_device1_output1 PASSED*',
        '*::test_device1_output2 PASSED*',
        '*::test_device2_input1 PASSED*',
        '*::test_device2_input2 PASSED*',
    ])
    result.stdout.no_fnmatch_line(
        '*::test_device3_output1 PASSED*',
    )
    result.stdout.no_fnmatch_line(
        '*::test_device3_input1 PASSED*'
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0