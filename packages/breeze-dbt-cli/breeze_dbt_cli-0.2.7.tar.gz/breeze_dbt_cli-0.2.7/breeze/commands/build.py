# breeze/commands/build.py

import typer
from typing import List, Optional, Tuple
from breeze.models.model import create_empty_sql_file, generate_model_yml
from breeze.models.source import generate_source_yml

build_app = typer.Typer(
    help="""
Build commands to generate models, YAML files, and sources.

Use these commands to create .sql and YAML files for dbt 
models and sources. You can use custom templates or force 
updates to existing files.

Options:
  --help  Show this message and exit.

Commands:
  model   Generate .sql files for dbt models.
  yml     Generate YAML files for one or more dbt models.
  source  Generate YAML files for one or more sources in a schema.
"""
)

def process_items_for_generation(
    item_names: List[str],
    generate_function,
    **kwargs,
) -> Tuple[List[str], List[str], List[str]]:
    """
    Generic handler to process a list of items, generating corresponding files.
    
    Args:
    - item_names: List of item names to process (e.g., model names or source names).
    - generate_function: The function used to generate files for each item.
    - generate_args: Dictionary containing arguments to pass to the generation function.

    Returns:
    - Tuple of three lists: (success, skipped, failed).
    """
    success_items = []
    skipped_items = []
    failed_items = []

    for item_name in item_names:
        try:
            file_created = generate_function(item_name, **kwargs)
            if file_created:
                success_items.append(item_name)
            else:
                skipped_items.append(item_name)
        except Exception as e:
            typer.echo(f"❌ Failed to generate for '{item_name}': {e}")
            failed_items.append(item_name)

    return success_items, skipped_items, failed_items

def provide_summary_feedback(success: List[str], skipped: List[str], failed: List[str], entity_type: str):
    """
    Provide summary feedback for the results of file generation.
    
    Args:
    - success: List of items successfully processed.
    - skipped: List of items that were skipped.
    - failed: List of items that failed.
    - entity_type: The type of entity being processed (e.g., "SQL files", "YAML files").
    """
    if success:
        typer.echo(f"\n✅ Successfully created {entity_type} for: {', '.join(success)}")
    if skipped:
        typer.echo(f"\n{entity_type.capitalize()} skipped for: {', '.join(skipped)}. Use --force to overwrite.")
    if failed:
        typer.echo(f"\n❌ Failed to create {entity_type} for: {', '.join(failed)}")

@build_app.command()
def model(
    path: str = typer.Argument(..., help="The path where the model is created / located."),
    model_names: List[str] = typer.Argument(..., help="One or more model names to generate .sql files for."),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing files."),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Path to a custom SQL template."),
    no_subfolder: bool = typer.Option(False, "--no-subfolder", "-n", help="Store the .sql file directly in the specified path without a subfolder for each model."),

):
    """
    Generate SQL files for dbt models in the specified schema.

    This command will create a .sql file for each specified model. By default, files will get created in `models/path/model_name/model_name.sql.
    You can suppress the subfolder named after the model by using the flag `--no-subfolder` or `-n`.
    The SQL file will contain a default template with `ref()` and `source()` CTEs for referencing other models.

    If a file already exists, it will not be overwritten unless the `--force` option is used.

    You can use a custom template for the SQL file created by including the `--template` flag and passing the path of your template.

    Options:
      - `path`: Name of the folder where the models will be created.
      - `model_names`: One or more model names for which to generate .sql files.
      - `--force`, `-f`: Overwrite existing files.
      - `--template`, `-t`: Use a custom SQL template file.
      - `--no_subfolder`, `-n`: Store .sql file in models/folder_name.

    Examples:
      - Generate .sql files for `model1` and `model2` in `my_folder`:

        \b
        breeze build model my_folder model1 model2

      - Force overwrite existing .sql file for `model1`:

        \b
        breeze build model my_schema model1 --force

      - Use a custom SQL template for `model1`:

        \b
        breeze build model my_schema model1 --template path/to/custom_template.sql
    """

    success_models, skipped_models, failed_models = process_items_for_generation(
        model_names, create_empty_sql_file, path=path, force=force, template_path=template, no_subfolder=no_subfolder
    )

    provide_summary_feedback(success_models, skipped_models, failed_models, "SQL files")


@build_app.command()
def yml(
    model_names: List[str] = typer.Argument(..., help="One or more model names to generate YAML files for."),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing files."),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Path to a custom YAML template."),
):
    """
    Generate YAML files for one or more models.

    This command creates a YAML file for each specified model, containing metadata about the model and its columns.
    The generated YAML file will include column names, data types, and placeholders for adding tests.

    If the YAML file already exists, it will not be overwritten unless the `--force` option is used.

    You can use a custom template for the YAML file created by including the `--template` flag and passing the path of your template.

    Options:
      - `model_names`: One or more model names for which to generate YAML files.
      - `--force`, `-f`: Overwrite existing YAML files.
      - `--template`, `-t`: Use a custom YAML template file.

    Examples:
      - Generate YAML files for `model1` and `model2`:

        \b
        breeze build yml model1 model2

      - Force overwrite an existing YAML file for `model1`:

        \b
        breeze build yml model1 --force

      - Use a custom YAML template for `model1`:

        \b
        breeze build yml model1 --template path/to/custom_template.yml
    """

    success_models, skipped_models, failed_models = process_items_for_generation(
        model_names, generate_model_yml, force=force, template_path=template
    )

    provide_summary_feedback(success_models, skipped_models, failed_models, "YAML files")


@build_app.command()
def source(
    schema_name: str = typer.Argument(..., help="The schema of the source, and by default, the folder where source .yml will be created."),
    source_names: List[str] = typer.Argument(..., help="One or more source names to generate YAML files for."),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing files."),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Path to a custom YAML template."),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Custom path to store the source YAML files.")
):
    """
    Generate YAML files for one or more sources.

    This command creates a YAML file for each specified source, containing metadata about the source and its columns.
    The generated YAML file will include column names, data types, and placeholders for adding tests.

    If the YAML file already exists, it will not be overwritten unless the `--force` option is used.

    You can use a custom template for the YAML file created by including the `--template` flag and passing the path of your template.

    Options:
      - `schema_name`: The schema of the source, and by default, the folder where source .yml will be created..
      - `source_names`: One or more source names for which to generate YAML files.
      - `--force`, `-f`: Overwrite existing YAML files.
      - `--template`, `-t`: Use a custom YAML template file.
      - `--custom-path`, `-p`: Create the source YAML file in the custom-path.

    Examples:
      - Generate YAML files for `source1` and `source2` with schema `my_schema`:

        \b
        breeze build source my_schema source1 source2

      - Force overwrite an existing YAML file for `source1`:

        \b
        breeze build source my_schema source1 -f

      - Use a custom YAML template for `source1`:

        \b
        breeze build source my_schema source1 --template path/to/source_template.yml
    """

    success_sources, skipped_sources, failed_sources = process_items_for_generation(
        source_names, generate_source_yml, schema_name=schema_name, force=force, template_path=template, path=path
    )

    provide_summary_feedback(success_sources, skipped_sources, failed_sources, "YAML files for sources")
