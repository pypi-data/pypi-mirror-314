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

from typing import List, Tuple

from kelvin.krn import KRNAsset
from kelvin.sdk.client.error import APIError
from kelvin.sdk.lib.exceptions import KSDKException
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


def get_undeploy_info_from_config(app_dir: str) -> Tuple[str, str, List[str]]:
    app_config_file_path: KPath = KPath(app_dir) / "app.yaml"

    if not app_config_file_path.exists():
        raise KSDKException(f"couldn't find app.yaml config file on the given directory: '{app_dir}'")
    loaded_app_config_object = app_config_file_path.read_yaml()

    app_configuration = KelvinAppConfiguration(**loaded_app_config_object)
    assets = []
    if app_configuration.app.kelvin is not None:
        assets = [asset.name for asset in app_configuration.app.kelvin.assets or []]

    return app_configuration.info.name, app_configuration.info.version, assets  # type: ignore


def undeploy_app(app_name: str, app_version: str, assets: List[str]) -> OperationResponse:
    try:
        client = session_manager.login_client_on_current_url()

        assets_krns = [str(KRNAsset(asset)) for asset in assets]

        logger.debug(
            f"Undeploying application.  app_name={app_name}, app_version={app_version}, resources={assets_krns}"
        )

        client.app_projection.undeploy_app_manager_app_version(
            app_name=app_name, version=app_version, data={"resources": assets_krns}
        )
        logger.relevant("App successfully undeployed")
        return OperationResponse(success=True, log="App successfully undeployed")
    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error undeploying application: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)
