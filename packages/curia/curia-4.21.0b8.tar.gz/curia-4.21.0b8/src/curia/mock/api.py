import dataclasses
import datetime
import functools
import inspect
import warnings
from collections import defaultdict
from types import MethodType
from typing import List, Dict, Callable, Tuple, Union
from unittest.mock import MagicMock

from curia.api.swagger_client import PlatformApi, Dataset
import curia.api.swagger_client.models as models_package
import re
from pymaybe import maybe
import uuid
from inspect import getframeinfo, stack

from curia.mock.server import Exception404
# pylint: disable=W0622,W0613
from curia.utils.string import to_snake_case, to_camel_case


def debug(message):
    caller = getframeinfo(stack()[1][0])
    print(f"[MockApi DEBUG: {caller.filename}:{caller.lineno}]: {message}")


def has_many_or_one_to_one_relationship(key, type_a, type_b):
    return f"{key}_id" in type_a.attribute_map and "id" in type_b.attribute_map


def resolve_one_to_many_relationship(key, type_a, type_b):
    type_a_camel_case = type_a.__name__
    return_candidates = []
    for attribute_name, attribute_type in type_b.swagger_types.items():
        if attribute_type == type_a_camel_case:
            return_candidates.append(attribute_name)
    if len(return_candidates) == 0:
        return False
    if len(return_candidates) > 1:
        raise ValueError(f"Multiple possible relationships found between {type_a} and {type_b}: {return_candidates}")
    if f"{return_candidates[0]}_id" in type_b.attribute_map:
        return f"{return_candidates[0]}_id"
    return False


def has_many_to_many_relationship(key, type_a, type_b):
    type_a_camel_case = type_a.__name__
    return_candidates = []
    for attribute_name, attribute_type in type_b.swagger_types.items():
        if attribute_type == f"list[{type_a_camel_case}]":
            return_candidates.append(attribute_name)
    if len(return_candidates) == 0:
        return False
    if len(return_candidates) > 1:
        raise ValueError(f"Multiple possible relationships found between {type_a} and {type_b}: {return_candidates}")
    return True


