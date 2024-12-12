from dataclasses import dataclass
from typing import Any, Dict, List, cast

from pydantic.v1.utils import deep_update

from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.configs.schema_manager_configs import SchemaManagerConfigs
from kelvin.sdk.lib.models.apps.common import ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour
from kelvin.sdk.lib.models.apps.ksdk_app_setup import Directory, File, MLFlowProjectCreationParametersObject
from kelvin.sdk.lib.models.factories.project.project import ProjectBase, ProjectFileTree
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.types import FileType
from kelvin.sdk.lib.schema.schema_manager import generate_base_schema_template, get_latest_app_schema_version
from kelvin.sdk.lib.utils.general_utils import dict_to_yaml


class ProjectDockerDefaultFileTree(ProjectFileTree):
    @staticmethod
    def get_tree_dict(app_root: KPath, **kwargs: Any) -> Dict:
        return {FileType.ROOT.value: {"file_type": FileType.CONFIGURATION, "directory": app_root}}

    def fundamental_dirs(self) -> List[Directory]:
        return [self.root]

    def optional_dirs(self) -> List[Directory]:
        return []


class ProjectMLFlowFileTree(ProjectFileTree):
    @staticmethod
    def get_tree_dict(app_root: KPath, **kwargs: Any) -> Dict:
        return {FileType.ROOT.value: {"file_type": FileType.APP, "directory": app_root}}

    def fundamental_dirs(self) -> List[Directory]:
        return [self.root]

    def optional_dirs(self) -> List[Directory]:
        return []


@dataclass
class KelvinV2Project(ProjectBase):
    flavour_registry = {
        ApplicationFlavour.default: ProjectDockerDefaultFileTree,
        ApplicationFlavour.mlflow: ProjectMLFlowFileTree,
    }

    def get_template_parameters(self) -> Dict:
        app_name = self.creation_parameters.app_name
        app_description = self.creation_parameters.app_description
        dir_path = self.creation_parameters.app_dir
        app_config_file = GeneralConfigs.default_app_config_file
        app_root_dir_path: KPath = KPath(dir_path) / app_name
        return {
            "app_root": app_root_dir_path,
            "app_name": app_name,
            "app_description": app_description,
            "app_version": GeneralConfigs.default_app_version,
            "app_config_file": app_config_file,
            "title": app_name.title(),
        }

    def _build_app_config_file(self, app_config_file_path: KPath) -> File:
        app_configuration = generate_base_schema_template(project_creation_parameters_object=self.creation_parameters)
        schema_data = get_latest_app_schema_version()
        if self.creation_parameters.kelvin_app_lang == ApplicationLanguage.python:
            app_configuration = deep_update(
                app_configuration,
                {
                    "system": {"environment_vars": [{"name": "KELVIN_GW_MODE", "value": "SOCKETS"}]},
                },
            )

        if isinstance(self.creation_parameters, MLFlowProjectCreationParametersObject):
            ins_dict = [{"name": i.name, "data_type": i.type} for i in self.creation_parameters.inputs]
            outs_dict = [{"name": o.name, "data_type": o.type} for o in self.creation_parameters.outputs]
            app_configuration = deep_update(
                app_configuration,
                {"app": {"kelvin": {"inputs": ins_dict, "outputs": outs_dict}}},
            )
        # insert the yaml schema lint info at the top of the file as a comment
        app_configuration_yaml: str = dict_to_yaml(
            content=app_configuration,
            comment_header={
                "yaml-language-server": "$schema="
                + SchemaManagerConfigs.general_app_schema_url.format(version=schema_data[0])
            },
        )
        file = File(file=app_config_file_path, content=app_configuration_yaml)

        return file

    def _build_file_tree(self) -> ProjectFileTree:
        # 1 - Configuration files, app dir and files
        parameters: dict = self.get_template_parameters()
        app_config_file = parameters.get("app_config_file", "")
        app_root_dir_path = parameters.get("app_root", "")

        project_file_tree_class = self.get_flavour_class()
        parameters.update(**project_file_tree_class.get_extra_template_parameters())

        # directory file tree required for a docker project
        project_type = self.creation_parameters.app_type
        kelvin_app_flavour = self.creation_parameters.app_flavour
        file_tree: ProjectFileTree = project_file_tree_class.from_tree(
            app_root=app_root_dir_path,
            template_parameters=parameters,
            project_type=project_type,
            kelvin_app_flavour=kelvin_app_flavour,
        )

        # append app config file
        app_config_file_path: KPath = app_root_dir_path / app_config_file
        file = self._build_app_config_file(app_config_file_path=app_config_file_path)
        file_tree.root.files.append(file)

        return file_tree
