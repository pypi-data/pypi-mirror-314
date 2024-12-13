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

import click

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import ClickExpandedPath, KSDKCommand, KSDKGroup
from kelvin.sdk.lib.utils.logger_utils import logger


@click.group(cls=KSDKGroup)
def bridge() -> None:
    """Manage and view bridges."""


@bridge.command(cls=KSDKCommand)
def list() -> bool:
    """List all available bridges in the platform."""
    from kelvin.sdk.interface import bridge_list

    return bridge_list(should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("bridge_name", nargs=1, type=click.STRING, required=False)
def show(bridge_name: str) -> bool:
    """Show the details of a bridge.

    e.g. kelvin bridge show "my-bridge"
    """
    from kelvin.sdk.interface import bridge_show

    if bridge_name is None:
        bridge_name = input("Enter the name of the bridge you want to show: ")

    return bridge_show(bridge_name=bridge_name, should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.option(
    "--bridge-config",
    type=ClickExpandedPath(exists=True),
    required=False,
    help=KSDKHelpMessages.bridge_config,
)
@click.option("--name", type=click.STRING, required=False, help=KSDKHelpMessages.bridge_name)
def undeploy(
    bridge_config: Optional[str],
    name: Optional[str],
) -> bool:
    """Undeploy a bridge application.
    Either provide the bridge name to undeploy or a configuration file to extract it from.

    """
    from kelvin.sdk.interface import bridge_undeploy

    if not (bridge_config or name):
        logger.error("Unable to undeploy bridge. Either provide a bridge name or bridge config.")
        return False

    return bridge_undeploy(bridge_config=bridge_config, bridge_name=name).success
