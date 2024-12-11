import dataclasses
import re
from typing import Set

from caseconverter import kebabcase, snakecase

from .enums import enum, enum_with_descriptions


@enum_with_descriptions
class ModelFeature:
    """
    Features of the repository model
    """

    files = enum("files", description="Files are used in the model")

    drafts = enum("drafts", description="Use drafts and published records")

    nr_vocabularies = enum(
        "nr_vocabularies",
        description="Use vocabularies from the Czech documents/data repository",
    )

    vocabularies = enum("vocabularies", description="Use plain invenio vocabularies")

    relations = enum("relations", description="Use relations to other models")

    tests = enum("tests", description="Generate basic tests for the model")

    custom_fields = enum(
        "custom_fields", description="Make the model extendable via custom fields"
    )

    requests = enum(
        "requests", description="Use requests for approving drafts and other actions"
    )

    communities = enum(
        "communities",
        description="Use communities for access control and other actions",
    )

    multilingual = enum(
        "multilingual",
        description="Use multilingual fields",
    )


@enum_with_descriptions
class BaseModel:
    """
    Base model to use for the repository.
    """

    empty = enum(
        "empty", description="Empty model, you will need to add all properties manually"
    )

    documents = enum(
        "documents", description="Model suitable for documents (such as articles, ...)"
    )

    data = enum(
        "data", description="Model suitable for data (such as datasets, images, ...)"
    )


@dataclasses.dataclass
class ModelConfig:
    prompts = {}
    options = {}

    base_model: BaseModel
    prompts["base_model"] = "Base model to use for the repository"

    model_name: str
    prompts["model_name"] = "Name of the model"

    model_description: str
    prompts["model_description"] = "Description of the model"

    model_package: str
    prompts["model_package"] = "Python package name of the model"

    api_prefix: str
    prompts["api_prefix"] = "API prefix for the model (will be api/<this value>)"

    pid_type: str
    prompts["pid_type"] = "PID type of the model. Must be up to 6 characters."

    features: Set[ModelFeature]
    prompts["features"] = "Model features"

    @classmethod
    def default_model_package(cls, config, values):
        return snakecase(values["model_name"])

    @classmethod
    def default_api_prefix(cls, config, values):
        return kebabcase(values["model_package"])

    @classmethod
    def default_pid_type(cls, config, values):
        pid_base = values["model_package"]
        pid_base = re.sub(r"[\s_-]", "", pid_base).lower()
        if len(pid_base) > 6:
            pid_base = re.sub(r"[AEIOU]", "", pid_base, flags=re.IGNORECASE)
        if len(pid_base) > 6:
            pid_base = pid_base[:3] + pid_base[len(pid_base) - 3 :]
        return pid_base

    @classmethod
    def default_features(cls, config, values):
        return {
            ModelFeature.nr_vocabularies,
            ModelFeature.tests,
            ModelFeature.custom_fields,
            ModelFeature.requests,
            ModelFeature.files,
            ModelFeature.drafts,
        }

    @property
    def model_config_file(self):
        return f"{self.model_name}.yaml"

    def after_user_input(self):
        if self.base_model == BaseModel.documents or self.base_model == BaseModel.data:
            self.features.add(ModelFeature.nr_vocabularies)

        if ModelFeature.nr_vocabularies in self.features:
            self.features.add(ModelFeature.vocabularies)

        if ModelFeature.vocabularies in self.features:
            self.features.add(ModelFeature.relations)

        if self.base_model == BaseModel.documents or self.base_model == BaseModel.data:
            self.features.update(ModelFeature)
            self.features.add(ModelFeature.multilingual)
