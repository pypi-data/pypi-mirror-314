import typer
import os
import shutil
from InquirerPy import inquirer
from pyrails.templates import settings_template, engine_template

app = typer.Typer()

def create_project_structure(base_path: str, folders: list):
    """
    Create the folder structure for the project and add __init__.py files.
    """
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        init_file = os.path.join(folder_path, "__init__.py")
        with open(init_file, "w") as file:
            file.write("")


def create_file(file_path: str, content: str = ""):
    """
    Create a file with specified content.
    """
    with open(file_path, "w") as file:
        file.write(content)


@app.command()
def new():
    """
    Initialize a new project with a specific structure and configuration.
    """
    # Gather project details
    project_name = inquirer.text(message="Enter project name:").execute()
    project_description = inquirer.text(message="Enter project description:").execute()
    default_slug = project_name.lower().replace(" ", "_")
    project_slug = inquirer.text(message=f"Enter project slug: ({default_slug})").execute() or default_slug
    project_version = inquirer.text(message="Enter project version:", default="0.1.0").execute()

    # Set project paths
    base_path = os.path.join("tmp", project_slug)
    project_path = os.path.join(base_path, project_slug)

    # Run Poetry to initialize the project
    typer.echo("Initializing Poetry project...")
    os.system(f"poetry new {base_path}")

    # Define folders to create
    folders_to_create = ["config", "db", "services", "schemas", "models", "routers"]

    # Create additional project folders
    create_project_structure(project_path, folders_to_create)

    # Create .env file
    create_file(os.path.join(base_path, ".env"), f"API_NAME={project_name}\n")

    # Add settings and database engine templates
    create_file(os.path.join(project_path, "config", "settings.py"), settings_template)
    create_file(os.path.join(project_path, "db", "engine.py"), engine_template.format(slug_name=project_slug))

    typer.echo(f"Project '{project_name}' created successfully!")


@app.command()
def remove(name: str):
    """
    Remove a project by its name.
    """
    slug = name.lower().replace(" ", "_")
    project_path = os.path.join("tmp", slug)

    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        typer.echo(f"Project '{name}' removed successfully!")
    else:
        typer.echo(f"Project '{name}' does not exist.")


if __name__ == "__main__":
    app()