class _MockApiInstanceBase:
    def __init__(self):
        seed_data, method_overrides, executables_configuration = MockApiConfiguration.get_configuration()
        self.db = defaultdict(dict)
        self.many_to_many_joins = defaultdict(lambda: defaultdict(list))
        self._load_seed_data(seed_data)
        self.method_overrides = method_overrides
        self.executables_configuration = executables_configuration
        self.currently_executing = {}

    def _load_seed_data(self, seed_data):
        """
        Loads a list of seed models into the database

        :param seed_data: List of API models to load
        """
        for model in seed_data:
            self._load_model(model)

    def _get_executable_configuration(self, model_type: type):
        for executable_configuration in self.executables_configuration:
            if executable_configuration.executable_class_name == model_type.__name__:
                return executable_configuration
        return None

    def _is_executable(self, model_type: type):
        return self._get_executable_configuration(model_type) is not None

    def _start_mock_execution(self, id_, model_type):
        executable_configuration = self._get_executable_configuration(model_type)
        self.db[model_type][id_].status = executable_configuration.run_status
        self.currently_executing[(model_type, id_)] = datetime.datetime.now()

    def _update_mock_execution_status(self, id_, model_type):
        executable_configuration = self._get_executable_configuration(model_type)
        if (model_type, id_) not in self.currently_executing:
            return
        current_time = datetime.datetime.now()
        start_time = self.currently_executing[(model_type, id_)]
        elapsed_time = current_time - start_time
        if elapsed_time.total_seconds() > executable_configuration.time_to_finish:
            self.currently_executing.pop((model_type, id_))
            if id_ in executable_configuration.ids_to_fail:
                self.db[model_type][id_].status = executable_configuration.failed_status
            else:
                self.db[model_type][id_].status = executable_configuration.complete_status

    def _stop_mock_execution(self, id_, model_type):
        executable_configuration = self._get_executable_configuration(model_type)
        if (model_type, id_) not in self.currently_executing:
            return

        self.currently_executing.pop((model_type, id_))
        self.db[model_type][id_].status = executable_configuration.aborted_status

    def _load_model(self, model):
        self.db[type(model)][model.id] = model
        model_snake_case = to_snake_case(type(model).__name__)
        for key in model.attribute_map.keys():
            value = getattr(model, key)

            if type(value) in MODEL_MAP.values() and has_many_or_one_to_one_relationship(key, type(model), type(value)):
                self._load_single_submodel(key, model, model_snake_case, value)
            if isinstance(value, list) and len(value) > 0 \
                    and hasattr(value[0], 'attribute_map'):
                self._load_multiple_submodels(key, model, model_snake_case, value)

    def _load_multiple_submodels(self, key: str, model, model_snake_case: str, value):
        if resolve_one_to_many_relationship(key, type(model), type(value[0])):
            # joined model case, one to many
            for joined_model in value:
                setattr(joined_model, f"{model_snake_case}_id", model.id)
        elif has_many_to_many_relationship(key, type(model), type(value[0])):
            # joined model case, many to many
            for joined_model in value:
                self.many_to_many_joins[(type(model), type(joined_model))][model.id].append(joined_model.id)
                self.many_to_many_joins[(type(joined_model), type(model))][joined_model.id].append(model.id)
        for joined_model in value:
            if joined_model.id not in self.db[type(joined_model)]:
                self._load_model(joined_model)

    def _load_single_submodel(self, key: str, model, model_snake_case: str, value):
        # joined model case
        setattr(model, f"{key}_id", value.id)
        if model_snake_case in value.attribute_map:
            setattr(value, model_snake_case, model)
        elif f"{model_snake_case}s" in value.attribute_map:
            if isinstance(getattr(value, f"{model_snake_case}s"), list):
                getattr(value, f"{model_snake_case}s").append(model)
            else:
                setattr(value, f"{model_snake_case}s", [model])
        if value.id not in self.db[type(value)]:
            # avoid infinite recursion
            self._load_model(value)

    def __getattribute__(self, name):
        try:
            method_overrides = object.__getattribute__(self, "method_overrides")
        except AttributeError:
            # handle case where object is still not fully initialized
            method_overrides = {}
        if name in method_overrides:
            return MethodType(method_overrides[name], self)
        return object.__getattribute__(self, name)

    def resolve_joins(self, models, joins: List[str]):
        if len(models) == 0:
            # no models to join other models to
            return
        for join in joins:
            self.resolve_join(join, models)

    def resolve_join(self, join, models):
        current_models = models
        current_model_type = type(current_models[0])
        segmentation = join.split(".")
        for segment in segmentation:
            inverted_attribute_map = {value: key for key, value in current_model_type.attribute_map.items()}

            if segment not in inverted_attribute_map:
                raise AttributeError(f"Cannot resolve join: {join}, {current_model_type} does not have an "
                                     f"attribute corresponding to {segment} (looking for '{segment}')")
            attribute_name = inverted_attribute_map[segment]
            attribute_swagger_type: str = current_model_type.swagger_types[attribute_name]
            if attribute_swagger_type.startswith("list["):
                next_model_type, next_models = self.resolve_join_segment_list(attribute_name, attribute_swagger_type,
                                                                              current_model_type, current_models, join)

            else:
                next_model_type, next_models = self.resolve_join_segment_direct(
                    attribute_name,
                    attribute_swagger_type,
                    current_models
                )
            current_models = next_models
            current_model_type = next_model_type

    def resolve_join_segment_list(self,
                                  attribute_name: str,
                                  attribute_swagger_type: str,
                                  current_model_type: type,
                                  current_models: list,
                                  join):
        attribute_swagger_type = attribute_swagger_type[len("list["):-1]
        next_model_type = MODEL_MAP[attribute_swagger_type]
        next_models = []
        if id_attr := resolve_one_to_many_relationship(attribute_name, current_model_type, next_model_type):
            # many to one case
            for individual_model in current_models:
                associated_models = [
                    value for value in self.db[next_model_type].values()
                    if getattr(value, id_attr) == individual_model.id
                ]
                setattr(individual_model, attribute_name, associated_models)
                next_models.extend(associated_models)
        elif has_many_to_many_relationship(attribute_name, current_model_type, next_model_type):
            # many to many case
            for individual_model in current_models:
                associated_models = [
                    self.db[next_model_type][id_]
                    for id_ in
                    self.many_to_many_joins[(current_model_type, next_model_type)][individual_model.id]
                ]
                setattr(individual_model, attribute_name, associated_models)
                next_models.extend(associated_models)
        else:
            raise ValueError(f"Cannot resolve join: {join}, could not resolve relationship between "
                             f"{current_model_type} and type {next_model_type}.")
        return next_model_type, next_models

    def resolve_join_segment_direct(self, attribute_name: str, attribute_swagger_type: str, current_models: list):
        next_model_type = MODEL_MAP[attribute_swagger_type]
        next_models = []
        for individual_model in current_models:
            next_model_id = getattr(individual_model, f"{attribute_name}_id")
            if next_model_id is None:
                raise ValueError(f"{attribute_name}_id value on {current_models} is null!")
            # get next model and set attribute of current model
            next_model = self.db[next_model_type][next_model_id]
            setattr(individual_model, attribute_name, next_model)
            next_models.append(next_model)
        return next_model_type, next_models


