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
