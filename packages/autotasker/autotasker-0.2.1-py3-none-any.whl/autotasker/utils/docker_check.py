import subprocess
import click
import re

def is_docker_running():
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error while running Docker: {e.stderr.strip()}", fg='red'))
        return False
    except FileNotFoundError:
        click.echo(click.style("Docker is not installed or not found in the PATH.", fg='red'))
        return False


def check_names(text: str) -> bool:
    """This function checks if the text contains any characters that are incompatible with Docker."""

    regex = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$'
    return bool(re.match(regex, text))
