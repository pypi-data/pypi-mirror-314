"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

from typing import Any, Dict, Optional

from pydantic.v1 import Extra, Field, validator

from kelvin.sdk.lib.models.generic import KPath, KSDKModel

try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore


class BridgeDeploymentRequest(KSDKModel):
    node_name: str
    bridge_name: str = Field(..., max_length=32)
    bridge_title: Optional[str] = Field(..., max_length=64)
    bridge_config: str
    protocol: Literal["opc-ua", "mqtt", "modbus", "roc"]
    quiet: bool = False


class BridgeTemplateData(KSDKModel):
    class Config:
        extra = Extra.allow

    @validator("bridge_config", pre=True)
    def validate_bridge_config(cls, value: str) -> KPath:  # noqa
        path = KPath(value)
        if not path.exists():
            raise ValueError(f"Path does not exist: {value}")
        return path

    @validator("status", "result", pre=True)
    def validate_empty_fields(cls, value: Optional[str]) -> Optional[str]:  # noqa
        if not value:
            return None
        return value

    status: Optional[str] = None
    result: Optional[Literal["success", "failed", "skip"]] = None

    node_name: str
    bridge_name: str
    bridge_title: str

    bridge_config: KPath

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {**super().dict(*args, **kwargs), "bridge_config": str(self.bridge_config)}
