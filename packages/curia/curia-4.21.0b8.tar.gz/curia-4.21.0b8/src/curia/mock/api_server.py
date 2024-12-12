import functools
import inspect
from typing import Tuple, List, Dict, Callable, Union, Any
from unittest.mock import MagicMock

from curia.api.swagger_client import PlatformApi, ApiClient
from curia.mock.api import build_method_dict, MockApiConfiguration, MockApiInstance
from curia.mock.server import ParseAndExtractDataSummary, Exception404, using_test_server
from curia.utils.string import to_snake_case


def build_mock_arguments(method: callable) -> Dict[str, Any]:
    """
    Builds a dictionary of mock arguments for a method, using the "inspect" module to parse the method signature
    There is no guarantee that this will work for all methods, but it should work for the ones we use in the
    PlatformApi

    :param method: Method to build mock arguments for
    :return: Dictionary of mock arguments. If the method has a default value for an argument, the default value is used.
    Otherwise, a MagicMock is used.
    """
    mock_arguments = {}
    for arg_name, arg in inspect.signature(method).parameters.items():
        if arg_name == "self":
            continue
        if arg.kind == inspect.Parameter.VAR_KEYWORD:
            continue
        if arg.kind == inspect.Parameter.VAR_POSITIONAL:
            continue
        if arg.default is not inspect.Parameter.empty:
            mock_arguments[arg_name] = arg.default
        else:
            mock_arguments[arg_name] = MagicMock()
    return mock_arguments


def match_call_pattern_to_method_name(
        call_pattern: Tuple[str, str],
        call_pattern_to_method_name: Dict[Tuple, str]) \
        -> Tuple[str, dict]:
    """
    Matches a URL call pattern to a method name, e.g. (/models/some-id-here, GET) -> get_one_base_model_controller_model
    :param call_pattern: Realized call pattern to match, e.g. (/models/some-id-here, GET)
    :param call_pattern_to_method_name: Dictionary of unrealized call patterns (e.g. /models/{id}) to method names
    :return: Method name that matches the call pattern
    """
    url, call_request_method = call_pattern
    call_pattern_components = url.split("/")[1:]  # remove leading slash
    for pattern, method_name in call_pattern_to_method_name.items():
        url_pattern, request_method = pattern
        if request_method != call_request_method:
            continue
        url_pattern_components = url_pattern.split("/")[1:]  # remove leading slash
        if len(url_pattern_components) != len(call_pattern_components):
            continue
        kwargs = {}
        for pattern_component, call_pattern_component in zip(url_pattern_components, call_pattern_components):
            if pattern_component.startswith("{") and pattern_component.endswith("}"):
                kwargs[pattern_component[1:-1]] = call_pattern_component
                continue
            if pattern_component != call_pattern_component:
                break
        else:
            return method_name, kwargs
    raise ValueError(f"Could not match call pattern {call_pattern} to any method!")


class Struct:
    """
    A simple class that allows for attribute access to a dictionary
    """

    def __init__(self, **entries):
        self._entries = entries

    def to_dict(self) -> dict:
        return self._entries

    def __setattr__(self, key, value) -> None:
        if key != "_entries":
            self._entries[key] = value
        super().__setattr__(key, value)

    def __getattr__(self, item) -> Any:
        if item == "_entries":
            return super().__getattribute__(item)
        if item in self._entries:
            return self._entries[item]
        return super().__getattribute__(item)

    def __repr__(self) -> str:
        return str(self._entries)


