# Import modules (assuming they're named generators.py, iterators.py,
# decorators.py, descriptors.py)
from . import generators
from . import iterators
from . import decorators
from . import descriptors


def run_module(module_name):
    """
    Run the main function of the specified module if it exists.
    """
    if module_name == "generators" and hasattr(generators, 'main'):
        print("\nRunning generators module:")
        generators.main()
    elif module_name == "iterators" and hasattr(iterators, 'main'):
        print("\nRunning iterators module:")
        iterators.main()
    elif module_name == "decorators" and hasattr(decorators, 'main'):
        print("\nRunning decorators module:")
        decorators.main()
    elif module_name == "descriptors" and hasattr(descriptors, 'main'):
        print("\nRunning descriptors module:")
        descriptors.main()
    else:
        print(f"Module '{module_name}' not found or has no main function.")


# When run as a script, prompt the user to specify the module they want to run.
if __name__ == "__main__":
    module_name = input(
        "Enter the module you want to run (generators, iterators, decorators, descriptors): ").strip()
    run_module(module_name)
