from jnbv.compare import dummy_test


def test_dummy_test():
    print("Hello!!")
    if not dummy_test():
        raise AssertionError
