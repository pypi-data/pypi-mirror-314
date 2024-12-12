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

from typing import List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import BridgeDeploy
from kelvin.sdk.client.model.responses import Bridge
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import KSDKException
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.models.bridge.ksdk_bridge_deployment import BridgeDeploymentRequest
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.schema.schema_manager import validate_app_schema_from_app_config_file
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import DisplayObject, display_data_entries, display_data_object
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


def bridge_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    List all available bridges in the platform.

    Parameters
    ----------
    query : str, optional
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the bridges available on the platform.

    """
    try:
        bridge_list_step_1 = "Retrieving bridges.."
        if query:
            bridge_list_step_1 = f'Searching bridges that match "{query}"'

        logger.info(bridge_list_step_1)

        client = session_manager.login_client_on_current_url()

        bridges = cast(List, client.bridge.list_bridge(search=query)) or []

        display_obj = display_data_entries(
            data=bridges,
            header_names=["Name", "Title", "Node name", "Workload name", "Protocol", "Created", "Updated"],
            attributes=["name", "title", "cluster_name", "workload_name", "protocol", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Bridges"),
            should_display=should_display,
            no_data_message="No bridges available",
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridges: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridges: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


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
    try:
        logger.info(f'Retrieving bridge details for "{bridge_name}"')

        client = session_manager.login_client_on_current_url()

        bridge_info: Bridge = client.bridge.get_bridge(bridge_name=bridge_name)
        bridge_info_display: DisplayObject = display_data_object(
            data=bridge_info,
            should_display=should_display,
            object_title=GeneralConfigs.table_title.format(title="Bridge Info"),
        )

        return OperationResponse(success=True, data=bridge_info_display.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving bridge: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving bridge: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def bridge_deploy(bridge_deployment_request: BridgeDeploymentRequest) -> OperationResponse:
    """
    Deploy a bridge from the specified deploy request.

    Parameters
    ----------
    bridge_deployment_request: BridgeDeploymentRequest
        the deployment object that encapsulates all the necessary parameters for deploy.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload deploy operation.

    """
    try:
        logger.info(f'Deploying bridge "{bridge_deployment_request.bridge_name}"..')

        # 0 - Load the app configuration and validate its contents against the schema.
        app_config_file_path: KPath = KPath(bridge_deployment_request.bridge_config)
        loaded_app_config_object = app_config_file_path.read_yaml()
        validate_app_schema_from_app_config_file(app_config=loaded_app_config_object)

        # 1 - Load the specific payload for the bridge.
        app = loaded_app_config_object.get("app", {})
        if not app:
            raise Exception("Invalid app configuration file. Missing 'app' section.")

        bridge = app.get("bridge", {})
        if not bridge:
            raise Exception("Invalid app configuration file. Missing 'app.bridge' section.")

        configuration = bridge.get("configuration", {})
        if not configuration:
            raise Exception("Invalid app configuration file. Missing 'app.bridge.configuration' section.")

        metrics_map = bridge.get("metrics_map", {})  # I think this might be optional

        logging_level = bridge.get("logging_level", "INFO")

        # 1.1 Prepare the payload, merge metrics_map and configuration
        payload = {"metrics_map": metrics_map, "configuration": configuration, "logging_level": logging_level}

        client = session_manager.login_client_on_current_url()

        if not bridge_deployment_request.quiet and loaded_app_config_object:
            logger.info("Bridge configuration successfully loaded")

        bridge_deploy_payload: BridgeDeploy = BridgeDeploy(
            cluster_name=bridge_deployment_request.node_name,
            name=bridge_deployment_request.bridge_name,
            title=bridge_deployment_request.bridge_title or bridge_deployment_request.bridge_name,
            payload=payload,
            protocol=bridge_deployment_request.protocol,
        )
        deploy_result = client.bridge.deploy_bridge(data=bridge_deploy_payload)
        success_message = ""
        if not bridge_deployment_request.quiet and deploy_result:
            success_message = f"""\n
                Bridge "{deploy_result.name}" successfully deployed.
            """
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error creating bridge: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error creating bridge: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def bridge_name_from_config(config_path: str) -> str:
    config_file = KPath(config_path)
    if not config_file.exists():
        raise KSDKException(f"couldn't find config file: '{config_file}'")

    config_yaml = config_file.read_yaml()
    config = KelvinAppConfiguration(**config_yaml)

    return config.info.name


def bridge_undeploy(bridge_name: str) -> OperationResponse:
    """
    Undeploy a bridge.

    Parameters
    ----------
    bridge_deployment_request: BridgeDeploymentRequest
        the deployment object that encapsulates all the necessary parameters for deploy.

    Returns
    -------
    OperationResponse
        an OperationResponse object encapsulating the result of the workload deploy operation.

    """
    try:
        logger.info(f'Undeploying bridge "{bridge_name}"..')

        client = session_manager.login_client_on_current_url()

        client.bridge.delete_bridge(bridge_name=bridge_name)

        logger.relevant("Bridge successfully undeployed")
        return OperationResponse(success=True, log="Bridge successfully undeployed")
    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error undeploying bridge: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)
