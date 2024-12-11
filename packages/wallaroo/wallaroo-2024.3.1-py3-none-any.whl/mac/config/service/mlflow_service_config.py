"""This module features the MLflowServiceConfig class."""

import logging
from typing import Dict, Optional

from pydantic import ConfigDict, field_validator

from mac.config.service import ServiceConfig
from mac.exceptions import MLflowModelSignatureError
from mac.types import SupportedServices

logger = logging.getLogger(__name__)


class MLflowServiceConfig(ServiceConfig):
    """This class represents the configuration of MLflowService."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True, extra="forbid", protected_namespaces=()
    )

    model_signature: Optional[Dict[str, str]] = None

    @property
    def service_type(self) -> SupportedServices:
        """This property specifies the type of service this configuration is for."""
        return SupportedServices.MLFLOW

    @field_validator("model_signature")
    @classmethod
    def model_signature_check(cls, value):
        """Checks if the signature dictionary has the valid keys.
        Only ["inputs", "outputs"] are allowed as keys. If the keys are not
        valid, then MLflowModelSignatureError is raised.

        :param value: Model signature as a dictionary.

        :raises MLflowModelSignatureError: If the parameter value does not have the
            valid keys.

        :return: validated value
        """
        keys = value.keys()
        expected_keys = ["inputs", "outputs"]
        if set(keys) != set(expected_keys):
            message = f"Found keys {keys}, but expected {expected_keys}."
            logger.error(message)
            raise MLflowModelSignatureError(message)

        return value
