from __future__ import annotations

from typing import get_args, get_origin

from pydantic.alias_generators import to_camel, to_pascal, to_snake

from vbl_aquarium.models import unity
from vbl_aquarium.utils.common import get_classes

p2c_types = {
    "str": "string",
}

unity_class_names = [x.__name__ for x in get_classes(unity)]


def generate_csharp_struct(class_name: str, fields: list[str], enums=None, has_unity_classes=False):
    # build using statements
    usings = ""
    # if enums is not None:
    #     usings += 'using System;\nusing UnityEngine;'
    # else:
    if has_unity_classes:
        usings += "using UnityEngine;"

    # build field declarations
    field_declarations = "\n".join(f"    public {field};" for field in fields)
    constructor_arg = ", ".join(f"{field.split(' ')[0]} {to_camel(to_snake(field.split(' ')[1]))}" for field in fields)
    constructor_assignments = "\n        ".join(
        f"{field.split(' ')[1]} = {to_camel(to_snake(field.split(' ')[1]))};" for field in fields
    )

    # build enum str
    enum_str = ""
    if enums is not None:
        enum_array = "\n".join(f"    {v[0]} = {v[1]}," for v in enums[1])
        enum_str = f"""
\n\npublic enum {enums[0]}
{{
{enum_array}
}}
"""

    # build the full class file string
    return f"""
{usings}
[Serializable]
public struct {class_name}
{{
{field_declarations}

    public {class_name}({constructor_arg})
    {{
        {constructor_assignments}
    }}
}}{enum_str}
"""


def pydantic_to_csharp(pydantic_class, class_json):
    class_name = pydantic_class.__name__

    fields = []

    enums = None  # when enums are active this should be a tuple (ClassName, [(Option1, Value1), (Option2, Value2)])

    has_unity_classes = False

    for name, data in pydantic_class.model_fields.items():
        field_data = ""

        # first, catch enums
        if "enum" in str(data.annotation):
            # get the name of the enum
            enum_name = data.annotation.__name__
            # pull the defs and properties from the json
            enum_values = class_json["$defs"][enum_name]["enum"]
            enum_keys = class_json["properties"][to_pascal(name)]["enum_keys"]
            # Bind the keys and values together
            data_list = zip(enum_keys, enum_values)
            enums = (enum_name, data_list)
            field_data = f"{enum_name} {alias if (alias := data.alias) else name}"

        if "bytearray" in str(data.annotation):
            field_data = f"byte[] {alias if (alias := data.alias) else name}"

        # finally, deal with arrays
        elif get_origin(data.annotation) == list:
            arg_class = get_args(data.annotation)
            type_name = arg_class[0].__name__

            # convert str -> string properly
            if type_name in p2c_types:
                type_name = p2c_types[type_name]

            if hasattr(arg_class[0], "__name__"):
                field_data = f"{type_name}[] {alias if (alias := data.alias) else name}"
            else:
                print(arg_class[0])

        # next, deal with base classes
        elif hasattr(data.annotation, "__name__"):
            # convert str -> string properly
            type_name = data.annotation.__name__
            if type_name in p2c_types:
                type_name = p2c_types[type_name]

            field_data = f"{type_name} {alias if (alias := data.alias) else name}"

        else:
            raise Exception("need to write a new parser for a missing type")

        if not has_unity_classes:
            for uc in unity_class_names:
                if uc in field_data:
                    has_unity_classes = True
                    break

        fields.append(field_data)

    return generate_csharp_struct(class_name, fields, enums, has_unity_classes)