class MockResponseMapper:
    """
    Builds a function capable of handling responses from the mock server in mock.server.py by hijacking
    the actual api instance and checking which requests are made to the server.
    """
    _mock_response_mapper = None

    def __init__(self):
        hijacked_api_instance = self.get_api_client_hijacker()

        self.method_dict = build_method_dict()

        self.call_pattern_to_method_name = build_call_pattern_dict(hijacked_api_instance, self.method_dict)
        self.mock_api_instance = MockApiInstance()

    def get_api_client_hijacker(self) -> PlatformApi:
        """
        Returns an instance of the api client that has been hijacked to record the last call made to the server
        :return: Hijacked api instance with a hijacked api client
        """
        hijacked_api_instance = PlatformApi()

        class ApiClientHijacker(ApiClient):
            """
            Hijacks the api client to record the last call made to the server
            """

            def __init__(self):
                self.last_call = None
                super().__init__()

            def call_api(self,
                         resource_path, method,
                         path_params=None, query_params=None, header_params=None,
                         body=None, post_params=None, files=None,
                         response_type=None, auth_settings=None, async_req=None,
                         _return_http_data_only=None, collection_formats=None,
                         _preload_content=True, _request_timeout=None) -> (object, int):
                self.last_call = (resource_path, method)
                return None, 200

        hijacked_api_instance.api_client = ApiClientHijacker()
        return hijacked_api_instance

    def response_map(self, request: ParseAndExtractDataSummary) -> Union[dict, list]:
        """
        Performs the actual mapping of the request to a response. This is the function that is called by the mock server
        to determine the response to a request. We first match the request to a method name, then we call the method
        on the mock api instance and return the result, which is then serialized to JSON and returned to the client.

        The request's body is prepped to be passed to the mock api instance by converting it to an object with
        attributes named using snake case. This is done because the mock api instance expects the request body to be
        an object with attributes named using snake case, but the client sends the request body as a dictionary with
        attributes named using lower camel case.

        The result of the mock api instance method is also prepped to be returned to the client by converting it to a
        dictionary with attributes named using lower camel case. This is done because the client expects the response
        body to be JSON with attributes named using lower camel case, but the mock api instance returns the response
        body as an object with attributes named using snake case.

        :param request: The request to map to a response
        """
        try:
            method_name, kwargs = match_call_pattern_to_method_name(
                (request.path, request.method),
                self.call_pattern_to_method_name
            )
        except ValueError as e:
            raise Exception404(f"Could not match call pattern {request.method} {request.path} to any method!") from e
        if not hasattr(self.mock_api_instance, method_name):
            raise Exception(f"Method {method_name} not found in mock api instance!")
        body_dict = {}
        if request.content_qs:
            if "bulk" in request.content_qs:
                body_dict = {
                    "body": {
                        "bulk": prep_for_obj(request.content_qs["bulk"])
                    }
                }
            else:
                body_dict = {"body": prep_for_obj(request.content_qs)}
        res = getattr(self.mock_api_instance, method_name)(
            **kwargs,
            **request.url_qs,
            **body_dict
        )
        return prep_for_json(res)

    @classmethod
    def get(cls) -> "MockResponseMapper":
        """
        Singleton getter

        :return: MockResponseMapper instance. Note that this is a singleton, so the same instance will be returned
        every time. This is necessary because the response_map callable is stateless, but we don't want to set up the
        same mock api instance and call pattern mapping every time we need to use it.
        """
        if cls._mock_response_mapper is None:
            cls._mock_response_mapper = cls()
        return cls._mock_response_mapper


