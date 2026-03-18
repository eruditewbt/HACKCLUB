import docker
import os

class CodeExecutor:
    """Executes code in a secure, language-specific Docker container."""

    def __init__(self):
        self.client = docker.from_env()
        self.lang_images = {
            "python": "python:3.9-slim",
            "javascript": "node:16-alpine",
            "cpp": "gcc:latest" # Example for a compiled language
        }

    def run_code(self, project_path, language, entry_file="main.py"):
        """
        Runs the code in the project directory using a Docker container.

        Args:
            project_path (str): The path to the project directory.
            language (str): The programming language.
            entry_file (str): The main file to execute.

        Returns:
            A tuple (exit_code, stdout, stderr).
        """
        if language not in self.lang_images:
            return 1, "", f"Error: Language '{language}' is not supported."

        image = self.lang_images[language]

        # Determine the command to run based on the language
        if language == "python":
            command = f"python {entry_file}"
        elif language == "javascript":
            command = f"node {entry_file}"
        elif language == "cpp":
            # Example for a compiled language: compile and then run
            command = f"g++ {entry_file} -o app && ./app"
        else:
            command = ""

        try:
            # Create and run the container
            container = self.client.containers.run(
                image,
                command,
                volumes={
                    os.path.abspath(project_path): {
                        'bind': '/app',
                        'mode': 'rw'
                    }
                },
                working_dir='/app',
                detach=True,
                remove=True
            )

            # Wait for the container to finish and get the output
            result = container.wait(timeout=60)
            stdout = container.logs(stdout=True, stderr=False).decode('utf-8')
            stderr = container.logs(stdout=False, stderr=True).decode('utf-8')

            return result['StatusCode'], stdout, stderr

        except docker.errors.ImageNotFound:
            return 1, "", f"Error: Docker image '{image}' not found."
        except Exception as e:
            return 1, "", f"An unexpected Docker error occurred: {e}"