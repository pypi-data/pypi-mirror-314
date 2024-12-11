import yaml

from nrp_devtools.config import OARepoConfig
from nrp_devtools.config.model_config import BaseModel, ModelConfig, ModelFeature


def create_model(config: OARepoConfig, *, model_name):
    model: ModelConfig = config.get_model(model_name)

    profiles = ["record"]
    profile_specific = {}

    plugins = {
        "oarepo-model-builder-ui",
    }
    permission_presets = ["authenticated"]
    extra_includes = []
    runtime_dependencies = {}
    settings = {}

    if ModelFeature.drafts in model.features:
        profiles.append("draft")
        profile_specific["draft"] = {}
        plugins.add("oarepo-model-builder-drafts")

    if ModelFeature.files in model.features:
        profiles.append("files")
        plugins.add("oarepo-model-builder-files")
        if ModelFeature.drafts in model.features:
            profiles.append("draft_files")
            profile_specific["draft-files"] = {}
            plugins.add("oarepo-model-builder-drafts-files")

    if ModelFeature.communities in model.features:
        permission_presets = ["communities"]

    if ModelFeature.requests in model.features:
        extra_includes.append(f"./{model.model_name}-requests.yaml")
        plugins.add("oarepo-model-builder-requests")

    if ModelFeature.custom_fields in model.features:
        extra_includes.append(f"./{model.model_name}-custom_fields.yaml")
        plugins.add("oarepo-model-builder-cf")

    if ModelFeature.files in model.features:
        profile_specific["files"] = {
            "use": ["invenio_files"],
            "properties": {"use": [f"./{model.model_name}-files.yaml"]},
        }

    if ModelFeature.vocabularies in model.features:
        plugins.add("oarepo-model-builder-vocabularies")
        runtime_dependencies["nr-vocabularies"] = "2.0.0"

    if ModelFeature.relations in model.features:
        plugins.add("oarepo-model-builder-relations")

    if ModelFeature.nr_vocabularies in model.features:
        runtime_dependencies["nr-vocabularies"] = "2.0.8"

    settings["i18n-languages"] = ["en"]

    if ModelFeature.multilingual in model.features:
        plugins.add("oarepo-model-builder-multilingual")
        settings.update(
            {
                "supported-langs": {
                    "en": {"text": {}},
                },
            }
        )

    if model.base_model == BaseModel.data:
        extend = {
            "extend": "nr-data#DataModel",
        }
        plugins.add("oarepo-model-builder-nr")
        runtime_dependencies["nr-metadata"] = "2.0.0"
    elif model.base_model == BaseModel.documents:
        extend = {
            "extend": "nr-documents#DocumentModel",
        }
        plugins.add("oarepo-model-builder-nr")
        runtime_dependencies["nr-metadata"] = "2.0.0"
    elif model.base_model == BaseModel.empty:
        extend = {}
    else:
        raise ValueError(f"Unknown base model: {model.base_model}")

    model_schema = {
        "profiles": profiles,
        "record": {
            "module": {"qualified": model.model_package},
            **extend,
            "permissions": {"presets": permission_presets},
            "pid": {"type": model.pid_type},
            "properties": {"metadata": {"properties": {}}},
            "resource-config": {"base-html-url": f"/{model.api_prefix}/"},
            **profile_specific,
            "use": ["invenio", *extra_includes],
        },
        "plugins": {
            "builder": {
                "disable": [
                    "script_sample_data",
                    "invenio_record_metadata_alembic_setup_cfg",
                ]
            },
            "packages": list(plugins),
        },
        "runtime-dependencies": runtime_dependencies,
        "settings": settings,
    }

    save_schema(config.models_dir / model.model_config_file, model_schema)

    if ModelFeature.files in model.features:
        save_schema(
            config.models_dir / f"{model.model_name}-files.yaml",
            {"caption": {"type": "keyword"}},
        )

    if ModelFeature.requests in model.features:
        save_schema(
            config.models_dir / f"{model.model_name}-requests.yaml",
            {
                "draft": {
                    "requests": {
                        "types": {
                            "publish-draft": {
                                "base-classes": [
                                    "oarepo_requests.types.publish_draft.PublishDraftRequestType"
                                ],
                                "allowed-receiver-ref-types": ["user", "group"],
                            }
                        }
                    }
                },
                "requests": {
                    "types": {
                        "delete-record": {
                            "base-classes": [
                                "oarepo_requests.types.delete_record.DeleteRecordRequestType"
                            ],
                            "allowed-receiver-ref-types": ["user", "group"],
                        },
                        "edit-record": {
                            "base-classes": [
                                "oarepo_requests.types.edit_record.EditRecordRequestType"
                            ],
                            "allowed-receiver-ref-types": ["user", "group"],
                        },
                    },
                },
            },
        )

    if ModelFeature.custom_fields in model.features:
        save_schema(
            config.models_dir / f"{model.model_name}-custom_fields.yaml",
            {"custom-fields": []},
        )


def save_schema(file, schema):
    with open(file, "w") as f:
        yaml.dump(schema, f)
