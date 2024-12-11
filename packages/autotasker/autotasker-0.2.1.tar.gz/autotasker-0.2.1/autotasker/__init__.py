import click
from autotasker.managers.docker_manager import DockerManager
from InquirerPy import prompt, inquirer

from autotasker.commands import docker

@click.group()
@click.version_option(version="0.2.1", message="autotasker 0.2.1")
def cli():
    """Application for Automating Processes."""
    pass

# Register commands
cli.add_command(docker)



if __name__ == '__main__':
    cli()
