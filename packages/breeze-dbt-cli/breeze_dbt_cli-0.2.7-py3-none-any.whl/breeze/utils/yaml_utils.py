# breeze/utils/yaml_utils.py

from typing import List, Optional
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq
import os

def load_yaml_file(file_path: str) -> dict:
    """
    Load the YAML file and return its content as a dictionary.
    
    Args:
    - file_path: The path of the YAML file to load.

    Returns:
    - A dictionary containing the contents of the YAML file.
    """
    yaml = YAML()
    try:
        with open(file_path, "r") as yml_file:
            return yaml.load(yml_file) or {}
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file or directory: '{file_path}'") from e


def write_yaml_file(file_path: str, data: dict) -> None:
    """
    Write the given data to a YAML file.
    
    Args:
    - file_path: The path of the YAML file to write to.
    - data: A dictionary containing the contents to write to the YAML file.
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(file_path, "w") as yml_file:
        yaml.dump(data, yml_file)

def find_yaml_path(entity_name: str, entity_type: str) -> Optional[str]:
    """
    Find the path to the YAML file for the given entity (model or source).
    
    Args:
    - entity_name: The name of the model or source to find.
    - entity_type: The type of entity to find ("model" or "source").
    
    Returns:
    - The path to the YAML file containing the entity, if found; otherwise, None.
    """
    for root, dirs, files in os.walk("models"):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                yml_path = os.path.join(root, file)
                with open(yml_path, "r") as yml_file:
                    yaml = YAML()
                    yml_data = yaml.load(yml_file)
                
                # Check for models or sources in the YAML data
                if entity_type == "model" and yml_data and "models" in yml_data:
                    for model in yml_data["models"]:
                        if model.get("name") == entity_name:
                            return yml_path
                elif entity_type == "source" and yml_data and "sources" in yml_data:
                    for source in yml_data["sources"]:
                        for table in source.get("tables", []):
                            if table.get("name") == entity_name:
                                return yml_path
    return None

def add_tests_to_yaml(
    yaml_entity: dict, test_names: List[str], columns: Optional[List[str]] = None
) -> bool:
    """
    Add one or more tests to a YAML entity (e.g., model or source).
    If columns are specified, the tests are added to those columns.
    If no columns are specified, the tests are added at the entity level.
    Returns True if changes were made, False otherwise.

    Args:
    - yaml_entity: The YAML entity to which tests will be added (e.g., model or source table).
    - test_names: A list of test names to add.
    - columns: An optional list of column names to add the tests to.

    Returns:
    - bool: True if changes were made, False otherwise.
    """
    changes_made = False

    if columns:
        # Ensure 'columns' key exists
        if "columns" not in yaml_entity or not yaml_entity["columns"]:
            yaml_entity["columns"] = []
        # Get existing columns
        existing_columns = {col["name"]: col for col in yaml_entity["columns"]}
        for col_name in columns:
            if col_name not in existing_columns:
                raise Exception(
                    f"Column '{col_name}' not found in entity '{yaml_entity.get('name', 'unknown')}'."
                )
            column = existing_columns[col_name]
            tests = column.get("tests")
            if tests is None:
                column["tests"] = CommentedSeq()
                tests = column["tests"]
            for test_name in test_names:
                if test_name not in tests:
                    tests.append(test_name)
                    changes_made = True
    else:
        # Add tests at the entity level
        tests = yaml_entity.get("tests")
        if tests is None:
            yaml_entity["tests"] = CommentedSeq()
            tests = yaml_entity["tests"]
        for test_name in test_names:
            if test_name not in tests:
                tests.append(test_name)
                changes_made = True

    return changes_made