def prep_for_obj(obj: Any) -> Any:
    """
    Prepares a dict for use as an object by converting all keys to snake case. This is necessary because the
    SDK models use snake case, but the actual api uses lower camel case.
    The outputs of this function are used to create SDK models, so they must match the format of the SDK models.

    :param obj: Object to prepare. Can be a dict, list, or a single value (str, int, etc.)
    :return: object prepared for use as an SDK model
    """
    if isinstance(obj, dict):
        return {to_snake_case(key): prep_for_obj(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [prep_for_obj(item) for item in obj]
    return obj


def prep_for_json(obj: Any) -> Any:
    """
    Prepares a model class for json serialization and return to the client by:
    - Converting objects to dicts using their attributes listed in the attribute_map
    - Converting the attribute names according to the attribute_map of the object
    - Recursively applying the above to all values in a dict, list, or sub-object

    This is necessary because the SDK models generally snake case, but the actual api generally uses lower camel case.
    The outputs of this function are returned to the client as json, so they must be in the same format as the actual
    api. We use the attribute_map of the SDK models to convert the attribute names to their API equivalents.

    The objects also have a to_dict method, but this method is overzealous and recursively converts all sub-objects to
    dicts, which is not desirable because then we can't tell how to convert the attribute names of the sub-objects
    as they lose the attribute_map of their class.

    Instead, we rely on this function to eventually convert the sub-objects to dicts, but only when it is safe to do so
    and the attribute names can be converted correctly.

    :param obj: Object to prepare. Can be a dict, list, object with attribute_map, or a single value (str, int, etc.)
    :return: object prepared for json serialization
    """
    if isinstance(obj, list):
        return [prep_for_json(item) for item in obj]
    if isinstance(obj, dict):
        return {key: prep_for_json(value) for key, value in obj.items()}
    if hasattr(obj, "attribute_map"):
        return {
            api_attr_name: prep_for_json(getattr(obj, sdk_attr_name))
            for sdk_attr_name, api_attr_name in obj.attribute_map.items()
        }
    return obj


def mock_api_request_handler_response_map(
        request: ParseAndExtractDataSummary,
        metadata: MockApiConfiguration) -> Union[dict, list]:
    """
    This function is compatible with the response_map parameter of the TestServer class in mock.server.py. When using
    the TestServer class, the metadata parameter should be a MockApiConfiguration instance specifying the initial
    state of the mock api instance which will be utilized by the MockApiInstance class under the hood.
    :param request: The request to handle. Will be automatically passed by the TestServer class.
    :param metadata: The MockApiConfiguration instance specifying the initial state of the MockApiInstance utilized
    under the hood. The value of this parameter will be determined by the response_map_metadata parameter of the
    TestServer class, or by the response_map_metadata parameter of the configure_mock_api_server function.

    :return: The response to return to the client. Should be a dict or list, turnable into json.
    """
    with metadata:
        return MockResponseMapper.get().response_map(request)


def build_call_pattern_dict(hijacked_api_instance: PlatformApi, methods: list) -> Dict[Tuple[str, str], str]:
    """
    Builds a dictionary that maps a call pattern (resource path, method) to a method name in the PlatformApi class
    and thereby to a method in the MockApiInstance class. This is done by hijacking the api client of the PlatformApi
    instance and checking which requests are made to the server when a method is called. The call pattern is then
    mapped to the method name of the method that was called.

    In order to call the methods of the PlatformApi instance, mock arguments are built for each method. These mock
    arguments are built by inspecting the method signature and building mock arguments for each parameter.
    :param hijacked_api_instance: The PlatformApi instance. The api client of this instance should already be hijacked
    with an ApiClientHijacker
    :param methods: A list of method names in the PlatformApi class that should be called in order to build the call
    pattern dictionary. Method names that end with "_with_http_info" are ignored as these methods are not intended to
    be called directly and are not mocked in the MockApiInstance class, so calling them would result in an error.

    :return: A dictionary mapping a call pattern (resource path, method) to a method name in the PlatformApi class
    """
    call_pattern_to_method_name = {}
    for method_name in methods:
        if method_name.endswith("_with_http_info"):
            continue
        method = getattr(hijacked_api_instance, method_name)
        mock_arguments = build_mock_arguments(method)
        method(**mock_arguments)
        if method_name.endswith("_0"):
            # some unusual duplicates exist ending with _0 that gunk up the process if present, so we skip them.
            continue
        call_pattern_to_method_name[hijacked_api_instance.api_client.last_call] = method_name
    return call_pattern_to_method_name


def configure_mock_api_server(seed_data: List[object],
                              method_overrides: Dict[str, Callable],
                              port=3000,
                              log_dir="temp/") -> Callable:
    """
    Decorator for test functions that configures a mock api server for the duration of the test function. The mock
    api server is configured to contain the seed data provided in its database. In a similar manner to MockApiInstance,
    the mock api server can be configured to override the functionality of certain methods by providing a callable
    for the method in the method_overrides dict. The mock api server is configured to run on the port provided and
    to log requests to the log_dir provided.

    Under the hood, this decorator uses the MockApiInstance class to simulate the functionality of the api server.
    So when a method on a client's real sdk is called, the client's sdk will translate the method call into a request
    to the mock api server. The mock api server will then translate the request *back* into its original method call
    and execute the method call on the MockApiInstance instance. The MockApiInstance instance will then execute the
    inferred or supplied method override, if any, and return the result to the mock server, which will then convert
    the result (an object) into the appropriate json response and return it to the client's sdk, which will then
    convert the json response into an object and return it to the client.

    This decorator combines the functionality of the MockApiInstance class and using_test_server decorator.

    The using_test_server decorator can be used to set up an arbitrary mock server for testing purposes. However, it
    requires the user to provide a response_map callable that maps requests to responses. This decorator provides
    a default response_map callable that maps requests to responses based on the seed data and method overrides
    provided, using the MockApiInstance class.

    :param seed_data: List of objects to seed the mock api server with. The objects should be instances of
    the classes in the curia.api.swagger_client.models package.
    :param method_overrides: Dict of method names to override with custom functions. The method names should be
    the same as the method names in the PlatformApi class. The custom functions should take the same arguments as
    the original methods and return the same type as the original methods. The custom functions should not call
    the original methods.
    :param port: Port to run the mock api server on
    :param log_dir: Directory to log requests to
    """
    mock_api_configuration = MockApiConfiguration(seed_data=seed_data, method_overrides=method_overrides)

    def decorator(fn) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            with mock_api_configuration:
                fn_with_test_server = using_test_server(
                    port=port,
                    log_dir=log_dir,
                    response_map=mock_api_request_handler_response_map,
                    response_map_metadata=mock_api_configuration
                )(fn)
                return fn_with_test_server(*args, **kwargs)

        return wrapper

    return decorator
