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

from typing import Any, Dict, List, Optional

from colorama import Fore

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import ExecuteDeploymentRequest
from kelvin.sdk.lib.configs.docker_configs import DockerConfigs
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import InvalidApplicationConfiguration, KDockerException
from kelvin.sdk.lib.models.apps.common import ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour, KelvinAppConfiguration, ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import (
    DockerAppBuildingObject,
    KelvinAppBuildingObject,
    ProjectBuildingObject,
    ProjectCreationParametersObject,
)
from kelvin.sdk.lib.models.factories.app_setup_configuration_objects_factory import (
    get_bridge_app_building_object,
    get_kelvin_app_building_object,
    get_project_building_object,
)
from kelvin.sdk.lib.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.models.factories.project.factory import ProjectFactory
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.ksdk_docker import DockerImageName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.schema.schema_manager import validate_app_schema_from_app_config_file
from kelvin.sdk.lib.utils.application_utils import check_if_app_name_is_valid
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


# 1 - entrypoint functions
def app_create_from_parameters(
    app_dir: str,
    app_name: str,
    app_description: str,
    app_type: ProjectType,
    app_flavour: ApplicationFlavour,
    kelvin_app_lang: ApplicationLanguage,
) -> OperationResponse:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    Parameters
    ----------
    app_dir: str
        the app's targeted dir. Will contain all the application files.
    app_name: str, optional
        the name of the new app.
    app_description: str, optional
        the description of the new app.
    app_type: ProjectType, optional
        the type of the new application. # E.g. 'docker', 'kelvin'.
    app_flavour: ApplicationFlavour, optional
        the flavour of the new application. # E.g. 'default', 'injector', 'extractor'.
    kelvin_app_lang: ApplicationLanguage, optional
        the language the new app will be written on. For kelvin apps only. # E.g. python.

    Returns
    ----------
    OperationResponse
        an OperationResponse object wrapping the result of the creation of the application.
    """
    from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectCreationParametersObject

    try:
        project_creation_parameters = ProjectCreationParametersObject(
            app_dir=app_dir,
            app_name=app_name,
            app_description=app_description,
            app_type=app_type,
            app_flavour=app_flavour,
            kelvin_app_lang=kelvin_app_lang,
        )
        return project_create(project_creation_parameters=project_creation_parameters)
    except Exception as exc:
        error_message = f"Error creating application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def project_create(project_creation_parameters: ProjectCreationParametersObject) -> OperationResponse:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    Parameters
    ----------
    project_creation_parameters: ProjectCreationParametersObject
        the object containing all the required variables for App creation.

    Returns
    ----------
    OperationResponse
        an OperationResponse object wrapping the result of the creation of the application.
    """
    try:
        check_if_app_name_is_valid(app_name=project_creation_parameters.app_name)

        project_class_name: str = project_creation_parameters.app_type.project_class_name()
        logger.info(f'Creating new {project_class_name} "{project_creation_parameters.app_name}"')

        # 1 - Create the base directory and app creation object
        project = ProjectFactory.create_project(project_creation_parameters=project_creation_parameters)
        project.create_dirs_and_files()

        app_creation_success_message: str = (
            f'Successfully created new {project_class_name}: "{project_creation_parameters.app_name}".'
        )
        logger.relevant(app_creation_success_message)
        logger.info(f"Kelvin code samples are available at: {Fore.YELLOW}{GeneralConfigs.code_samples_url}{Fore.RESET}")

        return OperationResponse(success=True, log=app_creation_success_message)
    except Exception as exc:
        error_message = ""
        if project_creation_parameters:
            app_name = project_creation_parameters.app_name
            error_message = f'Error creating "{app_name}" project: {str(exc)}'
            logger.exception(error_message)
            if project_creation_parameters.app_dir and app_name:
                app_complete_directory = KPath(project_creation_parameters.app_dir) / app_name
                app_complete_directory.delete_dir()
        return OperationResponse(success=False, log=error_message)


