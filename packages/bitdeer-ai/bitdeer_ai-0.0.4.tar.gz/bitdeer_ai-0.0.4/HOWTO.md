# How to Update the Python SDK on PyPI

1. Enter the root directory of the Python SDK.
2. Update the version number in the `__about__.py` file.
3. Run the following command to build the package:
    ```bash
    hatch build
    ```
4. Run the following command to upload the package to PyPI:
    ```bash
    hatch publish
    ```