import click
import os
import subprocess
import shutil

import click.shell_completion

SUCCESS = 'green'
WARNING = 'yellow'
ERROR = 'red'

def create_folder(project_name: str, directory: str):
    try:
        click.echo(f"Creating folder for project {project_name}...")
        os.mkdir(directory)
    except OSError as oserr:
        click.echo(f"Error when creating new project folder -> {oserr}")
    except Exception as e:
        click.echo(e, err=True, color=True)
    else:
        click.echo(f"Folder for project {project_name} was created successfully with route {directory.replace('\\','/')}")

def initialize_git(directory: str):
    if not os.path.isdir(directory):
        click.secho(f"No directory named {directory} was found. Git repository was not initialized", fg=WARNING)
        return
    os.chdir(directory)
    try:
        subprocess.call(('git','init'))
    except Exception as e:
        click.secho(f"Error when initializing git repository -> {e}", fg=ERROR)
    else:
        click.secho(f"Git repository initialized successfully in directory {directory}", fg=SUCCESS)

def create_gitignore(directory: str):
    """Copies the gitignore file in this working dir to the newly created project directory

    Args:
        directory (str): The directory to which the .gitignore file will be copied to
    """
    if not os.path.isdir(directory):
        click.secho(f"No directory named {directory} was found. .gitignore file was not copied to project folder", fg=WARNING)
        return   
    click.echo(f"Copying gitignore file to {directory} directory...")
    try:
        shutil.copy2(f'{os.path.dirname(__file__)}/.gitignore',directory)
    except Exception as e:
        click.secho(f"Error when copying gitignore file to destination folder -> {e}", fg=ERROR)
    else:
        click.secho(f"Gitignore file successfully copied to directory {directory}", fg=SUCCESS)

def create_virtual_environment(path: str):
    try:
        click.echo("Creating virtual environment...")
        subprocess.call(('python','-m','venv','.venv'), cwd=path)
    except Exception as e:
        click.echo(e, err=True)
    else:
        click.secho(f"Virtual environment created successfully in path {path}", fg=SUCCESS)

def open_project_vscode(directory: str):
    if not os.path.isdir(directory):
        click.secho(f"No directory named {directory} was found. Project creation failed. Please check previous steps to see errors.", fg=ERROR)
        return
    try:
        subprocess.call(('code',directory), cwd=directory)
    except Exception as e:
        click.secho(f"Error when opening in vscode -> {e}", fg=ERROR)
    else:
        click.secho("Successfully opened project in VS Code", fg=SUCCESS)

@click.command()
@click.argument("name")
@click.option('--directory', help="Directory in which the project will be created. Defaults to current directory")
@click.option('--no-git', is_flag=True, flag_value='True/False', help="Skips git initialization when creating the project folder. It won't add any .gitignore-like file")
@click.option('--open-vscode', is_flag=True, flag_value='True/False', help="If passed the created folder will be opened in vscode")
def create_project(name: str, no_git: bool, open_vscode: bool, directory: str = '.') -> None:
    new_dir = f'{directory}\\{name}' if directory else f'.\\{name}'
    create_folder(name, new_dir)
    create_virtual_environment(new_dir)
    if not no_git:
        initialize_git(new_dir)
        create_gitignore(new_dir)
    if open_vscode:
        open_project_vscode(new_dir)
    click.secho(f"Folder for project {name} was created successfully", fg=SUCCESS)