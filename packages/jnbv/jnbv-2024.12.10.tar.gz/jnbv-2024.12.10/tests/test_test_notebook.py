from jnbv.test import test_ipynb


def test_valid_kernel_valid_notebook():
    """Test a notebook that should contain no errors"""

    test_result = test_ipynb("tests/example-hdf5-notebook.ipynb", False)
    if not test_result:
        raise AssertionError


def test_valid_kernel_error_notebook():
    """Test a notebook that contains an error"""

    test_result = test_ipynb("tests/example-hdf5-notebook-error.ipynb", False)
    if test_result:
        raise AssertionError


def test_valid_kernel_invalid_notebook():
    """Test a notebook that is not a valid ipynb file"""

    test_result = test_ipynb("tests/test_compare_dummy.py", False)
    if test_result:
        raise AssertionError


def test_valid_kernel_nonexistent_notebook():
    """Test a notebook that does not exist"""

    test_result = test_ipynb("tests/i-am-not-here.ipynb", False)
    if test_result:
        raise AssertionError