def legacy_project_build(build_obj: ProjectBuildingObject) -> OperationResponse:
    from kelvin.sdk.lib.session.session_manager import session_manager

    logger.warning(
        f"""Deprecation warning: Building legacy applications will be deprecated in future versions.
            Please consider updating your application. See: {session_manager.get_documentation_link_for_current_url()}"""
    )

    try:
        app_type = build_obj.app_config_model.app.type
        if app_type == ProjectType.kelvin:
            app_type = ProjectType.kelvin_legacy
        app_name = build_obj.app_config_model.info.name
        app_version = build_obj.app_config_model.info.version

        if app_type in {ProjectType.kelvin_legacy, ProjectType.kelvin}:
            logger.info(f'Building application "{app_name}"')
            kelvin_app_building_object = get_kelvin_app_building_object(
                app_dir=build_obj.app_dir_path,
                app_config_raw=build_obj.app_config_raw,
                build_for_upload=build_obj.build_for_upload,
                fresh_build=build_obj.fresh_build,
            )
            return _build_kelvin_app(kelvin_app_building_object=kelvin_app_building_object)
        elif app_type == ProjectType.bridge:
            logger.info(f'Building "Bridge type" application "{app_name}"')
            bridge_app_building_object = get_bridge_app_building_object(
                app_dir=build_obj.app_dir_path,
                app_config_raw=build_obj.app_config_raw,
                build_for_upload=build_obj.build_for_upload,
                fresh_build=build_obj.fresh_build,
            )
            return _build_kelvin_app(kelvin_app_building_object=bridge_app_building_object)

        elif app_type == ProjectType.docker:
            logger.info(f'Building "Docker type" application "{app_name}"')
            docker_app_building_object = DockerAppBuildingObject(**build_obj.dict())
            return _build_docker_app(docker_app_building_object=docker_app_building_object)

        return OperationResponse(success=True, log=f"Project {app_name}:{app_version} successfully built")
    except Exception as exc:
        error_message = f"""Error building application: {str(exc)}

            Consider building the app in verbose mode to retrieve more information: --verbose
        """
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def project_build(
    app_dir: str,
    fresh_build: bool = False,
    build_for_upload: bool = False,
    docker_registry: str = "",
    multiarch: bool = False,
    build_args: Dict[str, str] = {},
) -> OperationResponse:
    """
    The entry point for the building of an application.

    Attempts to read the application content

    Parameters
    ----------
    app_dir : str
        the path where the application is hosted.
    fresh_build : bool
        If specified will remove any cache and rebuild the application from scratch.
    build_for_upload : bool
        indicates whether or the package object aims for an upload.
    docker_registry: str
        the docker registry to push the image to.
    multiarch : bool
        If specified, will try to build the application for multiple architectures.
    build_args: Dict[str, str]
        build arguments to pass to the docker build command.

    Returns
    -------
    OperationResponse
        an OperationResponse object wrapping the result of the application build process.

    """
    try:

        building_object = get_project_building_object(app_dir=app_dir, fresh_build=fresh_build)
        building_object.build_args = build_args
        building_object.build_for_upload = build_for_upload
        building_object.docker_registry = docker_registry
        building_object.multiarch = multiarch

        logger.info("Validating application schema...")
        validate_app_schema_from_app_config_file(app_config=building_object.app_config_raw)

        logger.info(f'Building application "{building_object.app_config_model.info.name}"')
        dockerfile = building_object.app_dir_path / "Dockerfile"
        if not dockerfile.exists():
            logger.error("Dockerfile not found.")
            return legacy_project_build(build_obj=building_object)

        return _build_app(building_object=building_object)

    except Exception as exc:
        error_message = f"Error building application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def __generate_app_deploy_payload(conf: KelvinAppConfiguration, assets: List[str]) -> Dict[str, Any]:
    mappings: Dict[str, Any] = {}
    m_inputs: List[Dict[str, Any]] = []
    m_outputs: List[Dict[str, Any]] = []
    m_resources: List[str] = []

    inputs = []
    outputs = []

    if conf.app.kelvin:
        inputs = conf.app.kelvin.inputs if conf.app.kelvin.inputs else []
        outputs = conf.app.kelvin.outputs if conf.app.kelvin.outputs else []

    for i in inputs:
        if not i.sources:
            m_inputs.append(
                {
                    "app": i.name,
                    "datastream": i.name,
                }
            )
        else:
            for s in i.sources:
                if s.names:
                    for n in s.names:
                        m_inputs.append(
                            {
                                "app": i.name,
                                "datastream": n,
                            }
                        )
    for o in outputs:
        if not o.targets:
            m_outputs.append(
                {
                    "app": o.name,
                    "datastream": o.name,
                }
            )
        else:
            for s in o.targets:
                if s.names:
                    for n in s.names:
                        m_outputs.append(
                            {
                                "app": o.name,
                                "datastream": n,
                            }
                        )

    for a in assets:
        m_resources.append(f"krn:asset:{a}")

    mappings["mappings"] = {"inputs": m_inputs, "outputs": m_outputs}
    mappings["resources"] = m_resources

    return mappings


