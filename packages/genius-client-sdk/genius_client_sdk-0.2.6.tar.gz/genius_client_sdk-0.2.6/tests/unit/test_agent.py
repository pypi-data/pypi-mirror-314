import json
import logging

import numpy
import pytest
from genius_client_sdk.agent import GeniusAgent
from genius_client_sdk.model import GeniusModel
from unittest.mock import patch, MagicMock, mock_open, Mock
from test_fixtures import PATH_TO_SPRINKLER_VFG, PATH_TO_SPRINKLER_NOWRAPPER_VFG
from test_fixtures import start_simple_http_server_always_returns_200


@pytest.fixture(scope="function", autouse=False)
def start_server():
    server_process = start_simple_http_server_always_returns_200()
    yield
    server_process.shutdown()


@pytest.fixture
def agent():
    return GeniusAgent()


def test_structure_learning_successful():
    agent = GeniusAgent()
    csv_data = "variable1,variable2\n1,0\n0,1"
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.text = '{"factors": []}'

    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch(
            "genius_client_sdk.agent.send_csv_request", return_value=response_mock
        ):
            with patch("genius_client_sdk.agent.send_http_request") as mock_request:
                mock_request.return_value.status_code = 200
                agent.structure_learning(
                    csv_path="dummy_path.csv", learn=False, verbose=False
                )
                assert agent.model.json_model == {"factors": []}
                mock_request.assert_called_once_with(
                    agent.agent_url,
                    http_request_method="post",
                    call="graph",
                    json_data={"vfg": agent.model.json_model},
                )


def test_structure_learning_fails_with_invalid_csv():
    agent = GeniusAgent()
    csv_data = "invalid_csv_data"
    response_mock = MagicMock()
    response_mock.status_code = 400
    response_mock.text = "Error"

    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch(
            "genius_client_sdk.agent.send_csv_request", return_value=response_mock
        ):
            with pytest.raises(
                AssertionError, match="Error performing structure learning: Error"
            ):
                agent.structure_learning(
                    csv_path="dummy_path.csv", learn=False, verbose=False
                )


def test_structure_learning_calls_parameter_learning():
    agent = GeniusAgent()
    csv_data = "variable1,variable2\n1,0\n0,1"
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.text = '{"factors": []}'
    learn_response_mock = MagicMock()
    learn_response_mock.status_code = 200
    learn_response_mock.text = '{"result": "success"}'

    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch(
            "genius_client_sdk.agent.send_csv_request", return_value=response_mock
        ):
            with patch(
                "genius_client_sdk.agent.send_http_request",
                return_value=learn_response_mock,
            ):
                agent.structure_learning(
                    csv_path="dummy_path.csv", learn=True, verbose=False
                )
                assert agent.model.json_model == {"factors": []}


def test_logs_summarized_model_contents(start_server):
    agent = GeniusAgent()

    with open(PATH_TO_SPRINKLER_NOWRAPPER_VFG, "r") as file:
        json_model = json.load(file)
    model = GeniusModel(agent.agent_url)
    model.json_model = json_model

    agent.model = model

    agent.logger = MagicMock()
    agent.log_model(summary=True)

    # these validations could be more robust but this is a start
    agent.logger.log.assert_any_call(logging.INFO, "Model contents:")
    agent.logger.log.assert_any_call(
        logging.INFO, "4 variables: ['cloudy', 'rain', 'sprinkler', 'wet_grass']"
    )
    agent.logger.log.assert_any_call(
        logging.INFO,
        "4 factors: [['cloudy'], ['rain', 'cloudy'], ['sprinkler', 'cloudy'], ['wet_grass', 'sprinkler', 'rain']]",
    )
    agent.logger.log.assert_any_call(logging.INFO, "Factor probabilities:")
    agent.logger.log.assert_any_call(logging.INFO, "[0.5 0.5]")
    agent.logger.log.assert_any_call(logging.INFO, "[[0.8 0.2]\n [0.2 0.8]]")
    agent.logger.log.assert_any_call(logging.INFO, "[[0.5 0.9]\n [0.5 0.1]]")
    agent.logger.log.assert_any_call(
        logging.INFO, "[[[1.   0.1 ]\n  [0.1  0.01]]\n\n [[0.   0.9 ]\n  [0.9  0.99]]]"
    )


def test_raises_exception_when_no_model_loaded():
    agent = GeniusAgent()
    with pytest.raises(
        Exception,
        match="No model loaded. load_genius_model\(\) must be run before viewing the model.",
    ):
        agent.log_model()


def test_load_model_from_json(agent, start_server):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 200
        agent.load_model_from_json(PATH_TO_SPRINKLER_VFG)
        assert agent.model is not None


def test_load_model_from_json_failure(agent, start_server):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 400
        with pytest.raises(AssertionError):
            agent.load_model_from_json(PATH_TO_SPRINKLER_VFG)


def test_infer(agent):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = r'{"result": {"evidence": {}, "probabilities": {}}, "success": true, "error": null, "metadata": {"execution_time": 0, "memory_used": 0}}'
        result = agent.infer("variable_id", {"evidence": "data"})
        assert "probabilities" in result


def test_infer_failure(agent):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 400
        with pytest.raises(AssertionError):
            agent.infer("variable_id", {"evidence": "data"})


def test_learn(agent):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"model": "data"}
        result = agent.learn(variables=["var1"], observations=[[1]])
        assert "model" in result


