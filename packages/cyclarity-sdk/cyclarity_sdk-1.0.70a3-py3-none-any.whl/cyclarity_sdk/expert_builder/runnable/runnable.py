"""
Parsing is a base class used to add arguments to command line and
"""

from enum import Enum  # noqa
import logging
from cyclarity_sdk.platform_api.logger import ClarityLoggerFactory, LogHandlerType
from abc import abstractmethod
from cyclarity_sdk.platform_api import PlatformApi, IPlatformConnectorApi
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
    Generic,
)
from types import TracebackType
from pydantic import (
    BaseModel,
    GetJsonSchemaHandler
)
from pydantic_core import core_schema as cs
from pydantic.json_schema import JsonSchemaValue

# Note the folllowing is an internal pydantic function that apply a temporal fix.
# Original issue can be found in the pydantic repo, issue #7837 - https://github.com/pydantic/pydantic/issues/7837
# Once fixed it could probably be replaced with the regular "from typing import get_args"
from pydantic._internal._generics import get_args


import inspect


class BaseModelExtraAllow(BaseModel):
    class Config:
        """
        Allow extra attributes so that baseclasses can define dynamic instance variables
        Without needing to prepend them with underscore (self._var)
        """

        extra = "allow"

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """
        We want to allow for extra attributes to define dynamic instance variables.
        There's a side effect to that - extra parameters/fields are also accepted during model initialization.
        However, we don't really want this side effect,
        even though this is actually the main reason the 'extra="allow"' configuration exists within pydantic.
        thus, the way we use 'extra="allow"' in somewhat out-of-the-ordinary.
        To account for this side effect, and also to make sure that the UI that is using our shcema
        doesn't allow for extra variables during model initialization,
        we remove the 'additionalProperties' key from the schema.
        """
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.pop('additionalProperties')
        return json_schema


class ParsableModel(BaseModelExtraAllow):
    @property
    def logger(self):
        return self._logger

    @property
    def platform_api(self):
        return self._platform_api

    @classmethod
    def generate_params_schema(cls, *args, **kwargs) -> dict[str, Any]:
        return cls.model_json_schema()

    def model_post_init(self, *args, **kwargs):
        # Default logger will log to screen
        self._logger = ClarityLoggerFactory.get_logger(
            name=self.__class__.__name__,
            level=logging.DEBUG,
            handler_type=LogHandlerType.IN_VEHICLE  # DEV
        )
        self._platform_api: PlatformApi = PlatformApi()  # Default api (CLI) # noqa

    def __repr__(self) -> str:
        return f"{type(self).__name__}({','.join(str(self).split(' '))})"


class ContextParsable(ParsableModel):
    def __enter__(self):
        """Setup phase (python built-in method)
            This is the place to do setup before running if that is needed.
            The implementation of the setup will be implemented in the setup() method.
        Returns:
            Runnable: self to use as the callable during execution
        """
        self.setup()
        return self

    def __call__(self, *args, **kwargs):
        """Executable phase (python built-in method)
            Calling an instance of a Runnable class will excecute the run() method and return the results.
        Returns:
            Results: a result object of the executable
                The results construction should be implemented in the get_results method()
        """
        return self.run(*args, **kwargs)

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:  # noqa
        """Teardown phase (python built-in method)
            This is the place to do teardown if that is needed.
            teardown logic of the Runnable should be implemented in the teardown() method.

        Args:
            exception_type (Optional[Type[BaseException]]): _description_
            exception_value (Optional[BaseException]): _description_
            traceback (Optional[TracebackType]): _description_

        Returns:
            bool: Should return True from __exit__ if you want to suppress an exception raised in the context and False in all other cases.
                The return value from the teardown() method will be reflected.
                In case the teardown() method will not return any value, False will be returned.
        """
        ret_val = self.teardown(exception_type=exception_type,
                                exception_value=exception_value, traceback=traceback)
        if ret_val is None:
            return False
        else:
            return ret_val

    @abstractmethod
    def setup(self):
        """Setup logic to be run before running the runnable.
        """
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """Excecution logic for the runnable.
        """
        pass

    @abstractmethod
    def teardown(self, exception_type=None, exception_value=None, traceback=None):
        """Teardown logic to be run to clean the setup logic.
        """
        pass

    @classmethod
    def mark_unimplemented(cls):
        """Mark a function as not-implemented.
            set a debug log record to indicate methods that were set with default functionality.
            This allows abstruct methods to be set with default functionallity for some types of Runnables.
        """
        cls.logger.debug(
            f'Unimplemented "{inspect.stack()[1].function}" method in {cls.__name__}')


class BaseResultsModel(BaseModelExtraAllow):
    pass


R = TypeVar("R", bound=BaseResultsModel)


class Runnable(ContextParsable, Generic[R]):  # noqa

    def model_post_init(self, *args, **kwargs):
        super().model_post_init(*args, **kwargs)
        self._platform_api = PlatformApi()

    def __call__(self, *args, **kwargs) -> R:
        """Executable phase (python built-in method)
            Calling an instance of a Runnable class will excecute the run() method and return the results.
        Returns:
            Results: a result object of the executable
                The results construction should be implemented in the get_results method()
        """
        return self.run(*args, **kwargs)

    @classmethod
    def get_results_type(cls) -> type[R]:
        try:
            return get_args(cls.__base__)[0]
        except (AttributeError, KeyError) as e:
            cls.logger.error(
                "Could not resolve results type.\nprobably due to pydantic unsupported version being used."
            )
            raise e

    @classmethod
    def generate_results_schema(cls) -> dict[str, Any]:
        return cls.get_results_type().model_json_schema()

    def set_platform_api_connector(self, platform_communicator: IPlatformConnectorApi):
        # set the relevant communicator to the platform API.
        # This function should be used by CyClarity internal logic and not by the user.
        self._platform_api.set_connector(platform_communicator)

    def set_logger(self, logger: logging.Logger):
        self._logger = logger