def configure_mock_api(seed_data: List[object], method_overrides: Dict[str, Callable]):
    mock_api_configuration = MockApiConfiguration(seed_data=seed_data, method_overrides=method_overrides)

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with mock_api_configuration:
                return fn(*args, **kwargs)

        return wrapper

    return decorator


@dataclasses.dataclass
class ExecutableConfiguration:
    executable_class_name: str
    time_to_finish: float = 3.0
    ids_to_fail: List[str] = dataclasses.field(default_factory=list)
    run_status: str = "RUNNING"
    failed_status: str = "FAILED"
    complete_status: str = "COMPLETE"
    aborted_status: str = "ABORTED"


DEFAULT_EXECUTABLES_CONFIGURATION = [
    ExecutableConfiguration(executable_class_name="ModelJob")
]


class MockApiConfiguration:
    STACK: List['MockApiConfiguration'] = []

    def __init__(self,
                 seed_data: List[object],
                 method_overrides: Dict[str, Callable],
                 executables_configuration: List[ExecutableConfiguration] = None):
        """
        Initialize and __enter__ a MockApiConfiguration to seed the mock API with certain values. MockApiConfiguration
        contexts stack -- e.g.:

        with MockApiConfiguration(..., ...):
            with MockApiConfiguration(..., ...):
                api_instance = MockApiInstance()

        Will have the api_instance configured with the seed data from both configurations and the methods from both
        configurations, with the innermost context having precedence.

        :param seed_data: List of API models to seed into the mock database
        :param method_overrides: Dict mapping strings (the names of methods) to callables that implement those methods.
            The callables should expect to receive self as the first argument
        """
        self.seed_data = seed_data
        self.method_overrides = method_overrides
        if executables_configuration is None:
            executables_configuration = DEFAULT_EXECUTABLES_CONFIGURATION
        self.executables_configuration = executables_configuration

    def __enter__(self):
        MockApiConfiguration.STACK.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        MockApiConfiguration.STACK.pop()

    @classmethod
    def get_configuration(cls) -> Tuple[List[object], Dict[str, Callable], List[ExecutableConfiguration]]:
        """
        Retrieves the current seed data and method overrides to instantiate a mock API instance

        :return: seed_data as concatenated seed_datas from all configs in STACK, method_overrides as combined
            dictionary of all method_overrides in STACK, with innermost configs taking precedence
        """
        seed_data = []
        method_overrides = {}
        executables_configuration = []
        for configuration in cls.STACK:
            seed_data.extend(configuration.seed_data)
            method_overrides.update(configuration.method_overrides)
            executables_configuration.extend(configuration.executables_configuration)
        if len(executables_configuration) == 0:
            executables_configuration = DEFAULT_EXECUTABLES_CONFIGURATION
        return seed_data, method_overrides, executables_configuration


def get_models():
    """
    Gets all model classes in autogenerated API by stepping through the package

    :return: List of all model classes in autogenerated API
    """
    return {
        model_name: getattr(models_package, model_name)
        for model_name in dir(models_package)
        if isinstance(getattr(models_package, model_name), type)
    }


MODEL_MAP = get_models()


