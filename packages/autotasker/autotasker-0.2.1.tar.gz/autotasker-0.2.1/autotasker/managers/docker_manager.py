import click
import subprocess
from autotasker.utils.dockerfile_templates import get_dockerfile_template
import os
from autotasker.utils.spinner import spinner




class DockerManager:
    """
        A class to manage Docker container creation and management.

        Attributes:
            image (str): The name of the Docker image.
            container (str): The name of the Docker container.
            port (int): The port on which the container will run.
            dockerfile_path (str): The directory where the Dockerfile will be created.
            language (str): The programming language used for the Docker container.
            version (str): The version of the programming language.
    """

    def __init__(self, dockerfile_path: str, language: str, image: str, envs: tuple,env_file:str, port: int = 8000, container: str = None, version: str = None):
        """
        Initializes the DockerManager with an image name, an optional container name, and a port.

        Args:
            dockerfile_path (str): The directory where the Dockerfile will be created.
            image (str): The name of the Docker image to be used.
            container (str, optional): The name for the Docker container. Defaults to "default_container".
            port (int, optional): The port on which the container will run. Defaults to 8000.
            language (str): The programming language for the Docker container
            version (str): The version of the programming language.
            envs (tuple): A tuple of environment variables to be included in the Dockerfile. Each element is a string
                      representing a key-value pair (e.g., ("ENV_VAR1=value1"), ("ENV_VAR2=value2")). These environment
                      variables are directly added to the Dockerfile with the 'ENV' instruction.
            env_file (str): Path to a file containing additional environment variables. Each line of the file should
                        contain a key-value pair formatted as `KEY=value`. These variables are read and also included
                        in the Dockerfile as `ENV` instructions.
        """

        self.version = version
        self.dockerfile_path = os.path.normpath(dockerfile_path)
        self.image = image
        self.port = port
        self.container = container
        self.language = language
        self.envs = envs
        self.env_file = env_file

    def create_dockerfile(self):
        """This function is used to create the Dockerfile based on the provided data."""
        stop = spinner("   • Generating Dockerfile ...")
        template = get_dockerfile_template(self.language, self.port, self.version, self.envs, self.env_file)

        full_dockerfile_path = os.path.join(self.dockerfile_path, "dockerfile")
        with open(full_dockerfile_path, "w") as f:
           f.write(template)
        stop()
        click.echo("\r   • Generating Dockerfile " + click.style("done    ", fg="green"))

    def create_image(self):
        """This function will create the Docker image using the provided data."""
        stop = spinner("   • Building Docker image ...")
        try:
            command = ["docker", "build", "-t", self.image, self.dockerfile_path]

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            stop()
            click.echo("\r   • Building Docker image ... " + click.style("done    ", fg="green"))
        except subprocess.CalledProcessError as e:
            stop()
            click.echo(click.style(f'\nError: {e.stderr.strip()}', fg='red'))
            raise click.Abort()
        except Exception as e:
            stop()
            raise click.Abort()


    def create_container(self):
        """This function will create the container from the previous image."""
        stop = spinner("   • Starting Docker container ...")
        try:
            command = ["docker", "run", "-d", "-p", f"{self.port}:{self.port}", "--name", self.container,
                       self.image]

            result = subprocess.run(command, capture_output=True, text=True)
            stop()

            if result.returncode == 0:
                click.echo("\r   • Starting Docker container ... " + click.style("done    ", fg="green"))
            else:

                click.echo(click.style(f'\nError: {result.stderr}', fg='red'))
                raise click.Abort()
        except Exception as e:
            remove_image = ["docker", "rm", self.container]
            remove_container = ["docker", "image", "rm", self.image]
            click.echo(click.style("Deleting container and image...", fg='red'), nl=False)
            result = subprocess.run(remove_container, capture_output=True, text=True)
            result = subprocess.run(remove_image, capture_output=True, text=True)
            click.echo("\rDeleted                " + click.style("created", fg="red"))
            raise click.Abort()


