"""Interactive utilities for the KIE notebook"""
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type, Union, cast, get_args, get_origin

import yaml
from IPython.display import clear_output, display
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from rich.prompt import Prompt

from databricks.kie.kie_schema import ModelManager, dict_to_model, model_to_dict

if TYPE_CHECKING:
    from ipywidgets import Textarea


def walkthrough_descriptions(model: Type[BaseModel],
                             current_path: Optional[str] = None,
                             current_outputs: Optional[List[str]] = None):
    """
    Interactively add descriptions to fields of an existing Pydantic model.
    Returns a new model with the added descriptions.
    """
    editor = ModelManager(model)
    model_name = editor.model.__name__

    def format_field(name: str, field: FieldInfo, prefix: str = "", with_description: bool = True) -> str:
        formatted = f"{prefix}{name} ({field.annotation.__name__})"
        if with_description and field.description:
            formatted = ": ".join([formatted, field.description])
        return formatted

    def get_full_path(name: str, current_path: Optional[str] = None) -> str:
        if not current_path:
            return name
        return " → ".join([current_path, name])

    current_outputs = current_outputs or []

    def refresh_display():
        clear_output(wait=True)
        for l in current_outputs:
            print(l)

    if not current_path:
        current_outputs.append(f"Adding descriptions for {model_name} fields:")
        current_outputs.append("(Press Enter to skip a field or keep existing description)\n")

    refresh_display()

    # Gather descriptions for each field
    for field_name, field in editor.model.model_fields.items():
        prompt = format_field(f"[bold]{get_full_path(field_name, current_path)}[/]", field, " > ", False)
        desc = Prompt.ask(prompt, default=field.description)
        #desc = input(prompt)
        # Clear the input line
        if desc and desc.strip():
            editor.edit_descriptions(**{field_name: desc.strip()})

        # Display the progress
        current_outputs.append(
            format_field(
                name=f"\033[1m{get_full_path(field_name, current_path)}\033[0m",  # Bold the name with ANSI
                field=editor.model.model_fields[field_name],  # Get the updated field
                prefix=" ✔ ",  # Prefix as completed
                with_description=True,
            ))

        refresh_display()

        # If the field is another BaseModel, recurse into it
        type_ = field.annotation
        make_optional = False
        if get_origin(type_) is Union:  # This is an optional field, strip the optional
            make_optional = True
            type_ = [t for t in get_args(type_) if t is not None][0]

        # This is an array, check the first item
        if get_origin(type_) is list:
            args = get_args(type_)
            if isinstance(args[0], type) and issubclass(args[0], BaseModel):
                # This is an array of models
                type_ = walkthrough_descriptions(args[0], field_name, current_outputs)
                type_ = List[type_]
        elif isinstance(type_, type) and issubclass(type_, BaseModel):
            # This is a nested model
            type_ = walkthrough_descriptions(type_, field_name, current_outputs)

        if make_optional:
            type_ = Optional[type_]
        editor.edit_types(**{field_name: type_})

    return editor.model


def show_schema_editor(output_schema: Type[BaseModel]) -> 'Textarea':
    """Show a YAML-based editor to quickly edit your desired output schema. 
    
    The editor updates automatically, so you don't have to confirm your outputs.
    When you are done, run:
    ```
    # handle = show_schema_editor(output_schema)
    
    output_schema = update_schema_from_handle(handle)
    ```
    """
    from ipywidgets import Textarea  # pylint: disable=import-outside-toplevel

    initial = cast(str, yaml.dump(model_to_dict(output_schema)))
    w = Textarea(value=initial,
                 description="Extract:",
                 layout={
                     "height": f"{len(initial.splitlines()) * 1.3}em",
                     "width": "100%"
                 },
                 disabled=False)
    display(w)
    return w


def update_schema_from_handle(handle: 'Textarea', existing_schema: Type[BaseModel]) -> Tuple[Type[BaseModel], bool]:
    """Update your output schema using the YAML stored in the text box referenced by `handle`. 
    
    Returns a tuple of the new schema + a boolean stating if the schema has changedd
    
    `handle` should be created by first calling:
    ```
    handle = show_schema_editor(output_schema)
    ```
    """
    existing_str = yaml.dump(model_to_dict(existing_schema))
    has_changed = existing_str != handle.value

    try:
        schema_yaml = yaml.safe_load(handle.value)
    except Exception as e:
        raise ValueError("Could not decode YAML of schema. Double check the text box or try running it again") from e
    if schema_yaml is None:
        raise ValueError("Text box is empty! Try running it again")
    schema_yaml = cast(Dict[str, Any], schema_yaml)
    return dict_to_model(schema_yaml), has_changed


def check_schema_has_descriptions(schema: Type[BaseModel]) -> bool:
    # Check the first few descriptions - this doesn't need to be exhaustive
    count = 0
    for _, field in schema.model_fields.items():
        if not field.description:
            return False
        count += 1
        if count >= 5:
            break
    return True
