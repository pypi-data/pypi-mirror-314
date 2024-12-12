import subprocess
import sys
import re
def run_script_with_auto_install(script_path):
    """
    Run a Python script, and automatically install missing modules if a ModuleNotFoundError occurs.

    Args:
        script_path (str): The path to the Python script to run.
    """
    while True:
        try:
            # Attempt to run the script
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
            print(repr(result.stdout))  # Print script's output if it runs successfully
            break  # Exit loop if script runs successfully
        except subprocess.CalledProcessError as e:
            # Check if the error is a ModuleNotFoundError
            if "ModuleNotFoundError" in e.stderr:
                # Extract the missing module name using regex
                match = re.search(r"No module named '(.*?)'", e.stderr)
                if match:
                    missing_module = match.group(1)
                    print(f"Missing module detected: {missing_module}")
                    print(f"Attempting to install {missing_module}...")

                    # Install the missing module
                    install_result = subprocess.run([sys.executable, "-m", "pip", "install", missing_module])
                    if install_result.returncode != 0:
                        print(f"Failed to install {missing_module}. Exiting.")
                        sys.exit(1)
                else:
                    print("Could not determine the missing module. Exiting.")
                    sys.exit(1)
            else:
                # If it's not a ModuleNotFoundError, re-raise the error
                print("An error occurred:")
                print(e.stderr)
                sys.exit(1)
script_to_run = r"E:\高频常用函数\jcw_utils\audio_operation.py"
run_script_with_auto_install(script_to_run)