def fn_get_one(models, model_type):
    """
    Constructs a method for getting a single object from the API mock database for an arbitrary model_type
    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that gets a single model from the API mock database
    """

    def get_one(self, id, **kwargs):
        if id in self.db[model_type]:
            if kwargs.get("join", None) is not None:
                self.resolve_joins([self.db[model_type][id]], kwargs["join"])
            if self._is_executable(model_type):
                self._update_mock_execution_status(id, model_type)
            return self.db[model_type][id]
        raise Exception404("404 Model Not Found")

    return get_one


def fn_get_many(models, model_type):
    """
    Constructs a method for getting many objects from the API mock database for an arbitrary model_type
    See docs to implement more filter functionality:
    https://github.com/nestjsx/crud/wiki/Requests#filter

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that gets several models from the API mock database
    """

    def get_many(self, **kwargs):
        to_return = []
        for model in self.db[model_type].values():
            if kwargs.get("filter", None) is not None:
                filter = kwargs["filter"]
                for f in filter:
                    field, condition, value = f.split("||")
                    field_snake_case = to_snake_case(field)
                    try:
                        model_value = getattr(model, field_snake_case)
                    except AttributeError as e:
                        raise AttributeError(f"Model {model} does not have attribute {field_snake_case}!") from e
                    model_value_type = type(model_value)
                    # attempt to coerce type
                    try:
                        model_value = model_value_type(model_value)
                    except Exception as e:
                        debug(f"Failed to coerce type while processing filters; {e}. ")
                    valid = evaluate_condition(condition, model_value, value)
                    if not valid:
                        break
                else:
                    # for else: https://book.pythontips.com/en/latest/for_-_else.html
                    # only runs if there were no breaks (so no filters were invalid)
                    to_return.append(model)
        if "join" in kwargs:
            self.resolve_joins(to_return, kwargs["join"])
        if self._is_executable(model_type):
            for entity in to_return:
                self._update_mock_execution_status(entity.id, model_type)
        return_type = models[f"GetMany{model_type.__name__}ResponseDto"]
        return return_type(data=to_return, count=len(to_return), total=len(to_return), page=0, page_count=1)

    return get_many


def evaluate_condition(condition, model_value, value):
    if condition == "$eq":
        valid = model_value == value
    elif condition == "$ne":
        valid = model_value != value
    elif condition == "$gt":
        valid = model_value > value
    elif condition == "$lt":
        valid = model_value < value
    elif condition == "$gte":
        valid = model_value >= value
    elif condition == "lte":
        valid = model_value <= value
    elif condition == "starts":
        valid = model_value.startswith(value)
    elif condition == "ends":
        valid = model_value.endswith(value)
    else:
        raise ValueError(f"Condition {condition} not recognized by the mock API. "
                         f"If you need it, implement it. (ask EK for reference as to how to do so)")
    return valid


def convert_model_to_model_cls(model: Union[dict, object], cls):
    """
    Converts a model, potentially as a dict,  to a model class instance. If the model is an object implementing to_dict,
    it will be converted to a dict first and then to the model class.
    """
    if hasattr(model, "to_dict"):
        model = model.to_dict()
    try:
        obj = cls(**model)
    except TypeError as e:
        warnings.warn(f"Failed to convert model {model} to model class {cls}. Error: {e} \n"
                      f"Returning model as a dict instead.")
        return model
    # The object is now a model class instance and has swagger_types, so we can use those to recursively search
    # for nested models and convert them to model class instances
    for attr, attr_type in obj.swagger_types.items():
        if attr_type in MODEL_MAP and getattr(obj, attr) is not None:
            # Recursively convert nested models
            setattr(obj, attr, convert_model_to_model_cls(getattr(obj, attr), MODEL_MAP[attr_type]))
        # handle the case when attr_type represents a list of models
        elif attr_type.startswith("list[") and attr_type[5:-1] in MODEL_MAP and getattr(obj, attr) is not None:
            # Recursively convert nested models
            setattr(
                obj,
                attr,
                [convert_model_to_model_cls(item, MODEL_MAP[attr_type[5:-1]]) for item in getattr(obj, attr)]
            )
    return obj


