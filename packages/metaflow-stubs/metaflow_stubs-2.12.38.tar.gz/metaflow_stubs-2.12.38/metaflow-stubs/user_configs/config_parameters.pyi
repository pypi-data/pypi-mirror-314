######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.38                                                                                #
# Generated on 2024-12-08T03:54:57.909247                                                            #
######################################################################################################

from __future__ import annotations

import collections
import typing
import abc
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.parameters
    import metaflow.user_configs.config_parameters
    import collections.abc
    import typing
    import abc

from ..exception import MetaflowException as MetaflowException
from ..parameters import Parameter as Parameter
from ..parameters import ParameterContext as ParameterContext

TYPE_CHECKING: bool

CONFIG_FILE: str

UNPACK_KEY: str

def dump_config_values(flow: "FlowSpec"):
    ...

class ConfigValue(collections.abc.Mapping, metaclass=abc.ABCMeta):
    """
    ConfigValue is a thin wrapper around an arbitrarily nested dictionary-like
    configuration object. It allows you to access elements of this nested structure
    using either a "." notation or a [] notation. As an example, if your configuration
    object is:
    {"foo": {"bar": 42}}
    you can access the value 42 using either config["foo"]["bar"] or config.foo.bar.
    
    All "keys"" need to be valid Python identifiers
    """
    def __init__(self, data: typing.Dict[str, typing.Any]):
        ...
    def __getattr__(self, key: str) -> typing.Any:
        """
        Access an element of this configuration
        
        Parameters
        ----------
        key : str
            Element to access
        
        Returns
        -------
        Any
            Element of the configuration
        """
        ...
    def __setattr__(self, name: str, value: typing.Any):
        ...
    def __getitem__(self, key: typing.Any) -> typing.Any:
        """
        Access an element of this configuration
        
        Parameters
        ----------
        key : Any
            Element to access
        
        Returns
        -------
        Any
            Element of the configuration
        """
        ...
    def __len__(self):
        ...
    def __iter__(self):
        ...
    def __repr__(self):
        ...
    def __str__(self):
        ...
    def to_dict(self) -> typing.Dict[typing.Any, typing.Any]:
        """
        Returns a dictionary representation of this configuration object.
        
        Returns
        -------
        Dict[Any, Any]
            Dictionary equivalent of this configuration object.
        """
        ...
    ...

class DelayEvaluator(collections.abc.Mapping, metaclass=abc.ABCMeta):
    """
    Small wrapper that allows the evaluation of a Config() value in a delayed manner.
    This is used when we want to use config.* values in decorators for example.
    
    It also allows the following "delayed" access on an obj that is a DelayEvaluation
      - obj.x.y.z (ie: accessing members of DelayEvaluator; accesses will be delayed until
        the DelayEvaluator is evaluated)
      - **obj (ie: unpacking the DelayEvaluator as a dictionary). Note that this requires
        special handling in whatever this is being unpacked into, specifically the handling
        of _unpacked_delayed_*
    """
    def __init__(self, ex: str):
        ...
    def __iter__(self):
        ...
    def __getitem__(self, key):
        ...
    def __len__(self):
        ...
    def __getattr__(self, name):
        ...
    def __call__(self, ctx = None, deploy_time = False):
        ...
    ...

def config_expr(expr: str) -> DelayEvaluator:
    """
    Function to allow you to use an expression involving a config parameter in
    places where it may not be directory accessible or if you want a more complicated
    expression than just a single variable.
    
    You can use it as follows:
      - When the config is not directly accessible:
    
            @project(name=config_expr("config").project.name)
            class MyFlow(FlowSpec):
                config = Config("config")
                ...
      - When you want a more complex expression:
            class MyFlow(FlowSpec):
                config = Config("config")
    
                @environment(vars={"foo": config_expr("config.bar.baz.lower()")})
                @step
                def start(self):
                    ...
    
    Parameters
    ----------
    expr : str
        Expression using the config values.
    """
    ...

class Config(metaflow.parameters.Parameter, collections.abc.Mapping, metaclass=abc.ABCMeta):
    """
    Includes a configuration for this flow.
    
    `Config` is a special type of `Parameter` but differs in a few key areas:
      - it is immutable and determined at deploy time (or prior to running if not deploying
        to a scheduler)
      - as such, it can be used anywhere in your code including in Metaflow decorators
    
    The value of the configuration is determines as follows:
      - use the user-provided file path or value. It is an error to provide both
      - if none are present:
        - if a default file path (default) is provided, attempt to read this file
            - if the file is present, use that value. Note that the file will be used
              even if it has an invalid syntax
            - if the file is not present, and a default value is present, use that
      - if still None and is required, this is an error.
    
    Parameters
    ----------
    name : str
        User-visible configuration name.
    default : Union[str, Callable[[ParameterContext], str], optional, default None
        Default path from where to read this configuration. A function implies that the
        value will be computed using that function.
        You can only specify default or default_value.
    default_value : Union[str, Dict[str, Any], Callable[[ParameterContext, Union[str, Dict[str, Any]]], Any], optional, default None
        Default value for the parameter. A function
        implies that the value will be computed using that function.
        You can only specify default or default_value.
    help : str, optional, default None
        Help text to show in `run --help`.
    required : bool, optional, default None
        Require that the user specified a value for the configuration. Note that if
        a default is provided, the required flag is ignored. A value of None is
        equivalent to False.
    parser : Union[str, Callable[[str], Dict[Any, Any]]], optional, default None
        If a callable, it is a function that can parse the configuration string
        into an arbitrarily nested dictionary. If a string, the string should refer to
        a function (like "my_parser_package.my_parser.my_parser_function") which should
        be able to parse the configuration string into an arbitrarily nested dictionary.
        If the name starts with a ".", it is assumed to be relative to "metaflow".
    show_default : bool, default True
        If True, show the default value in the help text.
    """
    def __init__(self, name: str, default: typing.Union[str, typing.Callable[[metaflow.parameters.ParameterContext], str], None] = None, default_value: typing.Union[str, typing.Dict[str, typing.Any], typing.Callable[[metaflow.parameters.ParameterContext], typing.Union[str, typing.Dict[str, typing.Any]]], None] = None, help: typing.Optional[str] = None, required: typing.Optional[bool] = None, parser: typing.Union[str, typing.Callable[[str], typing.Dict[typing.Any, typing.Any]], None] = None, **kwargs: typing.Dict[str, str]):
        ...
    def load_parameter(self, v):
        ...
    def __getattr__(self, name):
        ...
    def __iter__(self):
        ...
    def __len__(self):
        ...
    def __getitem__(self, key):
        ...
    ...

def resolve_delayed_evaluator(v: typing.Any) -> typing.Any:
    ...

def unpack_delayed_evaluator(to_unpack: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    ...

