import pytest

from optimal.optimizer import Optimizer
from optimal.utils import data, data_converted


@pytest.fixture(scope="module")
def converted_data():
    return data_converted(data)


@pytest.fixture
def optimizer_class(converted_data):
    return Optimizer(**converted_data)