def project_deploy(
    app_dir: str,
    assets: List[str],
    fresh_build: bool = False,
) -> OperationResponse:
    """
    The entry point for the deployment of an application.

    Attempts to read the application content

    Parameters
    ----------
    app_dir : str
        the path where the application is hosted.
    assets: List[str]
        list of assets to deploy the project to.
    fresh_build : bool
        If specified will remove any cache and rebuild the application from scratch.

    Returns
    -------
    OperationResponse
        an OperationResponse object wrapping the result of the application build process.

    """
    try:
        from kelvin.sdk.lib.session.session_manager import session_manager

        # 0 - Load the app configuration and validate its contents against the schema.
        app_config_file_path: KPath = KPath(app_dir) / "app.yaml"
        loaded_app_config_object = app_config_file_path.read_yaml()
        validate_app_schema_from_app_config_file(app_config=loaded_app_config_object)

        client = session_manager.login_client_on_current_url()
        app_configuration = KelvinAppConfiguration(**loaded_app_config_object)
        app_name_with_version = DockerImageName.parse(name=app_configuration.info.app_name_with_version)

        # 1 Generate the correct payload for the app deploy - mappings and resources. get name and version.
        name = app_configuration.info.name
        version = app_name_with_version.version or "0.0.1"
        app_deploy_payload = __generate_app_deploy_payload(app_configuration, assets)
        parsed_app_deploy_payload: ExecuteDeploymentRequest = ExecuteDeploymentRequest.parse_obj(app_deploy_payload)
        deploy_result = client.app_projection.deploy_app_manager_app_version(
            app_name=name, version=version, data=parsed_app_deploy_payload
        )
        logger.relevant(deploy_result)
        return OperationResponse(success=True, log=f"Project {name} successfully deployed")
    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error deploying application: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)
    except Exception as exc:
        error_message = f"""Error deploying application: {str(exc)}
        """
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def app_image_unpack(
    app_name_with_version: str,
    output_dir: str,
    container_dir: Optional[str] = None,
    clean_dir: bool = True,
) -> OperationResponse:
    """
    Extract the content of an image into a target directory.

    Parameters
    ----------
    app_name_with_version: str
        the name of the image to unpack the app from.
    container_dir: str
        The directory to extract from the container.
    output_dir: str
        the output directory to output the extracted content.
    clean_dir: str
        clean the directory before extracting into it.

    Returns
    ----------
    OperationResponse
        an OperationResponse object wrapping the result of the image extraction operation.

    """
    try:
        # 1 - Build the DockerImageName object for the application
        container_dir = container_dir or DockerConfigs.container_app_dir_path
        logger.info(f'Extracting directory "{container_dir}" from "{app_name_with_version}" into "{output_dir}"')

        docker_manager = get_docker_manager()
        docker_image_name: DockerImageName = DockerImageName.parse(name=app_name_with_version)

        # 2 - Find the provided application. If it does not exist, attempt to retrieve the registry's counterpart
        application_name: str = docker_image_name.raw_name
        docker_manager.check_if_docker_image_exists(docker_image_name=application_name, raise_exception=True)

        dir_was_extracted = docker_manager.extract_dir_from_docker_image(
            app_name=application_name,
            output_dir=output_dir,
            container_dir=container_dir,
            clean_dir=clean_dir,
        )

        if dir_was_extracted:
            success_message = f'Directory "{container_dir}" successfully extracted to "{output_dir}"'
            logger.relevant(success_message)
            return OperationResponse(success=True, log=success_message)
        else:
            raise KDockerException(f'The directory "{container_dir}" could not be extracted from the image.')

    except Exception as exc:
        error_message = f"Error unpacking application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def app_config(app_config_file_path: str) -> OperationResponse:
    """
    Yields the loaded json/dict for the provided configuration file path. (Parameters)

    Parameters
    ----------
    app_config_file_path: str
        the object containing all the required variables for App creation.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object wrapping the json of the app configuration file.

    """
    try:
        path_to_config_file: KPath = KPath(app_config_file_path.strip('"')).complete_path()
        if not path_to_config_file.exists():
            raise InvalidApplicationConfiguration(message="Please provide a valid file")
        return OperationResponse(success=True, data=path_to_config_file.read_yaml())
    except Exception as exc:
        error_message = f"Error loading the provided configuration file: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def app_image_remove(app_name_with_version: str) -> OperationResponse:
    """
    Remove the specified application from the existing image list (in the docker instance).

    Parameters
    ----------
    app_name_with_version: str
        the app to be removed. Must include the version.

    Returns
    ----------
    OperationResponse
        an OperationResponse object wrapping the result of the application image removal operation.

    """
    try:
        image = DockerImageName.parse(name=app_name_with_version)

        logger.info(f'Removing packaged application "{image.repository_image_name}"')

        docker_manager = get_docker_manager()
        removed = docker_manager.remove_docker_image(docker_image_name=image.repository_image_name)
        if removed:
            success_message = f'Successfully removed application: "{image.repository_image_name}"'
            logger.relevant(success_message)
        else:
            success_message = f'Unable to remove application (not found): "{image.repository_image_name}"'
        return OperationResponse(success=True, log=success_message)
    except Exception as exc:
        error_message = f"Error removing application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def app_image_config(
    app_name_with_version: str, output_dir: str, image_dir: str = DockerConfigs.container_app_config_file_path
) -> OperationResponse:
    """
    Extract the app configuration file (app.yaml) from a built image into a specific directory.

    Parameters
    ----------
    app_name_with_version: str
        the name of the image to unpack the app configuration file from.
    output_dir: str
        the output directory to output the app configuration file.
    image_dir: str
        the directory from which to extract the application configuration file.

    Returns
    --------
    OperationResponse
        an OperationResponse object wrapping the result of the application configuration extraction operation.

    """
    try:
        # 1 - Build the DockerImageName object for the application
        docker_manager = get_docker_manager()
        docker_image_name = DockerImageName.parse(name=app_name_with_version)

        # 2 - Find the provided application. If it does not exist, attempt to retrieve the registry's counterpart
        application_name: str = docker_image_name.raw_name
        docker_manager.check_if_docker_image_exists(docker_image_name=application_name, raise_exception=True)

        logger.info(f'Extracting "{application_name}"\'s configuration file to directory "{output_dir}"')

        app_config_was_unpacked = docker_manager.extract_dir_from_docker_image(
            app_name=application_name, output_dir=output_dir, container_dir=image_dir, clean_dir=False
        )

        success_message: str = ""
        if app_config_was_unpacked:
            success_message = f'Configuration file of "{application_name}" successfully extracted to "{output_dir}"'
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except Exception as exc:
        error_message = f"Error extracting application configuration: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


