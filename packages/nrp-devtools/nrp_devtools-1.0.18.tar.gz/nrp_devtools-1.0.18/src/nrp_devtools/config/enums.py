from enum import Enum


def enum(value, *, description):
    return (value, description)


def enum_with_descriptions(clz) -> Enum:
    clz_name = clz.__name__
    descriptions = {}
    new_class_members = {}
    for name, value in clz.__dict__.items():
        if isinstance(value, tuple):
            new_class_members[name] = value[0]
            descriptions[name] = value[1]
    ret = Enum(clz_name, new_class_members)
    for name, desc in descriptions.items():
        getattr(ret, name).description = desc
    return ret
