import re

import tomli
import tomli_w


class PyProject:
    def __init__(self, path):
        self.pyproject_file = path
        with open(self.pyproject_file, "rb") as f:
            self.pyproject_data = tomli.load(f)

    def save(self):
        with open(self.pyproject_file, "wb") as f:
            tomli_w.dump(self.pyproject_data, f)

    def add_dependencies(self, *dependencies):
        self.update_dependencies_array(
            self.pyproject_data["project"].setdefault("dependencies", []), dependencies
        )
        return self

    def add_optional_dependencies(self, group, *dependencies):
        self.update_dependencies_array(
            self.pyproject_data["project"]
            .setdefault("optional-dependencies", {})
            .setdefault(group, []),
            dependencies,
        )
        return self

    def add_entry_point(self, group, name, value):
        toml_entry_points = self.pyproject_data["project"].setdefault(
            "entry-points", {}
        )

        ep_group = toml_entry_points.setdefault(group, {})
        ep_group[name] = value
        return self

    def update_dependencies_array(self, target_array, new_values):
        target_packages = [re.split("[<>=]", ta)[0] for ta in target_array]
        for value in new_values:
            if not value:
                continue
            value_package = re.split("[<>=]", value)[0]
            if value_package not in target_packages:
                target_array.append(value)
        target_array.sort()
        return target_array
