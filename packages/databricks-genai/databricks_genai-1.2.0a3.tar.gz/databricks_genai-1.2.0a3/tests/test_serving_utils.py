from unittest.mock import Mock, patch

import pytest

from databricks.model_serving.utils import get_latest_model_version, get_model_specs


class MockModelVersion:

    def __init__(self, version: str):
        self.version = version


def test_get_latest_model_version_single_version():
    # Arrange
    model_name = 'test_model'
    mock_version = MockModelVersion('1')

    mock_client = Mock()
    mock_client.search_model_versions.return_value = [mock_version]

    with patch('databricks.model_serving.utils.MlflowClient', return_value=mock_client):
        result = get_latest_model_version(model_name)

    # Assert
    mock_client.search_model_versions.assert_called_once_with("name='test_model'")
    assert result == '1'


def test_get_latest_model_version_multiple_versions():
    # Arrange
    model_name = 'test_model'
    mock_versions = [MockModelVersion('1'), MockModelVersion('2'), MockModelVersion('3')]
    mock_client = Mock()
    mock_client.search_model_versions.return_value = mock_versions

    with patch('databricks.model_serving.utils.MlflowClient', return_value=mock_client):
        result = get_latest_model_version(model_name)

    # Assert
    mock_client.search_model_versions.assert_called_once_with("name='test_model'")
    assert result == '3'


def test_get_latest_model_version_unordered_versions():
    # Arrange
    model_name = 'test_model'
    mock_versions = [MockModelVersion('2'), MockModelVersion('1'), MockModelVersion('5'), MockModelVersion('3')]
    mock_client = Mock()
    mock_client.search_model_versions.return_value = mock_versions

    with patch('databricks.model_serving.utils.MlflowClient', return_value=mock_client):
        result = get_latest_model_version(model_name)

    # Assert
    mock_client.search_model_versions.assert_called_once_with("name='test_model'")
    assert result == '5'


def test_get_latest_model_version_empty_list():
    # Arrange
    model_name = 'test_model'
    mock_client = Mock()
    mock_client.search_model_versions.return_value = []

    with patch('databricks.model_serving.utils.MlflowClient', return_value=mock_client):
        with pytest.raises(ValueError):
            result = get_latest_model_version(model_name)


def test_all_model_specs_have_required_fields():
    # These fields may not apply to all models, but they
    # definitely apply to all "base" models that we want to use
    # TODO: We should also test for endpoint because it is required for the ground_truth models
    with patch('databricks.model_serving.utils.get_latest_model_version', return_value='1'):
        model_specs = get_model_specs()
        for model_spec in model_specs.values():
            assert model_spec.ft_model_name is not None
            assert model_spec.uc_schema is not None
