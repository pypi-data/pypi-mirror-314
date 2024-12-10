import json
import logging
import os
from unittest.mock import patch, mock_open, MagicMock

import pytest
import numpy as np

from genius_client_sdk.configuration import default_agent_config
from genius_client_sdk.model import GeniusModel
from test_fixtures import (
    start_simple_http_server_always_returns_200,
    start_simple_http_server_always_returns_400,
)


@pytest.fixture(scope="function", autouse=False)
def start_server():
    server_process = start_simple_http_server_always_returns_200()
    yield
    server_process.shutdown()


@pytest.fixture(scope="function", autouse=False)
def start_server_bad():
    server_process = start_simple_http_server_always_returns_400()
    yield
    server_process.shutdown()


def test_add_variables(start_server):
    model = GeniusModel()
    model.add_variables([("var1", ["v11", "v12"]), ("var2", ["v21", "v22"])])
    assert sorted(model.get_variable_names()) == ["var1", "var2"]
    assert sorted(model.get_variable_values("var1")) == ["v11", "v12"]
    assert sorted(model.get_variable_values("var2")) == ["v21", "v22"]


def test_adds_factor_with_role_name():
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1", role="likelihood")
    assert model.json_model["factors"][0]["role"] == "likelihood"
    assert model.json_model["factors"][0]["variables"] == ["var1"]


def test_adds_factor_without_role_name():
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1")
    assert model.json_model["factors"][0]["variables"] == ["var1"]
    assert model.json_model["factors"][0]["distribution"] == "categorical"
    assert model.json_model["factors"][0]["values"] == [0.1, 0.9]
    assert "role" not in model.json_model["factors"][0]


def test_add_factor_without_variables_raises_exception():
    model = GeniusModel()
    with pytest.raises(Exception) as excinfo:
        model.add_factor(np.array([0.1, 0.9]), "var1")
    assert "Variables must be added to the model before factors can be added." in str(
        excinfo.value
    )


def test_add_factor_with_nonexistent_variable_raises_assertion():
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    with pytest.raises(AssertionError) as excinfo:
        model.add_factor(np.array([0.1, 0.9]), "var2")
    assert "Variables var2 not in the list of added variables." in str(excinfo.value)


def test_add_factor_with_mismatched_dimensions_raises_assertion():
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    with pytest.raises(AssertionError):
        model.add_factor(np.array([[0.1, 0.9], [0.2, 0.8]]), "var1")
    assert "Number of variables associated with factor does not match the dimension of the factor values."


def test_validate_model_with_all_components(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1", role="likelihood")
    model.validate()
    assert model.json_model["factors"][0]["role"] == "likelihood"
    assert model.json_model["variables"]["var1"]["elements"] == ["v1", "v2"]


def test_validate_model_missing_components_raises_exception(start_server_bad):
    model = GeniusModel()
    with pytest.raises(Exception) as excinfo:
        model.validate()
    assert "Validation error" in str(excinfo.value)


def test_add_variable_toggles_flag(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    assert "var1" in model.json_model["variables"]
    assert model.json_model["variables"]["var1"]["elements"] == ["v1", "v2"]


def test_add_factor_toggles_flag(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1", role="likelihood")
    assert model.json_model["factors"][0]["role"] == "likelihood"
    assert model.json_model["factors"][0]["variables"] == ["var1"]
    assert model.json_model["factors"][0]["values"] == [0.1, 0.9]


def test_save_model_creates_json_file(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1", role="likelihood")
    file_path = "model.json"
    model.save(file_path)

    assert os.path.exists(file_path)
    with open(file_path, "r") as f:
        saved_model = json.load(f)
    assert saved_model["variables"]["var1"]["elements"] == ["v1", "v2"]
    assert saved_model["factors"][0]["role"] == "likelihood"


def test_visualize_model_creates_graph(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1", role="likelihood")
    model.visualize()
    assert True  # Assuming visualize does not raise an exception


def test_get_variable_values_returns_correct_values(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    values = model.get_variable_values("var1")
    assert values == ["v1", "v2"]


def test_get_variable_names_returns_correct_names(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    names = model.get_variable_names()
    assert names == ["var1"]


def test_get_factor_attributes_returns_correct_attributes(start_server):
    model = GeniusModel()
    model.add_variable("var1", ["v1", "v2"])
    model.add_factor(np.array([0.1, 0.9]), "var1", role="likelihood")
    attributes = model.get_factor_attributes(0, "role")
    assert str(attributes) == "FactorRole.Likelihood"


def test_initializes_with_default_version():
    model = GeniusModel()
    assert model.json_model["version"] == default_agent_config.build_version
    assert model.json_model["factors"] == []
    assert model.json_model["variables"] == {}


def test_initializes_with_provided_version():
    version = "1.0.0"
    model = GeniusModel(version=version)
    assert model.json_model["version"] == version
    assert model.json_model["factors"] == []
    assert model.json_model["variables"] == {}


def test_initializes_with_json_path(start_server):
    json_path = "path/to/json"
    with patch(
        "builtins.open",
        mock_open(read_data='{"factors": [], "variables": {}, "version": "1.0.0"}'),
    ):
        model = GeniusModel(json_path=json_path)
    assert model.json_model["version"] == "1.0.0"
    assert model.json_model["factors"] == []
    assert model.json_model["variables"] == {}


def test_initializes_logger_correctly():
    with patch.object(
        logging, "getLogger", return_value=MagicMock()
    ) as mock_get_logger:
        GeniusModel()
        mock_get_logger.assert_called_once_with("genius_client_sdk.model.GeniusModel")


def test_get_factor_distribution():
    # Create a mock VFG object
    mock_vfg = MagicMock()
    mock_vfg.factors = {0: MagicMock(distribution="categorical")}

    # Patch the _to_vfg method to return the mock VFG object
    with patch.object(GeniusModel, "_to_vfg", return_value=mock_vfg):
        model = GeniusModel()
        distribution = model.get_factor_attributes(
            factor_id=0, attribute="distribution"
        )

        assert distribution == "categorical"


def test_get_factor_attributes_unrecognized_attribute():
    model = GeniusModel()

    with patch.object(model, "_to_vfg") as mock_to_vfg:
        mock_to_vfg.return_value = type(
            "MockVFG", (object,), {"factors": {0: type("MockFactor", (object,), {})()}}
        )()

        with pytest.raises(
            KeyError,
            match=r"Unrecognized attribute unknown_attribute\. Attribute must be one of 'variables', 'distribution', 'values', or 'role'\.",
        ):
            model.get_factor_attributes(0, "unknown_attribute")


def test_add_factor_with_parents():
    model = GeniusModel()

    # Add variables first
    model.add_variable("A", [0, 1])
    model.add_variable("B", [0, 1])
    model.add_variable("C", [0, 1])

    # Define factor values
    values = np.array([[[0.1, 0.9], [0.8, 0.2]], [[0.3, 0.7], [0.6, 0.4]]])

    # Add factor with parents
    model.add_factor(values=values, target="A", parents=["B", "C"])

    # Check if the factor was added correctly
    assert len(model.json_model["factors"]) == 1
    assert model.json_model["factors"][0]["variables"] == ["A", "B", "C"]
