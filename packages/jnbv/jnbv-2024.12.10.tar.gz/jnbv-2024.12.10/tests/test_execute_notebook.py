from jnbv.execute import execute_ipynb_pm


def test_valid_kernel_valid_notebook():
    """Execute a notebook that requires certain hdf5 modules to be installed"""

    if not execute_ipynb_pm(
            "tests/example-hdf5-notebook.ipynb",
            "output.ipynb",
            "python3",
            False):
        raise AssertionError


def test_valid_kernel_valid_notebook_plotting():
    """Execute a notebook that requires certain hdf5 modules to be installed"""

    if not execute_ipynb_pm(
            "tests/example_plots_matplotlib_ipywidget.ipynb",
            "output.ipynb",
            "python3",
            False):
        raise AssertionError


def test_invalid_kernel_valid_notebook():
    """Execute a notebook that requires certain hdf5 modules to be installed"""

    if execute_ipynb_pm(
            "tests/example-hdf5-notebook.ipynb",
            "output.ipynb",
            "python3",
            False):
        raise AssertionError


def test_valid_kernel_invalid_notebook():
    """Execute a notebook that contains invalid syntax"""

    if execute_ipynb_pm(
            "tests/example-hdf5-notebook-invalid-syntax.ipynb",
            "output.ipynb",
            "python3",
            False):
        raise AssertionError


def test_valid_kernel_invalid_notebook_2():
    """Execute a notebook that is not an ipynb notebook"""

    if execute_ipynb_pm(
            "tests/test_compare_dummy.py",
            "output.ipynb",
            "python3",
            False):
        raise AssertionError


def test_valid_kernel_nonexistent_notebook():
    """Execute a notebook that does not exist"""

    if execute_ipynb_pm(
            "tests/i-am-not-here.ipynb",
            "output.ipynb",
            "python3",
            False):
        raise AssertionError
