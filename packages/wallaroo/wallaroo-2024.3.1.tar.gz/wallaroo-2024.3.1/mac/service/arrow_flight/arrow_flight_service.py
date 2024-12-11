"""This module implements the ArrowFlightService class, for serving models using
Arrow Flight RPC."""

import logging

from mac.config.service import ArrowFlightServiceConfig
from mac.service import Service
from mac.service.arrow_flight.server import ArrowFlightServer
from mac.types import PythonStep

logger = logging.getLogger(__name__)


class ArrowFlightService(Service):
    """This class implements the ArrowFlightService, in order to serve
    a PythonStep using Arrow Flight RPC.

    Attributes:
        - arrow_flight_server: An ArrowFlightServer instance.
    """

    def __init__(self, arrow_flight_server: ArrowFlightServer) -> None:
        """Initialize ArrowFlightService class."""
        self._arrow_flight_server = arrow_flight_server

    def serve(self) -> None:
        """This method serves an Inference object using the Arrow Flight RPC service."""
        logging.info(
            f"[📡] Starting server on `{self._arrow_flight_server.location}`..."  # type: ignore [union-attr] # noqa: E501
        )
        self._arrow_flight_server.serve()  # type: ignore [union-attr]


def create_arrow_flight_service(
    config: ArrowFlightServiceConfig, python_step: PythonStep
) -> ArrowFlightService:
    """Initializes an ArrowFlightService based on the given ArrowFlightServiceConfig
    and a given Inference object.

    :param config: A ArrowFlightServiceConfig instance.
    :param python_step: A PythonStep instance.

    :return: An ArrowFlightService instance.
    """
    logger.info("Creating Arrow Flight RPC service...")

    server = ArrowFlightServer(
        python_step=python_step,
        server_config=config.server,
        output_schema=config.output_schema,
    )
    service = ArrowFlightService(server)

    logger.info("Successfully created Arrow Flight RPC service.")

    return service
