import dataclasses
import typing
from pathlib import Path

from caseconverter import snakecase

if typing.TYPE_CHECKING:
    from .config import OARepoConfig


@dataclasses.dataclass
class RepositoryConfig:
    """Configuration of the repository"""

    prompts = {}
    repository_human_name: str
    prompts["repository_human_name"] = "Human name of the repository"

    repository_package: str
    prompts["repository_package"] = "Python package name of the whole repository"

    oarepo_version: int
    prompts["oarepo_version"] = "OARepo version to use"

    shared_package: str
    prompts["shared_package"] = "Python package name of the shared code"

    ui_package: str
    prompts["ui_package"] = "Python package name of the ui code"

    model_package: str = "models"
    prompts["model_package"] = "Directory containing model yaml files"

    @classmethod
    def default_shared_package(cls, config: "OARepoConfig", values):
        """Returns the default site package name based on the project directory name"""
        return f"shared"

    @classmethod
    def default_ui_package(cls, config: "OARepoConfig", values):
        """Returns the default site package name based on the project directory name"""
        return f"ui"

    @classmethod
    def default_model_package(cls, config: "OARepoConfig", values):
        """Returns the default package name based on the project directory name"""
        return f"models"

    @classmethod
    def default_repository_package(cls, config, values):
        """Returns the default repository package name based on the project directory name"""
        return snakecase(Path(config.repository_dir).name)

    @classmethod
    def default_repository_human_name(cls, config, values):
        """Returns the default repository package name based on the project directory name"""
        return snakecase(Path(config.repository_dir).name).replace("_", " ").title()

    @classmethod
    def default_oarepo_version(cls, config, values):
        return 12
