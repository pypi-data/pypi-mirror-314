import dataclasses
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Set

import dacite
import yaml
from yaml.representer import SafeRepresenter

from .i18n_config import I18NConfig
from .model_config import BaseModel, ModelConfig, ModelFeature
from .repository_config import RepositoryConfig
from .ui_config import UIConfig

serialization_config = dacite.Config()
serialization_config.type_hooks = {
    Path: lambda x: Path(x),
    ModelFeature: lambda x: ModelFeature[x] if isinstance(x, str) else x,
    BaseModel: lambda x: BaseModel[x] if isinstance(x, str) else x,
    Set[ModelFeature]: lambda x: set(x),
}


def Enum_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.value)


def Set_representer(dumper, data):
    return dumper.represent_sequence(
        "tag:yaml.org,2002:seq", list(data), flow_style=True
    )


SafeRepresenter.add_multi_representer(Enum, Enum_representer)
SafeRepresenter.add_representer(set, Set_representer)

UNKNOWN = (
    object()
)  # marker for unknown default value in get_model which will emit KeyError


@dataclasses.dataclass
class OARepoConfig:
    repository_dir: Path
    repository: Optional[RepositoryConfig] = None
    models: List[ModelConfig] = dataclasses.field(default_factory=list)
    uis: List[UIConfig] = dataclasses.field(default_factory=list)
    i18n: I18NConfig = dataclasses.field(default_factory=I18NConfig)
    forks: Dict[str, str] = dataclasses.field(default_factory=dict)

    python = "python3"
    python_version = ">=3.9,<3.11"

    overrides = {}

    @property
    def venv_dir(self):
        if "venv_dir" in self.overrides:
            return Path(self.overrides["venv_dir"])
        return self.repository_dir / ".venv"

    @property
    def pdm_dir(self):
        return self.repository_dir / ".nrp/venv-pdm"

    @property
    def ui_dir(self):
        return self.repository_dir / self.repository.ui_package

    @property
    def shared_dir(self):
        return self.repository_dir / self.repository.shared_package

    @property
    def models_dir(self):
        return self.repository_dir / self.repository.model_package

    @property
    def invenio_instance_path(self):
        if "invenio_instance_path" in self.overrides:
            return Path(self.overrides["invenio_instance_path"])
        return self.venv_dir / "var" / "instance"

    @property
    def invenio_command(self):
        return self.venv_dir / "bin" / "invenio"

    @property
    def theme_dir_name(self):
        return "semantic-ui"

    def add_model(self, model: ModelConfig):
        self.models.append(model)

    def get_model(self, model_name: str, default=UNKNOWN) -> ModelConfig:
        for model in self.models:
            if model.model_name == model_name:
                return model
        if default is not UNKNOWN:
            return default
        known_models = ", ".join(sorted([model.model_name for model in self.models]))
        raise KeyError(
            f"Model {model_name} not found. Known models are: {known_models}"
        )

    def add_ui(self, ui: UIConfig):
        self.uis.append(ui)

    def get_ui(self, ui_name: str, default=UNKNOWN) -> UIConfig:
        for ui in self.uis:
            if ui.name == ui_name:
                return ui
        if default is not UNKNOWN:
            return default
        known_uis = ", ".join(sorted([ui.name for ui in self.uis]))
        raise KeyError(f"UI {ui_name} not found. Known UIs are: {known_uis}")

    def add_fork(self, python_package: str, git_fork_url: str):
        self.forks[python_package] = git_fork_url

    def remove_fork(self, python_package: str):
        del self.forks[python_package]

    @property
    def config_file(self):
        return self.repository_dir / "oarepo.yaml"

    def load(self, extra_config=None):
        if extra_config:
            config_file = extra_config
        else:
            config_file = self.config_file
            if not config_file.exists():
                return

        with open(config_file) as f:
            config_data = yaml.safe_load(f)

        loaded = dacite.from_dict(
            type(self),
            {"repository_dir": self.repository_dir, **config_data},
            serialization_config,
        )

        self.models = loaded.models
        self.uis = loaded.uis
        self.repository = loaded.repository
        self.i18n = loaded.i18n
        self.forks = loaded.forks

    def save(self):
        if self.config_file.exists():
            previous_config_data = self.config_file.read_text().strip()
        else:
            previous_config_data = None

        io = StringIO()
        dict_data = dataclasses.asdict(self)
        dict_data.pop("repository_dir")
        yaml.safe_dump(dict_data, io)
        current_data = io.getvalue().strip()

        if previous_config_data != current_data:
            self.config_file.write_text(current_data)

    @classmethod
    def global_environment(cls):
        return {
            "PIP_EXTRA_INDEX_URL": "http://127.0.0.1:4549/simple",
            "UV_EXTRA_INDEX_URL": "http://127.0.0.1:4549/simple",
        }

    pypi_proxy_target = "https://oarepo.github.io/pypi/packages/simple"