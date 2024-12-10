from jnbv.compare import compare_ipynb_notebooks


def test_valid_kernel_valid_notebook():
    """Compare original notebook with output from successful execution"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example-hdf5-notebook-original.ipynb",
             "tests/example-hdf5-notebook-successful-execution.ipynb"],
            False)
    if not comparison_result:
        raise AssertionError


def test_valid_kernel_almost_same_notebook():
    """Compare original notebook with output from successful execution"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example-hdf5-notebook-original.ipynb",
             "tests/example-hdf5-notebook-almost-the-same.ipynb"],
            False)
    if not comparison_result:
        raise AssertionError


def test_valid_kernel_different_notebook():
    """Compare original notebook with output from the execution of a
       different notebook"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example-hdf5-notebook-original.ipynb",
             "tests/example-simple-notebook.ipynb"],
            False)
    if comparison_result:
        raise AssertionError


def test_valid_kernel_empty_output_notebook():
    """Compare original notebook with output from the failed execution of a
       notebook"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example_plots_matplotlib_ipywidget.ipynb",
             "tests/example_plots_matplotlib_ipywidget_kernel_died.ipynb"],
            False)
    if comparison_result:
        raise AssertionError


def test_invalid_kernel_valid_notebook():
    """Compare original notebook with output from execution with incorrect
       kernel"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example-hdf5-notebook-original.ipynb",
             "tests/example-hdf5-notebook-invalid-kernel.ipynb"],
            False)
    if comparison_result:
        raise AssertionError


def test_valid_kernel_nonexistent_notebook():
    """Comparison tests with a notebook that does not exist"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example-hdf5-notebook-original.ipynb",
             "tests/i-am-not-here.ipynb"],
            False)
    if comparison_result or error_message != "EMPTY NOTEBOOK!":
        raise AssertionError


def test_valid_kernel_invalid_notebook():
    """Comparison tests with a file that is not an ipynb notebook"""

    comparison_result, error_message, error_content = \
        compare_ipynb_notebooks(
            ["tests/example-hdf5-notebook-original.ipynb",
             "tests/test_compare_dummy.py"],
            False)
    if comparison_result or error_message != "EMPTY NOTEBOOK!":
        raise AssertionError
