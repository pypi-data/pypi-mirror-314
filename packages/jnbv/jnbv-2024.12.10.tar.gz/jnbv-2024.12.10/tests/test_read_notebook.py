from jnbv.read import read_ipynb


def test_valid_kernel_valid_notebook():
    """Read a notebook
       Expect no errors to be returned
    """

    nb, errors = read_ipynb("tests/example-hdf5-notebook.ipynb", False, False)
    if not (errors == [] or errors is None):
        raise AssertionError


def test_valid_kernel_invalid_notebook():
    """Read a notebook that is not a valid ipynb file
       Expect an error to be returned
    """

    nb, errors = read_ipynb("tests/test_compare_dummy.py", False, False)
    if errors != ['FILE NOT VALID']:
        raise AssertionError


def test_valid_kernel_nonexistent_notebook():
    """Read a notebook that does not exist
       Expect an error to be returned
    """

    nb, errors = read_ipynb("tests/i-am-not-here.ipynb", False, False)
    if errors != ['FILE NOT ACCESSIBLE']:
        raise AssertionError
