import os
import subprocess
import sys


ENV_CONTENT = """# MUST BE SET TO RUN PROJECT
SECRET_KEY=""

# Email
EMAIL=""
EMAIL_PASSWORD=""
"""


def run_command(command: list[str], shell: bool = False):
    """Run a shell command and handle any errors.

    Parameters
    ----------
    command : list of str
        The shell command to execute as a list of arguments.
    shell : bool, optional
        Whether to execute the command through the shell (default is False).

    Raises
    ------
    CalledProcessError
        If the command fails, exits the program with an error message.
    """

    try:
        subprocess.run(command, shell=shell, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{e.cmd}' failed with exit code {e.returncode}")
        sys.exit(1)


class ProjectSetup:
    def __init__(self, venv_dir: str):
        self.venv_dir = venv_dir


    def create_venv(self):
        """Create a Python virtual environment if it does not already exist.

        This function checks if the virtual environment directory exists. If not, it creates
        a new Python virtual environment in the specified directory.
        """

        print("Creating Python virtual environment...")

        if not os.path.exists(self.venv_dir):
            run_command([sys.executable, "-m", "venv", self.venv_dir])
        else:
            print("Virtual environment already exists. Skipping creation.")


    def activate_venv(self):
        """Activate the virtual environment.

        Notes
        -----
        On Windows, the activation script is located in `Scripts/activate`. On Unix-based systems,
        it is in `bin/activate`.
        """

        if os.name == "nt":
            activate_script = os.path.join(self.venv_dir, "Scripts", "activate.bat")
            run_command([activate_script], shell=True)
        else:
            activate_script = os.path.join(self.venv_dir, "bin", "activate")
            run_command(["source", activate_script], shell=True)


    def install_pip_requirements(self):
        """Install Python dependencies from a `requirements.txt` file.

        This function uses `pip` from the virtual environment to install the required
        Python packages specified in the `requirements.txt` file.

        Notes
        -----
        On Windows, pip is located at `Scripts/pip.exe`. On Unix-based systems,
        it is at `bin/pip`.
        """
        
        print("Installing Python dependencies...")
        if os.name == "nt":
            pip_path = os.path.join(self.venv_dir, "Scripts", "pip.exe")
        else:
            pip_path = os.path.join(self.venv_dir, "bin", "pip")

        run_command([pip_path, "install", "-r", "requirements.txt"])

    def create_env_file(self):
        """
        Creates a `.env` file with default content if the file does not exist.

        Notes
        -----
        The `.env` file will be created with the following default options:
        
        - SECRET_KEY - Django secret key
        - EMAIL - Email address for sending emails
        - EMAIL_PASSWORD - App password for loging into email
        """

        if not os.path.exists('.env'):
            with open('.env', "w") as file:
                file.write(ENV_CONTENT)
                print(f"'.env' created successfully.")
        else:
            print(f"'.env' already exists.")


    def install_node_dependencies(self):
        """Install Node.js dependencies from a `package.json` file.

        This function checks if a `package.json` file exists in the current directory.
        If it does, it runs `npm install` to set up Node.js dependencies.

        Notes
        -----
        On Windows, the command is executed with `shell=True` to avoid path issues.
        """

        print("Installing Node.js dependencies...")
        if not os.path.exists("package.json"):
            print("No package.json found. Skipping Node.js setup.")
            return

        run_command(["npm", "install"], shell=(os.name == "nt"))


def main():
    project = ProjectSetup(venv_dir='venv')

    project.create_venv()
    project.activate_venv()
    project.install_pip_requirements()
    project.create_env_file()
    project.install_node_dependencies()
    
    print("Project setup complete!")


if __name__ == "__main__":
    main()