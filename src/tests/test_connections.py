from unittest import mock
import pytest
import dogdash.connections
import json

def test_secrets_to_file(mocker):
    mock_secret = {"this": "that"}
    mocked_get_secrets = mocker.patch(
        "dogdash.connections.get_secret",
        return_value=mock_secret
    )

    test_filepath = dogdash.connections.secret_to_file("garbage", "region")

    with open(test_filepath) as f:
        test_secret = json.load(f)
    assert test_secret == mock_secret