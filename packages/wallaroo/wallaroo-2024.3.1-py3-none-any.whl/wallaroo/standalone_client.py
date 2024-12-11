import json
import os
import pathlib
import sys
import time
from typing import Any, Dict, List, Optional, Union

import requests

from wallaroo.inference_result import InferenceResult
from wallaroo.model_version import ModelVersion
from wallaroo.object import DeploymentError
from wallaroo.pipeline_config import PipelineConfig
from wallaroo.version import _user_agent


class StandaloneClient:
    def __init__(
        self,
        host: str,
        port: int,
        model_version: Optional[ModelVersion] = None,
        pipeline_config: Optional[PipelineConfig] = None,
        interactive: Optional[bool] = None,
    ):
        if (model_version and pipeline_config) or not (
            model_version or pipeline_config
        ):
            raise RuntimeError(
                "Specify either a model or a pipeline config for inference"
            )
        self._host = host
        self._port = port
        self._model_version = model_version
        self._pipeline_config = pipeline_config

        if interactive is not None:
            self._interactive = interactive
        elif "JUPYTER_SVC_SERVICE_HOST" in os.environ:
            self._interactive = True
        else:
            self._interactive = False

    def _url(self) -> str:
        if self._model_version:
            return (
                f"http://{self._host}:{self._port}/models/{self._model_version.name()}"
            )
        elif self._pipeline_config:
            return f"http://{self._host}:{self._port}/pipelines/{self._pipeline_config.pipeline_name}"
        else:
            raise RuntimeError(
                "Neither a model or pipeline config was specified for inference"
            )

    def status(self) -> Dict[str, Any]:
        """Returns a dict of standalone engine model status.

        Example: {'models': [{'class': 'ccfraud', 'name': 'z5', 'status': 'Running'}]}

        Example: {'models': [{'class': 'postprocess',
                  'name': 'first-postprocess',
                  'status': 'Running'},
                  {'class': 'noopfloats', 'name': 'noopv1', 'status': 'Running'},
                  {'class': 'preprocess', 'name': 'first-preprocess', 'status': 'Running'}]}

        Example: {"models": [{"class":"synerror",
                              "name":"v1",
                              "status":{"Error":"Python compile or runtime error [\"  File \\\"//tmp/.tmpk7mJpI/syntax_error.py\\\", line 1\", \"    PLEASE CRASH HERE\", \"           ^\", \"SyntaxError: invalid syntax\"]"}}]}

        """
        url = f"http://{self._host}:{self._port}/models"
        headers = {"User-Agent": _user_agent}
        try:
            res = requests.get(url, timeout=3, headers=headers)
        except Exception:
            raise DeploymentError(f"Error getting status from {url}")
        data = None
        if res.status_code == 200:
            data = res.json()
        else:
            raise DeploymentError(
                f"Engine at {url} returned code {res.status_code}: {res.text}"
            )
        return data

    def infer(self, tensor: Dict[str, Any]) -> List[InferenceResult]:
        if not isinstance(tensor, dict):
            raise TypeError(f"tensor is {type(tensor)} but 'dict' is required")

        url = self._url()
        warning = False
        duration = 300
        headers = {"User-Agent": _user_agent}
        for ix in range(duration + 1):
            res = None
            try:
                res = requests.post(
                    url,
                    json=tensor,
                    timeout=1,
                    headers=headers,
                )
                data = res.json()
                break
            except (requests.exceptions.RequestException, json.JSONDecodeError):
                if self._interactive:
                    if not warning:
                        sys.stdout.write(
                            "Waiting for deployment to become ready - this may take a few seconds"
                        )
                        warning = True
                    sys.stdout.write(".")
                time.sleep(1)
        if ix == duration:
            raise RuntimeError(f"Deployment did not come up within {duration}s")
        return [InferenceResult(None, d) for d in data]

    def infer_from_file(
        self, filename: Union[str, pathlib.Path]
    ) -> List[InferenceResult]:
        if not isinstance(filename, pathlib.Path):
            filename = pathlib.Path(filename)
        with filename.open("rb") as f:
            tensor = json.load(f)
        return self.infer(tensor)