def fn_create_one(models, model_type):
    """
    Constructs a method for creating one object the API mock database for an arbitrary model_type

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that creates a object in the API mock database
    """

    def create_one(self, body, **kwargs):
        body = convert_model_to_model_cls(body, model_type)
        body.id = str(uuid.uuid4())
        self.db[model_type][body.id] = body
        return body

    return create_one


def fn_create_many(models, model_type):
    """
    Constructs a method for creating many objects in the API mock database for an arbitrary model_type

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that creates many objects in the API mock database
    """

    def create_many(self, body, **kwargs):
        if hasattr(body, "bulk"):
            bulk = body.bulk
        else:
            bulk = body["bulk"]
        models = []
        for model in bulk:
            model = convert_model_to_model_cls(model, model_type)
            model.id = str(uuid.uuid4())
            self.db[model_type][model.id] = model
            models.append(model)
        return models

    return create_many


def fn_update_one(models, model_type):
    """
    Constructs a method for updating one object in the API mock database for an arbitrary model_type

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that updates one object in the API mock database
    """

    def update_one(self, id, body, **kwargs):
        if hasattr(body, "to_dict"):
            body = body.to_dict()
        if id not in self.db[model_type]:
            raise Exception404("404 Model Not Found")
        result = self.db[model_type][id]
        for field, value in body.items():
            setattr(result, field, value)
        if self._is_executable(model_type):
            self._update_mock_execution_status(id, model_type)
        return result

    return update_one


def fn_delete_one(models, model_type):
    """
    Constructs a method for deleting one object in the API mock database for an arbitrary model_type

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that deletes one object in the API mock database
    """

    def delete_one(self, id, **kwargs):
        if id not in self.db[model_type]:
            raise Exception404("404 Model Not Found")
        del self.db[model_type][id]
        return {"id": id, "deleted": True}

    return delete_one


def fn_replace_one(models, model_type):
    """
    Constructs a method for replacing one object in the API mock database for an arbitrary model_type

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that replaces one object in the API mock database
    """

    def replace_one(self, body, **kwargs):
        body = convert_model_to_model_cls(body, model_type)
        self.db[model_type][body.id] = body
        if self._is_executable(model_type):
            self._update_mock_execution_status(id, model_type)
        return body

    return replace_one


def fn_start(models, model_type):
    """
    Constructs a method for "starting" one object in the API mock database for an arbitrary model_type. No code
    is actually executed when the object is started, the status is just changed.

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that starts one object in the API mock database
    """

    def start(self: _MockApiInstanceBase, id, **kwargs):
        if id not in self.db[model_type]:
            raise Exception404("404 Model Not Found")
        if not self._is_executable(model_type):
            raise ValueError("This model type is not executable by default. "
                             f"Please add an ExecutableConfiguration for it ({model_type.__name__}) to the mock API "
                             "instance configuration.")
        self._start_mock_execution(id, model_type)
        return self.db[model_type][id]

    return start


def fn_stop(models, model_type):
    """
    Constructs a method for "stopping" one object in the API mock database for an arbitrary model_type. No code
    is actually executed when the object is stopped, the status is just changed.

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that stops one object in the API mock database
    """

    def stop(self, id, **kwargs):
        if id not in self.db[model_type]:
            raise Exception404("404 Model Not Found")
        if not self._is_executable(model_type):
            raise ValueError("This model type is not executable by default. "
                             f"Please add an ExecutableConfiguration for it ({model_type.__name__}) to the mock API "
                             "instance configuration.")
        self._stop_mock_execution(id, model_type)
        return self.db[model_type][id]

    return stop


def fn_status(models, model_type):
    """
    Constructs a method for getting the status of one object in the API mock database for an arbitrary model_type.

    :param models: Dict mapping api model names to api model classes
    :param model_type: api model class, e.g. ProcessJob
    :return: Method that gets the status of one object in the API mock database
    """

    def status(self, id, **kwargs):
        if id in self.db[model_type]:
            if id not in self.db[model_type]:
                raise Exception404("404 Model Not Found")
            if self._is_executable(model_type):
                self._update_mock_execution_status(id, model_type)
            return self.db[model_type][id]
        raise Exception404("404 Model Not Found")

    return status


