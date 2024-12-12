import pytest
from example_package_m67.hello import add_one


def test_add_one():
    assert add_one(1) == 2
    assert add_one(0) == 1
    assert add_one(-1) == 0
    assert add_one(100) == 101


if __name__ == "__main__":
    pytest.main()
