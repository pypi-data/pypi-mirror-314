import dataclasses
import typing
from enum import Enum

import click
from dacite import from_dict

from nrp_devtools.config import OARepoConfig
from nrp_devtools.config.config import serialization_config


def ask_for_configuration(config: OARepoConfig, config_class, initial_values=None):
    """
    Ask for configuration interactively.
    """
    values = initial_values or {}
    prompts = config_class.prompts
    for field in dataclasses.fields(config_class):
        if field.name not in prompts:
            continue

        if field.name in values:
            value = values[field.name]
        elif hasattr(config_class, "default_" + field.name):
            value = getattr(config_class, "default_" + field.name)(config, values)
        elif not isinstance(field.default, dataclasses._MISSING_TYPE):
            value = field.default or ""
        else:
            value = ""

        if typing.get_origin(field.type) == set:
            # set of enums
            value = prompt_set_choices(
                typing.get_args(field.type)[0], prompts[field.name], default=value
            )
        elif issubclass(field.type, Enum):
            value = prompt_choices(field.type, prompts[field.name], default=value)
        else:
            value = click.prompt(prompts[field.name], default=value)

        values[field.name] = value

    ret = from_dict(config_class, values, serialization_config)

    if hasattr(ret, "after_user_input"):
        ret.after_user_input()

    return ret


def prompt_choices(enum, prompt, default=None):
    """
    Prompt user to choose from enum values.
    """
    print(prompt)

    choices = {str(idx + 1): e for idx, e in enumerate(enum)}

    for idx, c in choices.items():
        print(f"{idx:5s} {c.description}")

    if default:
        for idx, c in choices.items():
            if c.value == default:
                default = idx
                break
        else:
            default = None

    return choices[
        click.prompt(
            "Your choice",
            type=click.Choice(choices.keys()),
            default=default,
        )
    ].value


def prompt_set_choices(enum, prompt, default=None):
    """
    Prompt user to choose from enum values.
    """
    print(prompt)

    choices = {chr(ord("A") + idx): e for idx, e in enumerate(enum)}

    value = set(default or {})

    while True:
        for idx, c in choices.items():
            if c in value:
                tick = "[x]"
            else:
                tick = "[ ]"
            print(f"{idx:5s} {tick} {c.description}")

        inp = click.prompt(
            "Enter char(s) to toggle, c to continue",
            default="",
        )
        if inp == "c":
            break
        else:
            for cc in inp:
                if cc not in choices:
                    continue
                value ^= {choices[cc]}

    return value
