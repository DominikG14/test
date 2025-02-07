import os
import subprocess
import sys

def run_command(command, shell=False):
    """Run shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=shell, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{e.cmd}' failed with exit code {e.returncode}")
        sys.exit(1)

def create_venv_and_install_requirements():
    """Create Python virtual environment and install requirements."""
    print("Creating Python virtual environment...")
    venv_dir = "venv"

    # Step 1: Create virtual environment if it doesn't exist
    if not os.path.exists(venv_dir):
        run_command([sys.executable, "-m", "venv", venv_dir])
    else:
        print("Virtual environment already exists. Skipping creation.")

    # Step 2: Activate virtual environment and install dependencies
    activate_script = os.path.join(venv_dir, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_dir, "bin", "activate")
    
    print("Installing Python dependencies...")
    pip_path = os.path.join(venv_dir, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")

    run_command([pip_path, "install", "--upgrade", "pip"])
    run_command([pip_path, "install", "-r", "requirements.txt"])

def install_node_dependencies():
    """Install Node.js dependencies from package.json."""
    print("Installing Node.js dependencies...")
    if not os.path.exists("package.json"):
        print("No package.json found. Skipping Node.js setup.")
        return

    run_command(["npm", "install"], shell=(os.name == "nt"))


def main():
    create_venv_and_install_requirements()
    install_node_dependencies()
    print("Project setup complete!")


if __name__ == "__main__":
    main()