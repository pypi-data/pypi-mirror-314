# __main__.py

from mypackage_gyy import generators
from mypackage_gyy import iterators
from mypackage_gyy import decorators
from mypackage_gyy import descriptors

if __name__ == "__main__":
    print("Launching mypackage")

    # Run each module's main function if they exist
    print("\nRunning generators module:")
    generators.main()  # Assuming `main` exists in generators.py

    print("\nRunning iterators module:")
    iterators.main()   # Assuming `main` exists in iterators.py

    print("\nRunning decorators module:")
    decorators.main()  # Assuming `main` exists in decorators.py

    print("\nRunning descriptors module:")
    descriptors.main()  # Assuming `main` exists in descriptors.py