def test_learn_failure(agent):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 400
        with pytest.raises(AssertionError):
            agent.learn(variables=["var1"], observations=[[1]])


def test_act(agent):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = r'{"result": {"action_data": {}, "belief_state": {}, "policy_belief": {}, "efe_components": {}}, "success": true, "error": null, "warnings": null, "metadata": {"execution_time": 0.5, "memory_used": [0.125, "MB"]}}'
        result = agent.act(numpy.array([1, 2, 3]))
        assert "belief_state" in result
        assert "policy_belief" in result
        assert "efe_components" in result
        assert "action_data" in result
        assert "metadata" in result
        assert "success" in result["metadata"]
        assert "error" in result["metadata"]
        assert "warnings" in result["metadata"]
        assert "execution_time" in result["metadata"]
        assert "memory_used" in result["metadata"]


def test_act_failure(agent):
    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 400
        with pytest.raises(AssertionError):
            agent.act(numpy.array([1, 2, 3]))


def test_logs_raw_json_model():
    agent = GeniusAgent()
    model_mock = MagicMock()
    model_mock.json_model = {"factors": []}
    agent.model = model_mock
    agent.logger = MagicMock()

    agent.log_model(summary=False, logging_level=logging.INFO)

    agent.logger.log.assert_called_with(
        logging.INFO, json.dumps({"factors": []}, indent=4)
    )


def test_fails_to_log_model_when_no_model_loaded():
    agent = GeniusAgent()
    agent.logger = MagicMock()

    with pytest.raises(
        Exception,
        match="No model loaded. load_genius_model\(\) must be run before viewing the model.",
    ):
        agent.log_model(summary=False, logging_level=logging.INFO)


@patch(
    "builtins.open", new_callable=mock_open, read_data="variable1,variable2\n1,2\n3,4"
)
@patch("genius_client_sdk.agent.send_http_request")
def test_learn_with_mocked_file(mock_send_http_request, mock_file):
    # Mock the response from send_http_request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "mocked result"}
    mock_send_http_request.return_value = mock_response

    # Create an instance of GeniusAgent
    agent = GeniusAgent()
    with patch.object(agent.logger, "info") as mock_logger_info:
        # Call the learn method with the mocked file path
        agent.learn(csv_path="mocked_path.csv", verbose=True)

        # Check that the log contains the expected output
        mock_logger_info.assert_called_with(json.dumps(mock_response.json(), indent=4))


def test_structure_learning_verbose_logging():
    agent = GeniusAgent()
    csv_data = "variable1,variable2\n1,0\n0,1"
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.text = '{"factors": []}'
    learn_response_mock = MagicMock()
    learn_response_mock.status_code = 200
    learn_response_mock.json.return_value = {"model": "data"}

    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch(
            "genius_client_sdk.agent.send_csv_request", return_value=response_mock
        ):
            with patch(
                "genius_client_sdk.agent.send_http_request",
                return_value=learn_response_mock,
            ):
                with patch.object(agent.logger, "info") as mock_logger_info:
                    agent.structure_learning(
                        csv_path="dummy_path.csv", learn=True, verbose=True
                    )
                    mock_logger_info.assert_called_with(
                        json.dumps(learn_response_mock.json(), indent=4)
                    )


def test_structure_learning_passes_correct_agent_url():
    agent1 = GeniusAgent(agent_hostname="localhost")
    agent2 = GeniusAgent(agent_hostname="127.0.0.1")
    csv_data = "variable1,variable2\n1,0\n0,1"
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.text = '{"factors": []}'
    learn_response_mock = MagicMock()
    learn_response_mock.status_code = 200
    learn_response_mock.json.return_value = {"model": "data"}

    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch(
            "genius_client_sdk.agent.send_csv_request", return_value=response_mock
        ):
            with patch(
                "genius_client_sdk.agent.send_http_request",
                return_value=learn_response_mock,
            ):
                with patch("genius_client_sdk.agent.GeniusModel") as mock_genius_model:
                    agent1.structure_learning(csv_path="dummy_path.csv", learn=True)
                    mock_genius_model.assert_called_with(
                        agent_url=agent1.agent_url, version=agent1.build_version
                    )
                    agent2.structure_learning(csv_path="dummy_path.csv", learn=True)
                    mock_genius_model.assert_called_with(
                        agent_url=agent2.agent_url, version=agent2.build_version
                    )


def test_load_model_from_json_passes_correct_agent_url_and_version(start_server):
    agent1 = GeniusAgent(agent_hostname="localhost", build_version="1.0")
    agent2 = GeniusAgent(agent_hostname="127.0.0.1", build_version="2.0")

    with patch("genius_client_sdk.agent.send_http_request") as mock_request:
        mock_request.return_value.status_code = 200
        with patch("genius_client_sdk.agent.GeniusModel") as mock_genius_model:
            agent1.load_model_from_json(PATH_TO_SPRINKLER_VFG)
            mock_genius_model.assert_called_with(
                agent_url=agent1.agent_url,
                version=agent1.build_version,
                json_path=PATH_TO_SPRINKLER_VFG,
            )

            agent2.load_model_from_json(PATH_TO_SPRINKLER_VFG)
            mock_genius_model.assert_called_with(
                agent_url=agent2.agent_url,
                version=agent2.build_version,
                json_path=PATH_TO_SPRINKLER_VFG,
            )
