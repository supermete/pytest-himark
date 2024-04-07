from pathlib import Path

current_directory = Path(__file__).parent
config_json = current_directory.joinpath('config.json')


def test_json_filter(pytester):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        import pytest
        
        @pytest.mark.marker1
        def test_marker1():
            assert True
            
        @pytest.mark.marker2
        def test_marker2():
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

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0