# 2 - internal, utils methods
def _build_docker_app(docker_app_building_object: DockerAppBuildingObject) -> OperationResponse:
    """
    The entry point for the building of a 'Docker' type application.

    Parameters
    ----------
    docker_app_building_object : DockerAppBuildingObject
        the ProjectBuildingObject that contains all necessary variables to build a docker app.

    Returns
    -------
    OperationResponse
        an OperationResponse object wrapping the result of whether the Docker application was successfully built.

    """
    docker_manager = get_docker_manager()

    app_name = docker_app_building_object.app_config_model.info.name
    app_version = docker_app_building_object.app_config_model.info.version

    build_result = docker_manager.build_docker_app_image(docker_build_object=docker_app_building_object)
    result_message = f'Image successfully built: "{app_name}:{app_version}"'
    logger.relevant(result_message)

    return OperationResponse(success=build_result, log=result_message)


def _build_kelvin_app(kelvin_app_building_object: KelvinAppBuildingObject) -> OperationResponse:
    """
    The entry point for the building of a kelvin-type application.

    Package the kelvin application using a KelvinAppBuildingObject, thus building a valid docker image.

    Parameters
    ----------
    kelvin_app_building_object : KelvinAppBuildingObject
        the object that contains all the required variables to build an app.

    Returns
    -------
    OperationResponse
        an OperationResponse object wrapping the result of whether the kelvin application was successfully built.

    """
    docker_manager = get_docker_manager()

    # 1 - Retrieve the variables necessary to build the application
    app_name = kelvin_app_building_object.full_docker_image_name
    app_version = kelvin_app_building_object.app_config_model.info.version
    app_build_dir_path = kelvin_app_building_object.app_build_dir_path
    app_config_file_path = kelvin_app_building_object.app_config_file_path
    app_dir_path = kelvin_app_building_object.app_dir_path
    app_build_dir_path.delete_dir().create_dir()

    logger.debug(f'Provided configuration file path: "{app_config_file_path}"')
    logger.debug(f'Provided application directory: "{app_dir_path}"')

    # 3.1 - Setup the broker configuration
    if not kelvin_app_building_object.build_for_upload:
        docker_manager.setup_kelvin_broker_configuration(
            app_name=kelvin_app_building_object.app_config_model.info.name,
            target_output_directory=app_build_dir_path,
            app_config_file_path=app_config_file_path,
            project_type=kelvin_app_building_object.app_config_model.app.type,
        )

    # 3.2 - Finally, build the image
    success_build = docker_manager.build_kelvin_app_docker_image(kelvin_app_building_object=kelvin_app_building_object)
    logger.relevant(f'Image successfully built: "{app_name}:{app_version}"')

    return OperationResponse(success=success_build)


def _build_app(building_object: ProjectBuildingObject) -> OperationResponse:
    """
    The entry point for the building of a 'Docker' type application.

    Parameters
    ----------
    docker_app_building_object : DockerAppBuildingObject
        the ProjectBuildingObject that contains all necessary variables to build a docker app.

    Returns
    -------
    OperationResponse
        an OperationResponse object wrapping the result of whether the Docker application was successfully built.

    """
    docker_manager = get_docker_manager()

    app_name = building_object.app_config_model.info.name
    app_version = building_object.app_config_model.info.version

    build_result = docker_manager.build_kelvin_v2_app_image(build_object=building_object)
    result_message = f'Image successfully built: "{app_name}:{app_version}"'
    logger.relevant(result_message)

    return OperationResponse(success=build_result, log=result_message)
