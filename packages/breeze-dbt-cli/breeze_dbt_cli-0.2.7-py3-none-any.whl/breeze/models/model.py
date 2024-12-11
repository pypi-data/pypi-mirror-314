# breeze/models/model.py

import os
from breeze.utils.db_utils import get_columns_from_database
from breeze.utils.yaml_utils import load_yaml_file, write_yaml_file, find_yaml_path, add_tests_to_yaml
from breeze.utils.template_utils import get_template_content
from breeze.utils.dbt_utils import load_manifest, find_model_in_manifest
from typing import Optional, List
from jinja2 import Template
import typer
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq

def create_empty_sql_file(
    model_name: str,
    path: str,
    force: bool = False,
    template_path: Optional[str] = None,
    no_subfolder: bool = False
) -> bool:
    """
    Create an SQL file for the specified model in the correct directory,
    populated with a default SELECT template or a custom template.
    Returns True if the file was created or overwritten, False if it was skipped.
    """
    # Define the directory and SQL file path
    if no_subfolder:
        model_dir = os.path.join("models", path)
        sql_path = os.path.join(model_dir, f"{model_name}.sql")
    else:
        model_dir = os.path.join("models", path, model_name)
        os.makedirs(model_dir, exist_ok=True)
        sql_path = os.path.join(model_dir, f"{model_name}.sql")

    # Get the template content using the new utility function
    try:
        select_template = get_template_content("default_model_template.sql", custom_template_path=template_path)
    except FileNotFoundError as e:
        typer.echo(f"❌ {e}")
        return False

    # Check if the SQL file already exists
    if os.path.exists(sql_path) and not force:
        typer.echo(f"SQL file for '{model_name}' model already exists at '{sql_path}'. Skipping creation.")
        return False

    # Create or overwrite the SQL file with the template
    with open(sql_path, "w") as sql_file:
        sql_file.write(select_template)

    if force and os.path.exists(sql_path):
        typer.echo(f"♻️  SQL file for '{model_name}' model at '{sql_path}' has been overwritten.")
    else:
        typer.echo(f"✅  SQL file for '{model_name}' model created at '{sql_path}'")

    return True


def generate_model_yml(
    model_name: str, force: bool = False, template_path: Optional[str] = None
) -> bool:
    """
    Generate or update model YAML files, including data_type for each column.
    Returns True if the file was created, False if it already existed.
    """
    # Load the manifest file using the utility function
    manifest = load_manifest()

    # Find the model in the manifest using the utility function
    model = find_model_in_manifest(manifest, model_name)

    # Extract folder_name from the model's original file path
    original_file_path = model["original_file_path"]
    model_dir = os.path.dirname(original_file_path)

    yml_path = os.path.join(model_dir, f"{model_name}.yml")

    # Check if the YML file already exists
    if os.path.exists(yml_path) and not force:
        typer.echo(f"YML file for model '{model_name}' already exists at '{yml_path}'. Skipping creation.")
        return False

    # Prepare columns data
    columns = get_columns_from_database(
        model["database"], model["schema"], model.get("alias") or model["name"]
    )
    if not columns:
        raise Exception(
            f"Error: Table '{model.get('alias') or model['name']}' was not found in schema '{model['schema']}' of database '{model['database']}'."
        )
    columns_data = [
        {"name": col_name, "data_type": data_type} for col_name, data_type in columns
    ]

    # Get the template content from template_utils
    try:
        template_content = get_template_content("default_model_template.yml", custom_template_path=template_path)
    except FileNotFoundError as e:
        raise Exception(f"❌ {e}")

    # Create a Jinja2 template with whitespace control
    jinja_template = Template(
        template_content, trim_blocks=True, lstrip_blocks=True
    )
    # Render the template with context variables
    content = jinja_template.render(
        model_name=model_name, schema_name=model["schema"], columns=columns_data
    )

    # Write content to the YML file
    with open(yml_path, "w") as yml_file:
        yml_file.write(content)

    if force and os.path.exists(yml_path):
        typer.echo(f"♻️  Model YML file for model '{model_name}' at '{yml_path}' has been overwritten.")
    else:
        typer.echo(f"✅  Model YML file for model '{model_name}' created at '{yml_path}'")
    return True


def add_test_to_model(
    test_names: List[str], model_name: str, columns: Optional[List[str]] = None
) -> bool:
    """
    Add one or more tests to a model YAML file.
    If columns are specified, the tests are added to those columns.
    If no columns are specified, the tests are added at the model level.
    Returns True if changes were made, False otherwise.
    """
    # Locate the YAML file for the model
    yml_path = find_yaml_path(model_name, "model")
    if not yml_path:
        raise Exception(f"YAML file for model '{model_name}' not found.")

    # Load the YAML file using the utility function
    yml_data = load_yaml_file(yml_path)

    models = yml_data.get("models", [])
    if not models:
        raise Exception(f"No models found in YAML file '{yml_path}'.")

    # Find the model in the YAML
    model = next((m for m in models if m.get("name") == model_name), None)
    if model is None:
        raise Exception(f"Model '{model_name}' not found in YAML file '{yml_path}'.")

    # Use the utility function to add tests
    changes_made = add_tests_to_yaml(model, test_names, columns)

    if changes_made:
        # Write back the YAML file using the utility function
        write_yaml_file(yml_path, yml_data)
        return True
    else:
        return False
