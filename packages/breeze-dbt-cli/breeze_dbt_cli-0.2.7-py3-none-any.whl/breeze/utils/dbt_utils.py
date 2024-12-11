# breeze/utils/dbt_utils.py

import os
import json
import yaml

def load_manifest() -> dict:
    """
    Load the dbt manifest.json file and return its contents as a dictionary.
    Raises an exception if the manifest file is not found.
    """
    manifest_path = os.path.join("target", "manifest.json")

    if not os.path.exists(manifest_path):
        raise Exception(
            "manifest.json not found. Please run 'dbt compile' or 'dbt build' first."
        )

    # Load the manifest file
    with open(manifest_path, "r") as manifest_file:
        manifest = json.load(manifest_file)
    
    return manifest

def find_model_in_manifest(manifest: dict, model_name: str) -> dict:
    """
    Find a model in the manifest by its name and return its metadata.
    Raises an exception if the model is not found.
    """
    if not manifest or "nodes" not in manifest:
        raise Exception("Manifest is empty or does not contain 'nodes'.")
    
    model_unique_id = None
    for node_id, node in manifest["nodes"].items():
        if node["resource_type"] == "model" and node["name"] == model_name:
            model_unique_id = node_id
            break

    if not model_unique_id:
        raise Exception(f"Model '{model_name}' not found in manifest.")

    return manifest["nodes"][model_unique_id]


def get_profile() -> dict:
    """
    Retrieve the dbt profiles.yml configuration.
    """
    home_dir = os.path.expanduser("~")
    profiles_path = os.path.join(home_dir, ".dbt", "profiles.yml")

    if not os.path.exists(profiles_path):
        raise Exception(
            "\u274c profiles.yml not found. Please place the profiles.yml file in ~/.dbt/."
        )

    with open(profiles_path, "r") as profiles_file:
        profiles = yaml.safe_load(profiles_file) or {}

    return profiles

def get_profile_name_from_dbt_project() -> str:
    """
    Retrieve the profile name from dbt_project.yml.
    """
    dbt_project_path = os.path.join(os.getcwd(), "dbt_project.yml")

    if not os.path.exists(dbt_project_path):
        raise Exception(
            "\u274c dbt_project.yml not found. Please ensure you're in a dbt project directory."
        )
    with open(dbt_project_path, "r") as dbt_project_file:
        dbt_project = yaml.safe_load(dbt_project_file)

    profile_name = dbt_project.get("profile") if dbt_project else None

    if not profile_name:
        raise Exception("\u274c Profile name not found in dbt_project.yml.")
    return profile_name

def get_target_from_profile(profile: dict, profile_name: str) -> dict:
    profile_data = profile.get(profile_name)
    if not profile_data:
        raise Exception(f"\u274c Profile '{profile_name}' not found in profiles.yml.")

    # Ensure that a target is defined in the profile
    target_name = profile_data.get("target")
    if not target_name or target_name is None:
        raise Exception(f"\u274c No target defined in profile '{profile_name}'.")

    if target_name not in profile_data["outputs"]:
        raise Exception(
            f"\u274c Target '{target_name}' not found in profile '{profile_name}'."
        )

    target = profile_data["outputs"][target_name]
    return target
