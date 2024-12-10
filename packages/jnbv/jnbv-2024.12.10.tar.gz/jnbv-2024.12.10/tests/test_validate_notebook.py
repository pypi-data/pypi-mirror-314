from jnbv.__main__ import run_actions


def test_valid_kernel_valid_notebook():
    """Run validation test with valid kernel and valid notebook"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/example-hdf5-notebook-original.ipynb",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if not validation_result:
        raise AssertionError


def test_valid_kernel_valid_notebook_plotting_py3789():
    """Run validation test with valid kernel and valid notebook"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/example_plots_matplotlib_ipywidget.ipynb",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if not validation_result:
        raise AssertionError


def test_valid_kernel_valid_notebook_plotting_py36():
    """Run validation test with valid kernel and valid notebook"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/example_plots_matplotlib_ipywidget_py36.ipynb",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if not validation_result:
        raise AssertionError


def test_invalid_kernel_valid_notebook():
    """Run validation test with kernel that is missing dependencies"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/example-hdf5-notebook-original.ipynb",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if validation_result:
        raise AssertionError


def test_valid_kernel_invalid_notebook():
    """Run validation test with notebook that contains a syntax error"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/example-hdf5-notebook-invalid-syntax.ipynb",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if validation_result:
        raise AssertionError


def test_valid_kernel_invalid_notebook_2():
    """Run validation test with notebook that is not an ipynb notebook"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/test_compare_dummy.py",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if validation_result:
        raise AssertionError


def test_valid_kernel_nonexistent_notebook():
    """Run validation test with notebook that does not exist"""

    successful_execution, test_result, comparison_result = \
        run_actions(True, True, True, True, False, "python3", False,
                    "tests/i-am-not-here.ipynb",
                    "output.ipynb", "")

    validation_result = successful_execution and test_result and \
        comparison_result

    if validation_result:
        raise AssertionError
