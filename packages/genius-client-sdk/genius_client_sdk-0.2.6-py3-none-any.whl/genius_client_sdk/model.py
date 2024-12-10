import json
import logging

import networkx as nx
import numpy as np

from pyvfg import vfg_from_json

from genius_client_sdk.configuration import default_agent_config
from genius_client_sdk.utils import send_http_request

import io


class GeniusModel:
    """
    The GeniusModel class is used to build factor graphs from scratch. The class has the following
    capabilities:
    - Create a model from a JSON file path
    - Construct model by adding variables or factors
    - Validate a constructed model with POST /validate in the fastAPI
    - Save (export) a model to JSON
    - Visualize the model with networkx
    - Get variable names and values for a given model
    - Get factor attributes for a given model

    Internally, the model is stored in the json_model instance variable and is just a dict that is
    converted to and from JSON as needed.

    In the future, many of the methods in this class will become part of pyvfg and this class will
    likely become a wrapper around pyvfg.
    """

    def __init__(
        self,
        agent_url: str = default_agent_config.agent_url,
        version: str = default_agent_config.build_version,
        json_path: str = None,
    ) -> None:
        """
        Initializes the GeniusModel.

        Parameters:
        version (str): The version of the model, default is the build version from Constants.
        json_path (str, optional): The path to the JSON file for the model. Defaults to None.
        """
        self.agent_url = agent_url
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

        """Builds the skeleton JSON model dict."""

        if json_path:
            self._from_json(json_path)
        else:
            self.json_model = {
                "factors": [],
                "variables": {},
                "version": version,
            }

    def _from_json(self, json_path: str) -> None:
        """
        Loads a JSON file to a dict and validates it.

        Parameters:
        json_path (str): The path to the JSON file.
        """
        with open(json_path, "r") as file:
            self.json_model = json.load(file)

        self.validate(verbose=False)

    def add_variables(self, variables: list[tuple[str, list]]) -> None:
        """
        Adds a list of variables to the JSON model dict.

        Parameters:
        name (str): The name of the variable.
        values (list): The values for the variable.
        """
        for variable in variables:
            self.add_variable(variable[0], variable[1])

    def add_variable(self, name: str, values: list) -> None:
        """
        Adds a variable to the JSON model dict.

        Parameters:
        name (str): The name of the variable.
        values (list): The values for the variable.
        """
        self.json_model["variables"][name] = {"elements": values}

    def add_factor(
        self,
        values: np.ndarray,
        target: str,
        parents: list[str] = None,
        role: str = None,
    ):
        """
        Adds a factor to the JSON model. Note: The reason for separating the conditioned variable
        from its parents is to be able to construct the variable list as:

        [conditioning variable, parent_1, parent_2, ...]

        This structure is assumed in the VFG format but not explicitly stated. By asking the user
        to construct the variable and its parents in this way it avoids situations where the user
        might input the variables in the wrong order.

        In the case of marginal distributions the parents field would be left defaulting to None.

        Parameters:
        values (np.ndarray): The values for the factor.
        target (str): The conditioned (target) variable. Defaults to None.
        parents (list[str]): The conditioning (parent) variables.
        role (str, optional): The role of the factor. Defaults to None.
        """

        if parents:
            variables = [target] + parents
        else:
            variables = [target]

        # Checks that variables have been added before attempting to build the factors
        if not self.json_model["variables"]:
            raise Exception(
                "Variables must be added to the model before factors can be added."
            )

        # Assert that factors are part of variable list
        for var in variables:
            added_variables = list(self.json_model["variables"].keys())
            assert (
                var in added_variables
            ), f"Variables {var} not in the list of added variables. Added variables: {added_variables}."

        # Assert that number of variables match tensor rank
        assert (
            len(variables) == len(list(values.shape))
        ), "Number of variables associated with factor does not match the dimension of the factor values."

        # Add factor
        factor_dict = {
            "variables": variables,
            "distribution": "categorical_conditional"
            if len(list(values.shape)) > 1
            else "categorical",
            "values": values.tolist(),
        }

        # Add "role" attribute
        if role:
            factor_dict["role"] = role

        # Add factor to JSON model dict
        self.json_model["factors"].append(factor_dict)

    def validate(self, verbose: bool = True):
        """
        Validates that a model is a valid factor graph.

        Parameters:
        verbose (bool): If True, prints a success message upon validation. Defaults to True.
        """

        # POST /validate with dict representation of JSON model
        response = send_http_request(
            agent_url=self.agent_url,
            http_request_method="post",
            call="validate",
            json_data={"vfg": self.json_model},
        )

        assert response.status_code == 200, f"Validation error: {str(response.text)}"

        if verbose:
            self.logger.info("Model validated successfully.")

    def save(self, outpath: str) -> None:
        """
        Export JSON model dict to JSON file at a given path.

        Parameters:
        outpath (str): The path to save the JSON file.
        """

        self.validate(verbose=False)

        with open(outpath, "w") as f:
            # iof = io.TextIOWrapper(f.buffer)
            json.dump(
                self.json_model, io.TextIOWrapper(f.buffer), indent=5, sort_keys=False
            )

        self.logger.info(f"JSON representation of model exported to: {outpath}")

    def visualize(
        self, factor_color: str = "lightgreen", variable_color: str = "lightcoral"
    ) -> None:
        """
        Visualize the JSON model dict.

        Parameters:
        factor_color (str): The color for the factor nodes. Defaults to "lightgreen".
        variable_color (str): The color for the variable nodes. Defaults to "lightcoral".
        """

        self.validate(verbose=False)

        # Gather variable names and the number of variables
        variable_names = list(self.json_model["variables"].keys())
        n_variables = len(variable_names)

        # Try to use the role as the factor name; if it does not exist, then name factor by
        # position in the factor list.
        factor_names = []
        factors = self.json_model["factors"]
        n_factors = len(factors)

        # Collect factor names
        for f in range(n_factors):
            if (
                "role" in factors[f]
            ):  # If the user has input a role, use it as the factor name
                factor_names.append(factors[f]["role"])
            else:  # If the user has not input a role, use the position in the list as the name
                factor_names.append(f"F{f}")

        g = nx.Graph()  # Initialize networkx graph

        # Add factor and variable nodes to networkx graph
        for f in factor_names:
            g.add_node(f)

        for v in variable_names:
            g.add_node(v)

        # Build connection list that shows what factors hook to what nodes
        connection_list = []

        # Loop over factors and use the "variables" attribute to determine connections
        for idx, f in enumerate(self.json_model["factors"]):
            for v in f["variables"]:
                connection_list.append((factor_names[idx], v))

        # Add edges to networkx graph
        g.add_edges_from(connection_list)

        # Draw graph
        color_map = [factor_color] * n_factors + [variable_color] * n_variables
        nx.draw(g, with_labels=True, font_color="black", node_color=color_map)

    def _to_vfg(self, json_model: dict):
        """
        Wrapper for vfg_from_json in pyvfg.

        Parameters:
        json_model (dict): The JSON model dict.

        Returns:
        The VFG object created from the JSON model.
        """
        self.validate(verbose=False)
        return vfg_from_json(json.dumps(json_model))

    def get_variable_values(self, variable_id: str) -> list:
        """
        Wrapper for pyvfg variable elements access.

        Parameters:
        variable_id (str): The ID of the variable.

        Returns:
        list: The values of the variable.
        """
        vfg = self._to_vfg(json_model=self.json_model)
        return vfg.variables[variable_id].elements

    def get_variable_names(self) -> list:
        """
        Wrapper for pyvfg variable keys access.

        Returns:
        list: The names of the variables.
        """
        vfg = self._to_vfg(json_model=self.json_model)
        return list(vfg.variables.keys())

    def get_factor_attributes(self, factor_id: int, attribute: str):
        """
        Wrapper for pyvfg factor attributes access.

        Parameters:
        factor_id (int): The ID of the factor.
        attribute (str): The attribute to retrieve.

        Returns:
        The value of the specified attribute.

        Raises:
        KeyError: If the attribute is not recognized.
        """
        vfg = self._to_vfg(json_model=self.json_model)

        if attribute == "variables":
            return vfg.factors[factor_id].variables
        elif attribute == "distribution":
            return vfg.factors[factor_id].distribution
        elif attribute == "values":
            return vfg.factors[factor_id].values
        elif attribute == "role":
            return vfg.factors[factor_id].role
        else:
            raise KeyError(
                f"Unrecognized attribute {attribute}. Attribute must be one of 'variables', 'distribution', 'values', or 'role'."
            )
