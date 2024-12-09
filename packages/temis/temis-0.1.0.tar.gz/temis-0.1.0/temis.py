import click
import project_management

@click.group()
def cli() -> None:
    pass

cli.add_command(project_management.create_project)

