import os

class FileManager:
    """Manages file creation, writing, and reading within a project directory."""

    def __init__(self, project_path):
        self.project_path = project_path
        os.makedirs(self.project_path, exist_ok=True)

    def write_file(self, filename, content):
        """Writes content to a file inside the project directory."""
        file_path = os.path.join(self.project_path, filename)
        try:
            with open(file_path, "w") as f:
                f.write(content)
            print(f"File '{filename}' created successfully.")
            return True
        except Exception as e:
            print(f"Error writing to file '{filename}': {e}")
            return False

    def read_file(self, filename):
        """Reads content from a file inside the project directory."""
        file_path = os.path.join(self.project_path, filename)
        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file '{filename}': {e}")
            return None

    def get_all_files(self):
        """Returns a dictionary of all files and their content in the project directory."""
        files_content = {}
        for root, _, filenames in os.walk(self.project_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as f:
                    files_content[filename] = f.read()
        return files_content