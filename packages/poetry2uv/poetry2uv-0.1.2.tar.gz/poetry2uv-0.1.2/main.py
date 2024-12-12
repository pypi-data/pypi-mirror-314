import toml
from poetry.core.packages.dependency import Dependency


def transform_poetry_to_project(pyproject_toml_path, output_toml_path):
    # Load the pyproject.toml file
    with open(pyproject_toml_path, "r") as file:
        pyproject_data = toml.load(file)

    # Extract the `[tool.poetry]` section
    poetry_section = pyproject_data.get("tool", {}).get("poetry", {})

    if not poetry_section:
        raise ValueError(
            "No [tool.poetry] section found in pyproject.toml. Are you sure this is a Poetry project?"
        )

    # Create a new "project" section
    project_section = {}

    # Map basic metadata fields
    metadata_mapping = {
        "name": "name",
        "version": "version",
        "description": "description",
        "readme": "readme",
    }

    for poetry_key, project_key in metadata_mapping.items():
        if poetry_key in poetry_section:
            project_section[project_key] = poetry_section[poetry_key]

    # Convert `license` to `{ text = "VALUE" }` format
    if "license" in poetry_section:
        project_section["license"] = {"text": poetry_section["license"]}

    # Convert authors to PEP 621 format
    if "authors" in poetry_section:
        project_section["authors"] = [
            {
                "name": author.split("<")[0].strip(),
                "email": author.split("<")[1].strip(" >"),
            }
            if "<" in author
            else {"name": author}
            for author in poetry_section["authors"]
        ]

    # Handle the Python version specifier
    dependencies = poetry_section.get("dependencies", {})
    if "python" in dependencies:
        project_section["requires-python"] = convert_python_version(
            dependencies["python"]
        )
        del dependencies["python"]

    # Handle runtime `dependencies` in PEP 508 format
    project_section["dependencies"] = []
    for dep, version in dependencies.items():
        dep_string = convert_to_pep508(dep, version)
        project_section["dependencies"].append(dep_string)

    # Handle development dependencies in PEP 508 format
    dev_dependencies = poetry_section.get("dev-dependencies", {})
    project_section["optional-dependencies"] = {"dev": []}
    for dep, version in dev_dependencies.items():
        dep_string = convert_to_pep508(dep, version)
        project_section["optional-dependencies"]["dev"].append(dep_string)

    # Rewrite the `pyproject.toml` data
    pyproject_data["project"] = project_section

    # Remove the old `[tool.poetry]` section
    if "tool" in pyproject_data and "poetry" in pyproject_data["tool"]:
        del pyproject_data["tool"]["poetry"]
        # Remove the `tool` section if it's now empty
        if not pyproject_data["tool"]:
            del pyproject_data["tool"]

    # Save the transformed `pyproject.toml`
    with open(output_toml_path, "w") as file:
        toml.dump(pyproject_data, file)

    print(f"Transformed pyproject.toml saved to {output_toml_path}")


def convert_python_version(poetry_version):
    """
    Convert a version specifier (e.g., ^3.8) into a PEP 621-compatible `requires-python` field.
    """
    if poetry_version.startswith("^"):
        # ^3.8 becomes >= 3.8, < 4.0
        base_version = poetry_version[1:]
        major, minor, *_ = base_version.split(".")
        upper_version = f"< {int(major) + 1}.0"
        return f">= {base_version}, {upper_version}"
    elif poetry_version.startswith("~"):
        # ~3.8 becomes >= 3.8, < 3.9
        base_version = poetry_version[1:]
        major, minor, *_ = base_version.split(".")
        upper_version = f"< {major}.{int(minor) + 1}"
        return f">= {base_version}, {upper_version}"
    else:
        # Pass through exact or already valid specifiers
        return poetry_version


def convert_to_pep508(dep_name, dep_spec):
    """
    Convert a dependency to its PEP 508-compliant representation using Poetry's `Dependency` class.
    """
    if isinstance(dep_spec, str):
        # Handle simple version specifier (e.g., "^1.2.3")
        dependency = Dependency(dep_name, dep_spec)
    elif isinstance(dep_spec, dict):
        # For more complex cases, pass additional data to Dependency class
        version = dep_spec.get("version", "*")
        optional = dep_spec.get("optional", False)
        python = dep_spec.get("python", None)
        markers = dep_spec.get("markers", None)

        # Create a Dependency object
        dependency = Dependency(dep_name, version)
        if optional:
            dependency.marker = f'extra == "{dep_name}"'
        if python:
            dependency.python_constraint = python
        if markers:
            dependency.marker = markers
    else:
        raise ValueError(f"Unsupported dependency format: {dep_spec}")

    # Return the dependency in PEP 508 format
    return dependency.to_pep_508()


def main():
    transform_poetry_to_project("pyproject.toml", "pyproject_transformed.toml")


# Example Usage
if __name__ == "__main__":
    main()
