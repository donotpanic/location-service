import pytest
from location_service import main, get_lat_lon


@pytest.mark.parametrize("location_input, expected_name", [
    ("San Francisco", "San Francisco"),
    ("94103", "San Francisco"),
])
def test_valid_response(location_input, expected_name):
    result = get_lat_lon(location_input)
    assert result[0].get("name") == expected_name
    assert len(result[0]) == 3


@pytest.mark.parametrize("location_input", [
    ("InvalidCity"),
    ("00000"),
])
def test_invalid_city(location_input):
    result = get_lat_lon(location_input)
    assert result == [None]


def test_mixed_valid_and_invalid():
    test_cities = ["San Francisco", None, None, "San Francisco"]
    result = get_lat_lon("San Francisco, CA", "00000", "InvalidCity", "94103")
    for i, r in enumerate(test_cities):
        if r is None:
            assert r == result[i]
        else:
            assert r == result[i].get("name")


def test_empty_input():
    result = get_lat_lon()
    assert result == []


def test_whitespace_city():
    result = get_lat_lon(" San Francisco  ")
    assert result[0].get("name") == "San Francisco"


@pytest.mark.parametrize("cli_args, expected_output", [
    (["San Francisco, CA", "New York, NY"], [
        "Location: San Francisco",
        "  City: San Francisco",
        "Location: New York",
        "  City: New York",
    ]),
    (["94103", "10001"], [
        "Location: 94103",
        "  City: San Francisco",
        "Location: 10001",
        "  City: New York",
    ]),
])
def test_command_line_utility(monkeypatch, capsys, cli_args, expected_output):
    monkeypatch.setattr('sys.argv', ['program_name'] + cli_args)

    main()

    captured = capsys.readouterr()

    for line in expected_output:
        assert line in captured.out

# TODO: Add test cases for LAT/LON verification
# TODO: Add test case for API KEY not found
# TODO: Add additional error handling test cases
