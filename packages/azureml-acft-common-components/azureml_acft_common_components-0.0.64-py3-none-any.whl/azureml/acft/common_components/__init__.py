# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Azure ML ACFT Common Components package."""

__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import sys

from azureml.automl.core.shared import logging_utilities, log_server

from .model_selector.component import ModelSelector
from .model_selector.constants import ModelSelectorConstants, ModelSelectorDefaults, ModelSelectorAPIConstants

from .utils.logging_utils import set_logging_parameters, get_logger_app, LoggingLiterals

try:
    from ._version import ver as VERSION, selfver as SELFVERSION
    __version__ = VERSION
except ImportError:
    VERSION = '0.0.0+dev'
    SELFVERSION = VERSION
    __version__ = VERSION

PROJECT_NAME = __name__

__all__ = [
    "ModelSelector",
    "ModelSelectorConstants",
    "ModelSelectorDefaults",
    "ModelSelectorAPIConstants",
    "set_logging_parameters",
    "get_logger_app",
    "LoggingLiterals",
]

# Mark this package as being allowed to log certain built-in types
module = sys.modules[__name__]
logging_utilities.mark_package_exceptions_as_loggable(module)
log_server.install_sockethandler(__name__)
