"""This module features the ArrowFlightServiceConfig class."""

import logging

import pyarrow as pa

from mac.config.service.service_config import ServiceConfig
from mac.types import SupportedServices

logger = logging.getLogger(__name__)


class ArrowFlightServiceConfig(ServiceConfig):
    """This class represents the configuration of ArrowFlightService."""

    output_schema: pa.Schema

    @property
    def service_type(self) -> SupportedServices:
        """This property specifies the type of service this configuration is for."""
        return SupportedServices.FLIGHT
