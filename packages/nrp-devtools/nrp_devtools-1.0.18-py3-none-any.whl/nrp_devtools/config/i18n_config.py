import dataclasses
from typing import List


@dataclasses.dataclass
class I18NConfig:
    """
    Configuration for internationalization.
    """

    prompts = {}
    options = {}

    babel_input_translations: List[str] = dataclasses.field(default_factory=list)
    babel_output_translations: str = "i18n/translations"
    babel_source_paths: List[str] = dataclasses.field(default_factory=list)
    i18next_input_translations: List[str] = dataclasses.field(default_factory=list)
    i18next_output_translations: str = "i18n/semantic-ui/translations"
    i18next_source_paths: List[str] = dataclasses.field(default_factory=list)
    languages: List[str] = dataclasses.field(default_factory=lambda: ["en"])
