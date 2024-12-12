"""
Automated testing script for building, installing, and testing a Python package.

This script:
1. Builds the Python package using the build module.
2. Installs the built package using pip with a force-reinstall option.
3. Runs tests using pytest, ensuring that any issues are surfaced.
"""

import os
import subprocess
import glob
import sys


def run_command(command, description=""):
    """
    Run a shell command and handle errors.

    Parameters:
    - command (str): The shell command to run.
    - description (str): Description of the action being performed.
    """
    try:
        if description:
            print(f"\n{description}")
        print(f"Running: {command}")
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)


def install_dependencies():
    """Ensure required dependencies are installed."""
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    run_command(f"{sys.executable} -m pip install build pytest pytest-cov", "Installing required tools")


def build_package():
    """
    Build the package using the build module.
    
    Removes old builds from the `dist` folder before proceeding.
    """
    if os.path.exists("dist"):
        # Remove old builds
        print("\nCleaning up old builds...")
        for file in glob.glob("dist/*"):
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except OSError as e:
                print(f"Error removing {file}: {e}")
    
    # Build the package
    run_command(f"{sys.executable} -m build", "Building the package")


def install_package(package_path, extra_params=""):
    """
    Install the package from the given path.

    Parameters:
    - package_path (str): Path to the package `.whl` file.
    - extra_params (str): Additional parameters for pip install.
    """
    command = f"{sys.executable} -m pip install {package_path} --force-reinstall {extra_params}"
    run_command(command, "Installing the package")


def run_tests():
    """Run tests using pytest recursively through all test folders."""
    run_command(
        f"{sys.executable} -m pytest tests/ -v --maxfail=3 --disable-warnings",
        "Running tests with pytest in all test folders"
    )


def main():
    """
    Execute the automated testing process.

    Steps:
    1. Install dependencies.
    2. Build the package.
    3. Install the built package.
    4. Run tests.
    """
    print("Starting automated testing process...")

    # Step 0: Ensure dependencies are installed
    install_dependencies()

    # Step 1: Build the package
    build_package()

    # Step 2: Find the built .whl file
    wheel_files = glob.glob("dist/*.whl")
    if not wheel_files:
        print("\nNo .whl file found in dist/. Ensure the build step succeeded.")
        exit(1)
    latest_wheel = wheel_files[-1]  # Get the most recent wheel file
    print(f"\nFound wheel file: {latest_wheel}")

    # Step 3: Install the package
    install_package(latest_wheel)

    # Step 4: Run the tests
    run_tests()

    print("\nAll steps completed successfully!")


if __name__ == "__main__":
    main()
