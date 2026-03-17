import os
import sys
import subprocess
import platform

PROJECT_NAME = "LocalDevAgent"
MAIN_FILE = "main.py"
DATA_DIRS = ["data", "utils"]  # directories to include in build

def run_command(cmd):
    """Run a shell command and print output."""
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(1)

def build_with_briefcase():
    """Build using BeeWare Briefcase."""
    print("Detected Briefcase. Building native app...")
    # Initialize project if not exists
    if not os.path.exists(PROJECT_NAME):
        run_command(f"briefcase new --template=existing --name {PROJECT_NAME} --src {MAIN_FILE}")
    run_command(f"briefcase build")
    run_command(f"briefcase package")
    print("\nBriefcase build complete. Check the 'dist/' folder.")

def build_with_pyinstaller():
    """Build using PyInstaller."""
    print("Briefcase not found. Falling back to PyInstaller...")
    # Prepare --add-data arguments for PyInstaller
    add_data_args = []
    sep = ";" if platform.system() == "Windows" else ":"
    for d in DATA_DIRS:
        if os.path.exists(d):
            add_data_args.append(f"--add-data \"{d}{sep}{d}\"")

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        MAIN_FILE
    ] + add_data_args + ["--clean", "--noconfirm"]

    run_command(cmd)
    print("\nPyInstaller build complete. Check the 'dist/' folder.")

def main():
    try:
        import briefcase
        build_with_briefcase()
    except ImportError:
        print("Briefcase not installed.")
        try:
            import PyInstaller.__main__
            build_with_pyinstaller()
        except ImportError:
            print("Neither Briefcase nor PyInstaller is installed. Please install at least one:")
            print("  pip install briefcase")
            print("  or")
            print("  pip install pyinstaller")
            sys.exit(1)

if __name__ == "__main__":
    main()