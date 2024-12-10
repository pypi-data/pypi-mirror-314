import http.server
import socketserver
import threading
from socketserver import TCPServer
from genius_client_sdk.configuration import default_agent_config
import os

__PAYLOAD_PATH = "demo/curie-agent/payloads"


def __get_path_to_repo_root() -> str:
    """
    this weird little bit allows tests to run nicely in IDE or CLI/CICD, by finding the root of the repo by way of finding the payloads directory
    """
    # base path, assume we're at root of project
    path_to_payloads = __PAYLOAD_PATH
    _path_depth = 0

    path_to_repo_root = ""
    # if we're in the tests directory, we need to go up a few levels to get to root
    while not (os.path.exists(path_to_payloads)) and _path_depth < 5:
        path_to_repo_root = "../" + path_to_repo_root
        path_to_payloads = path_to_repo_root + __PAYLOAD_PATH
        _path_depth += 1

    # fail fast and clearly if we can't find the path
    if not (os.path.exists(path_to_payloads)):
        raise FileNotFoundError(
            f"Could not find payloads directory that should indicate the root of the repo ({__PAYLOAD_PATH}); CWD: {os.getcwd()}"
        )
    return path_to_repo_root


# this is the path to the root of the repo
PATH_TO_REPO_ROOT = __get_path_to_repo_root()

# this is the path to the payloads directory in the repo
PATH_TO_PAYLOADS = PATH_TO_REPO_ROOT + __PAYLOAD_PATH

# this is the path to the payload used for learning in the sprinkler example
PATH_TO_SPRINKLER_LEARNING_PAYLOAD = (
    f"{PATH_TO_PAYLOADS}/learn/sprinkler__observation_pgmpy__simple.json"
)

# this is the path to the payload containing the VFG in the sprinkler example (for interacting directly with agent)
PATH_TO_SPRINKLER_VFG = f"{PATH_TO_PAYLOADS}/factor_graphs/sprinkler_vfg_0_3_0.json"

# this is the path to the raw inner payload containing the VFG in the sprinkler example (for interacting with pyvfg)
PATH_TO_SPRINKLER_NOWRAPPER_VFG = (
    f"{PATH_TO_PAYLOADS}/factor_graphs/sprinkler_vfg_0_3_0_no_wrapper.json"
)


def __start_simple_http_server(handler):
    """
    Internal method to start a simple HTTP server with the given handler
    """

    class __ReusableTCPServer(socketserver.TCPServer):
        """
        Simple TCP server that allows the address to be reused
        """

        allow_reuse_address = True

    httpd = __ReusableTCPServer(
        (default_agent_config.agent_hostname, default_agent_config.agent_port), handler
    )

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return httpd


def start_simple_http_server_always_returns_200() -> TCPServer:
    """
    Start a simple HTTP server that always returns 200 OK
    """

    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        allow_reuse_address = True

        def handle(self):
            # This method will be called for each request
            self.request.recv(1024).strip()
            # You can parse the data here to determine if it's GET, POST, or PUT
            # For simplicity, we'll just send 'OK' for all requests
            self.request.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")

    # Start a simple HTTP server in a separate thread
    handler = CustomHTTPRequestHandler

    return __start_simple_http_server(handler)


def start_simple_http_server_always_returns_400() -> TCPServer:
    """
    Start a simple HTTP server that always returns 400 Error
    """

    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        allow_reuse_address = True

        def handle(self):
            # This method will be called for each request
            self.request.recv(1024).strip()
            # You can parse the data here to determine if it's GET, POST, or PUT
            # For simplicity, we'll just send 'OK' for all requests
            self.request.sendall(
                b"HTTP/1.1 400 Error\r\nContent-Length: 5\r\n\r\nError"
            )

    # Start a simple HTTP server in a separate thread
    handler = CustomHTTPRequestHandler

    return __start_simple_http_server(handler)
