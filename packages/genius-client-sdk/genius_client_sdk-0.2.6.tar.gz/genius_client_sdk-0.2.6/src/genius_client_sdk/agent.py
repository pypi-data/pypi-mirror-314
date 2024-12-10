import json
import logging

import numpy as np

from genius_client_sdk.model import GeniusModel
from genius_client_sdk.configuration import default_agent_config, BaseAgentConfig
from genius_client_sdk.utils import (
    control_payload,
    inference_payload,
    learning_payload,
    send_csv_request,
    send_http_request,
)


class GeniusAgent:
    """
    The GeniusAgent class is used as a wrapper around fastAPI to communicate to and from the Genius
    agent. This class has the following capabilities enabled by the API calls:
    - POST /graph of genius model loaded from a JSON or from the GeniusModel class
    - GET /graph of genius model and print/view its contents
    - POST /infer to perform inference given some evidence and a variable of interest
    - POST /learn to perform parameter learning given an input CSV or list of variables and their
      observations
    - POST /actionselection to perform action selection given a POMDP model structure and
      observation vector
    - POST /import to perform structure learning given a CSV data file

    At the moment, it is assumed that the user connects to a local GeniusAgent. In the future,
    initializing this class will have options to specify a URL and port.
    """

    def __init__(
        self,
        agent_http_protocol: str = default_agent_config.agent_http_protocol,
        agent_hostname: str = default_agent_config.agent_hostname,
        agent_port: int = default_agent_config.agent_port,
        build_version: str = default_agent_config.build_version,
    ) -> None:
        """
        Initializes the GeniusAgent instance.

        Attributes:
        model (GeniusModel or None): The model loaded into the agent. Initially set to None.
        """
        self.model = None
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self.agent_http_protocol = agent_http_protocol
        self.agent_hostname = agent_hostname
        self.agent_port = agent_port
        self.build_version = build_version
        self.agent_url = BaseAgentConfig.AGENT_URL_FORMAT.format_map(locals())

    def load_model_from_json(self, json_path: str) -> None:
        """
        Load a JSON model from a path.

        Parameters:
        json_path (str): The path to the JSON file containing the model.
        """

        # Turn into GeniusModel class
        self.load_genius_model(
            GeniusModel(
                agent_url=self.agent_url,
                version=self.build_version,
                json_path=json_path,
            )
        )

    def load_genius_model(self, model: GeniusModel) -> None:
        """
        Load a model from the GeniusModel class.

        Parameters:
        model (GeniusModel): An instance of the GeniusModel class.
        """

        # POST /graph with dict representation of JSON model
        self.model = model

        response = send_http_request(
            self.agent_url,
            http_request_method="post",
            call="graph",
            json_data={"vfg": self.model.json_model},
        )

        assert response.status_code == 200, "Loading model failed: " + str(
            response.text
        )

    def log_model(
        self, summary: bool = False, logging_level: int = logging.INFO
    ) -> None:
        """
        Prints the JSON model to logs.
        Optionally, summarizes the model in a (slightly) more readable format.

        Parameters:
        summary (bool): If True, prints a summarized view of the model. Defaults to False.
        logging_level (int): The logging level to use. Defaults to DEFAULT_LOGGING_LEVEL.
        """

        if not self.model:
            raise Exception(
                "No model loaded. load_genius_model() must be run before viewing the model."
            )

        # Log summarized and easy-to-read view of model contents instead of raw JSON
        if summary:
            self.logger.log(logging_level, "Model contents:")

            # Log number of variables in the model and their names
            x = f"{len(self.model.get_variable_names())} variables: {sorted(self.model.get_variable_names())}"
            self.logger.log(logging_level, x)

            # Log number of factors in the model and their names
            n_factors = len(self.model.json_model["factors"])
            factor_vars = [
                self.model.get_factor_attributes(factor_id=f, attribute="variables")
                for f in range(n_factors)
            ]
            self.logger.log(
                logging_level, f"{n_factors} factors: {sorted(factor_vars)}"
            )

            # Log all factor probabilities
            self.logger.log(logging_level, "Factor probabilities:")
            for f in range(n_factors):
                self.logger.log(
                    logging_level,
                    str(
                        self.model.get_factor_attributes(
                            factor_id=f, attribute="values"
                        )
                    ),
                )
                self.logger.log(logging_level, "\n")
        else:
            self.logger.log(
                logging_level, json.dumps(self.model.json_model, indent=4)
            )  # Prints raw JSON model

    def infer(self, variable_id: str, evidence: dict, verbose: bool = True) -> dict:
        """
        Run inference based on input variable to infer and evidence (observed data).

        Parameters:
        variable_id (str): The ID of the variable to infer.
        evidence (dict): A dictionary containing observed data.
        verbose (bool): If True, prints out probabilities. Defaults to True.

        Returns:
        dict: A dictionary containing the inference result.
        """

        # Collects input into correct schema for the API request
        payload = inference_payload(variable_id=variable_id, evidence=evidence)

        # POST /infer with variables and evidence
        response = send_http_request(
            self.agent_url,
            http_request_method="post",
            call="infer",
            json_data=payload,
        )

        assert (
            response.status_code == 200
        ), f"Error performing inference: {str(response.text)}."

        # Rearranges return from API so that success and error are now under metadata
        inference_result = json.loads(response.text)
        inference_result = {
            "evidence": inference_result["result"]["evidence"],
            "probabilities": inference_result["result"]["probabilities"],
            "metadata": {
                "success": inference_result["success"],
                "error": inference_result["error"],
                "execution_time": inference_result["metadata"]["execution_time"],
                "memory_used": inference_result["metadata"]["memory_used"],
            },
        }

        # Prints out probabilities
        if verbose:
            self.logger.info(inference_result["probabilities"])

        return inference_result

    def learn(
        self,
        variables: list = None,
        observations: list = None,
        csv_path: str = None,
        verbose: bool = False,
    ) -> None:
        """
        Run learning based on observations of variables. Accepts either a list of variables and
        nested list of observations or a path to a CSV file.

        Parameters:
        variables (list): A list of variables to learn.
        observations (list): A nested list of observations for the variables.
        csv_path (str): The path to a CSV file containing the observations.
        verbose (bool): If True, prints out the JSON model file. Defaults to False.

        Returns:
        dict: A dictionary containing the learning result.
        """

        # Collects input into correct schema for the API request
        payload = learning_payload(
            variables=variables, observations=observations, csv_path=csv_path
        )

        # POST /learn with variables/observations or CSV containing this information
        response = send_http_request(
            self.agent_url,
            http_request_method="post",
            call="learn",
            json_data=payload,
        )

        assert (
            response.status_code == 200
        ), f"Error performing parameter learning: {str(response.text)}."

        self.logger.info(
            "Parameter learning successful. Use log_model() to see updated probabilities."
        )

        # Prints out JSON model file
        if verbose:
            self.logger.info(json.dumps(response.json(), indent=4))

        return response.json()

    def act(self, observation: np.ndarray, policy_len: int = 2, verbose: bool = True):
        """
        Performs action selection given an observation array and policy length.

        Parameters:
        observation (np.ndarray): An array containing the observation data.
        policy_len (int): The length of the policy. Defaults to 2.
        verbose (bool): If True, prints out the action, inferred state, and policy distribution. Defaults to True.

        Returns:
        dict: A dictionary containing the action selection result.
        """

        # TODO: Assert number of observations matches observation variable length

        # Collects input into correct scheme for the API request
        payload = control_payload(
            observation=observation,
            policy_len=policy_len,
        )

        # POST /actionselection with observation and policy length
        response = send_http_request(
            self.agent_url,
            http_request_method="post",
            call="actionselection",
            json_data=payload,
        )

        assert (
            response.status_code == 200
        ), f"Action selection failed: {str(response.text)}."

        # Rearranges return from API so that success and error are now under metadata
        control_result = json.loads(response.text)
        # control_result is defined in GPAI-159
        control_result = {
            "belief_state": control_result["result"]["belief_state"],
            "policy_belief": control_result["result"]["policy_belief"],
            "efe_components": control_result["result"]["efe_components"],
            "action_data": control_result["result"]["action_data"],
            "metadata": {
                "success": control_result["success"],
                "error": control_result["error"],
                "warnings": control_result["warnings"],
                "execution_time": control_result["metadata"]["execution_time"],
                # Note: memory_used is an array, e.g. [0.125, "MB"]
                "memory_used": control_result["metadata"]["memory_used"],
            },
        }

        if verbose:
            self.logger.info(f"Action: {control_result['action_data']}")
            self.logger.info(f"Inferred state: {control_result['belief_state']}")
            self.logger.info(f"Policy distribution: {control_result['policy_belief']}")

        return control_result

    def structure_learning(
        self,
        csv_path: str = None,
        learn: bool = True,
        verbose: bool = False,
    ) -> None:
        """
        Performs structure learning given a CSV file. Structure learning entails taking a dataset
        and attempting to build the dependencies in a probabilistic model from it. The resulting
        model is then sent to the connected Genius agent.

        If the learning argument is true, GeniusAgent.learn() will also be called to fill in the
        probabilities.

        Accepts either a list of variables and nested list of observations or a path to a CSV
        file.
        """

        # Open the CSV file and read its contents
        with open(csv_path, "r") as file:
            csv_data = file.read()

        # POST /import with loaded CSV
        response = send_csv_request(self.agent_url, data=csv_data, call="import")

        assert (
            response.status_code == 200
        ), f"Error performing structure learning: {str(response.text)}."

        self.logger.info(
            "Structure learning successful. Use log_model() to see learned structure."
        )

        # Send model dict to GeniusModel class
        model = GeniusModel(agent_url=self.agent_url, version=self.build_version)
        model.json_model = json.loads(response.text)

        # Send model to agent
        self.model = model
        self.load_genius_model(model=self.model)

        if learn:
            # Collect input into correct schema for the API request
            payload = learning_payload(
                variables=None, observations=None, csv_path=csv_path
            )

            # POST /learn with variables/observations or CSV containing this information
            response = send_http_request(
                self.agent_url,
                http_request_method="post",
                call="learn",
                json_data=payload,
            )

            assert (
                response.status_code == 200
            ), f"Error performing learning: {str(response.text)}."

            self.logger.info(
                "Parameter learning successful. Use log_model() to see learned probabilities."
            )

        # Prints out JSON model file
        if verbose:
            self.logger.info(json.dumps(response.json(), indent=4))
