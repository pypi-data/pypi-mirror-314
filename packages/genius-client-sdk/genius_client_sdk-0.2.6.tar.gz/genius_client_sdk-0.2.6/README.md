# Genius client side SDK

Python library which provides access to the Genius API. For a full tour of functionality see `demos/client-sdk/00_sdk_demo.ipynb`.

# Configuration

- Copy .env.template to .env
- Set the following variables if running a remote agent:

AGENT_HTTP_PROTOCOL={your protocol (http or https)} - defaults to http
AGENT_HOSTNAME={your agent hostname} - defaults to localhost
AGENT_PORT={your port, use 443 if https} - defaults to 3000

# Features

## Build a factor graph from scratch

The `GeniusModel` class is used to build factor graphs from scratch. The class has the following capabilities:
- Create a model from a JSON file path
- Construct model by adding variables or factors
- Validate a constructed model with `POST /validate` in the fastAPI
- Save (export) a model to JSON
- Visualize the model with networkx
- Get variable names and values for a given model
- Get factor attributes for a given model

## Build a POMDP model from scratch

Creates a POMDP style factor graph model. This class is really just a wrapper around the `GeniusModel` class with constrained functionality to enable the user to create a POMDP model. Strictly speaking, one can create it with the GeniusModel class but the convenience functions in this class make the process easier and include checks to make sure all the necessary model components are present.

## Query a model with Genius

The `GeniusAgent` class is used as a wrapper around fastAPI to communicate to and from a running Genius agent. This class has the following capabilities enabled by the API calls:
- `POST /graph` of genius model loaded from a JSON or from the `GeniusModel` class
- `GET /graph` of genius model and print/view its contents
- `POST /infer` to perform inference given some evidence and a variable of interest
- `POST /learn` to perform parameter learning given an input CSV or list of variables and their observations
- `POST /actionselection` to perform action selection given a POMDP model structure and observation vector
    
At the moment, it is assumed that the user connects to a local `GeniusAgent` as specified in the `.env` file. In the future, initializing this class will have options to specify a URL and port.

# Remaining work

- TODO: VFG wrapping

- TODO: Add todos from PR
- TODO: Fix remaining todos in code
- TODO: SDK Gridworld full demo
- TODO: SDK MAB full demo
- TODO: Add structure learning
- TODO: Connecting to a Genius agent (GPAI-148)
- TODO: Unit tests and production quality (GPAI-149)
- TODO: (maybe) reevaluate the way genius_client_sdk is built and used in the notebooks once we work with this a little bit more