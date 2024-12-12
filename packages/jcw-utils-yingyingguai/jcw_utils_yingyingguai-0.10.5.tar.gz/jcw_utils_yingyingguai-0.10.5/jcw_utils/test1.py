import os
import inspect
from icecream import ic

def print_script_and_function_name():
    # Get the current script's file path
    script_path = os.path.abspath(__file__)

    # Get the current function name using inspect
    current_function_name = inspect.currentframe().f_code.co_name

    # Print the script path and function name
    print(f"Current script path: {script_path}")
    print(f"Current function name: {current_function_name}")

# Example function
def example_function():
    print_script_and_function_name()
    current_function_name = inspect.currentframe().f_code.co_name
    ic(current_function_name)

# Run the example function
# example_function()
class classname(object):
    
    """
    docstring
    """
    pass
a=classname()
print(a)