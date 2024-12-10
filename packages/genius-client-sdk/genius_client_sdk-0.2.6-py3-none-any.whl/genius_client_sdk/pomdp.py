import logging

import numpy as np

from genius_client_sdk.configuration import default_agent_config
from genius_client_sdk.model import GeniusModel
from genius_client_sdk.utils import send_http_request


class POMDPModel(GeniusModel):
    """
    Creates a POMDP style factor graph model. This class is really just a wrapper around the
    GeniusModel class with constrained functionality to enable the user to create a POMDP
    model. Strictly speaking, one can create it with the GeniusModel class but the convenience
    functions in this class make the process easier and include checks to make sure all the
    necessary model components are present.

    A POMDP model requires preset factors (with specific roles) and specific variables. The initial
    state prior is optional. Each time a component is added, the corresponding flags dict is toggled to true.
    """

    def __init__(
        self,
        agent_url: str = default_agent_config.agent_url,
        version=default_agent_config.build_version,
        json_path=None,
    ):
        """
        Initializes the POMDPModel.

        Parameters:
        version (str): The version of the model, default is the build version from Constants.
        json_path (str, optional): The path to the JSON file for the model. Defaults to None.
        """
        super().__init__(agent_url=agent_url, version=version, json_path=json_path)
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

        # Flags are toggled when each model component is added to the model
        self.flags = {
            "likelihood": False,
            "transition": False,
            "preference": False,
            "state": False,
            "observation": False,
            "control": False,
        }

    """ POMDP factors """

    def add_likelihood_factor(
        self, values: np.ndarray, target: str, parents: list[str] = None
    ) -> None:
        """
        Initializes the POMDPModel.

        Parameters:
        version (str): The version of the model, default is the build version from Constants.
        json_path (str, optional): The path to the JSON file for the model. Defaults to None.
        """
        self.add_factor(
            values=values, target=target, parents=parents, role="likelihood"
        )
        self._toggle_flag("likelihood")

    def add_transition_factor(
        self, values: np.ndarray, target: str, parents: list[str] = None
    ) -> None:
        """
        Adds a transition factor to the model.

        Parameters:
        variables (list): The list of variables for the factor.
        values (np.ndarray): The values for the factor.
        """
        self.add_factor(
            values=values, target=target, parents=parents, role="transition"
        )
        self._toggle_flag("transition")

    def add_prior_factor(
        self, values: np.ndarray, target: str, parents: list[str] = None
    ) -> None:
        """
        Adds a prior factor to the model.

        Parameters:
        variables (list): The list of variables for the factor.
        values (np.ndarray): The values for the factor.
        """
        self.add_factor(
            values=values, target=target, parents=parents, role="initial_state_prior"
        )

    def add_preference_factor(
        self, values: np.ndarray, target: str, parents: list[str] = None
    ) -> None:
        """
        Adds a preference factor to the model.

        Parameters:
        variables (list): The list of variables for the factor.
        values (np.ndarray): The values for the factor.
        """
        self.add_factor(
            values=values, target=target, parents=parents, role="preference"
        )
        self._toggle_flag("preference")

    """ POMDP variables """

    def add_state_variable(self, name: str, values: list) -> None:
        """
        Adds a state variable to the model.

        Parameters:
        name (str): The name of the state variable.
        values (list): The values for the state variable.
        """
        self.add_variable(name=name, values=values)
        self._toggle_flag("state")

    def add_observation_variable(self, name: str, values: list) -> None:
        """
        Adds an observation variable to the model.

        Parameters:
        name (str): The name of the observation variable.
        values (list): The values for the observation variable.
        """
        self.add_variable(name=name, values=values)
        self._toggle_flag("observation")

    def add_action_variable(self, name: str, values: list) -> None:
        """
        Adds an action variable to the model.

        Parameters:
        name (str): The name of the action variable.
        values (list): The values for the action variable.
        """
        self.add_variable(name=name, values=values)
        self._toggle_flag("control")

    """ Other methods """

    def _check_flags(self):
        """
        Runs through each flag and determines which are false.

        Raises:
        Exception: If any required components are missing from the POMDP model.
        """
        false_keys = [key for key, value in self.flags.items() if not value]

        if false_keys:
            raise Exception(
                f"The following components are missing from the POMDP model: {false_keys}"
            )

    def _toggle_flag(self, component: str):
        """
        Toggles a flag from false to true.

        Parameters:
        component (str): The component whose flag is to be toggled.
        """
        if not self.flags[component]:
            self.flags[component] = True

    def validate(self, verbose: bool = True):
        """
        Method override for parent class that just adds the _check_flags() statement to ensure all
        model components are present before validation.

        Parameters:
        verbose (bool): If True, prints a success message upon validation. Defaults to True.
        """
        self._check_flags()

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