def upload_dataset(self, body, **kwargs):
    # TODO: if more advanced mocking functionality is needed for this endpoint, it can be added here
    test_body = Dataset(
        name="Mocked Dataset",
        type="query",
        description="Mocked Dataset",
        organization_id="mocked_organization_id",
    )
    test_body.id = str(uuid.uuid4())
    self.db[Dataset][test_body.id] = test_body
    return test_body


def default_functionality_builder(method, models):
    """
    Tries to parse the return type of a method from its docstring and creates a method that returns a MagicMock
    of that return type

    :param method: Method to mock
    :param models: List of models
    :return: function that mocks the default functionality of a model
    """
    return_line = [line.strip() for line in maybe(method.__doc__).split("\n").or_else("") if ":return:" in line]
    return_type = maybe(return_line or None).split()[1].or_else(None)

    if return_type is not None and return_type in models:
        @functools.wraps(method)
        def function(self, *args, **kwargs):
            return MagicMock(models[return_type])
    else:
        if return_type is not None:
            debug(f"{return_type} of method {method} is not a model; reverting to default MagicMock")

        @functools.wraps(method)
        def function(self, *args, **kwargs):
            return MagicMock()
    return function


# matches model names to functionality builders
regex_to_functionality_builder = {
    r"get_one_base_([a-z_]*)_controller_\1": fn_get_one,
    r"get_many_base_([a-z_]*)_controller_\1": fn_get_many,
    r"create_one_base_([a-z_]*)_controller_\1": fn_create_one,
    r"create_many_base_([a-z_]*)_controller_\1": fn_create_many,
    r"update_one_base_([a-z_]*)_controller_\1": fn_update_one,
    r"delete_one_base_([a-z_]*)_controller_\1": fn_delete_one,
    r"replace_one_base_([a-z_]*)_controller_\1": fn_replace_one,
    r"([a-z_]*)_controller_start": fn_start,
    r"([a-z_]*)_controller_stop": fn_stop,
    r"([a-z_]*)_controller_status": fn_status,
    r"dataset_controller_upload": upload_dataset,
}


def get_functionality(models, method_name, method):
    """
    Parses a method name and builds the appropriate functionality around it, e.g. methods that look like
    create_one_base_{}_controller_{} will actually create a {} in the mock database

    :param models: List of parsed models
    :param method_name: Name of method to implement
    :param method: Actual method to implement
    :return: boolean representing whether functionality was parsed and created, Method mocking functionality
    """
    for pattern, functionality_builder in regex_to_functionality_builder.items():
        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.fullmatch(method_name)
        if match:
            if len(match.groups()) == 0:
                # if there are no groups, this method is hardcoded for a specific model
                # e.g. dataset_controller_upload
                return True, functionality_builder
            model_type_snake_case = match.group(1)
            model_type_camel_case = to_camel_case(model_type_snake_case)
            if model_type_camel_case not in models:
                debug(f"Could not find model for method {method_name}! "
                      f"(parsed snake case: {model_type_snake_case})"
                      f"(parsed camel case: {model_type_camel_case})")
                break
            return True, functionality_builder(models, models[model_type_camel_case])
    return False, default_functionality_builder(method, models)


def build_method_dict():
    """
    Builds a dictionary of methods on the API and mocked functionality for each method
    :return: Dictionary of methods that can be used to mock the API
    """
    method_dict = {}
    debug(f"Found {len(MODEL_MAP.keys())} models")
    n_specialized = 0
    for method_name, method in inspect.getmembers(PlatformApi, predicate=inspect.isfunction):
        if method_name.startswith("__"):
            continue
        specialized, new_method_functionality = get_functionality(MODEL_MAP, method_name, method)
        method_dict[method_name] = new_method_functionality
        if specialized:
            n_specialized += 1

    debug(f"Found {len(method_dict.keys())} methods, {n_specialized} of which have autogenerated functionality.")
    return method_dict


def get_mock_api_instance_class():
    """
    Builds the mock api instance class by reading the actual api instance
    :return: MockApiInstance class
    """
    method_dict = build_method_dict()

    return type("MockApiInstance", (_MockApiInstanceBase,), method_dict)


MockApiInstance = get_mock_api_instance_class()
