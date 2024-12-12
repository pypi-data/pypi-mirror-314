from contextlib import suppress
import importlib.metadata
from pathlib import Path
import toml
def extract_pyproject_info(pytoml_file: Path, keyword) -> str:
    """Returns the version, license, GitHub URL, author, or description information
    from the nearby pyproject.toml file."""
    with suppress(FileNotFoundError):
        with open((root_dir := pytoml_file) / "pyproject.toml",
                  encoding="utf-8") as pyproject_toml:
            pyproject_data = toml.load(pyproject_toml)

            # Extract version
            if keyword == "version":
                version = pyproject_data.get("project", {}).get("version", None)
                if version:
                    return f"{version}-dev"

            # Extract license
            elif keyword == "license":
                classifiers = pyproject_data.get("project", {}).get("classifiers", [])
                license_classifier = next((c for c in classifiers if c.startswith("License :: OSI Approved")), None)
                if license_classifier:
                    return license_classifier.split("::")[-1].strip()

            # Extract GitHub URL
            elif keyword == "url":
                urls = pyproject_data.get("project", {}).get("urls", {})
                homepage = urls.get("Homepage", None)
                if homepage:
                    return homepage

            # Extract author
            elif keyword == "author":
                authors = pyproject_data.get("project", {}).get("authors", [])
                if authors:
                    return ', '.join(
                        f"{author.get('name', 'Unknown')}" for author in authors)

            # Extract description
            elif keyword == "description":
                description = pyproject_data.get("project", {}).get("description", None)
                if description:
                    return description
            
            elif keyword == "name":
                name = pyproject_data.get("project", {}).get("name", None)
                if name:
                    return name

    return importlib.metadata.version(__package__ or __name__.split(".", maxsplit=1)[0])

