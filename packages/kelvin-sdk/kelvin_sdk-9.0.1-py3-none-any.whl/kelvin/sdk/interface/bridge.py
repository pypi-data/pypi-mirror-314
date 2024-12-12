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

from typing import Optional

from typeguard import typechecked

from kelvin.sdk.lib.models.bridge.ksdk_bridge_deployment import BridgeDeploymentRequest
from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def bridge_list(should_display: bool = False) -> OperationResponse:
    """
    List all available bridges in the platform.

    Parameters
    ----------
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the bridges available on the platform.

    """
    from kelvin.sdk.lib.api.bridge import bridge_list as _bridge_list

    return _bridge_list(query=None, should_display=should_display)


@typechecked
def bridge_show(bridge_name: str, should_display: bool = False) -> OperationResponse:
    """
    Show the details of a bridge.

    Parameters
    ----------
    bridge_name : str
        The name of the bridge.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded bridge instance and its detailed data.

    """
    from kelvin.sdk.lib.api.bridge import bridge_show as _bridge_show

    return _bridge_show(bridge_name=bridge_name, should_display=should_display)


@typechecked
def bridge_deploy(bridge_deployment_request: BridgeDeploymentRequest) -> OperationResponse:
    """
    Deploy a workload from the specified deploy request.

    Parameters
    ----------
    workload_deployment_request: WorkloadDeploymentRequest
        the deployment object that encapsulates all the necessary parameters for deploy.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the workload deploy operation.

    """
    from kelvin.sdk.lib.api.bridge import bridge_deploy as _bridge_deploy

    return _bridge_deploy(bridge_deployment_request=bridge_deployment_request)


@typechecked
def bridge_undeploy(bridge_config: Optional[str], bridge_name: Optional[str]) -> OperationResponse:
    """
    Undeploy a bridge.
    Parameters
    ----------
    bridge_config:  Optional[str]
        config file of the bridge

    bridge_name: Optional[str]
        bridge name

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the workload deploy operation.

    """
    from kelvin.sdk.lib.api.bridge import bridge_name_from_config
    from kelvin.sdk.lib.api.bridge import bridge_undeploy as _bridge_undeploy

    if not bridge_name:
        bridge_name = bridge_name_from_config(bridge_config or "app.yaml")

    return _bridge_undeploy(bridge_name)
