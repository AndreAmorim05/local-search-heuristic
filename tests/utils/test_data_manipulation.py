# from copy import deepcopy
import pytest

from optimal.utils import Investiment, Risk, convert_class


@pytest.fixture
def budget_ceiling_per_class():
    budget_ceiling_per_class = {
        "low": 1_200_000,
        "medium": 1_500_000,
        "high": 900_000
    }

    return budget_ceiling_per_class


@pytest.fixture
def single_modificated_data():
    single_data = {
        "description": "Compra de serviços em nuvem",
        "cost": 120_000,
        "recovery": 80_000,
        "risk": Risk.LOW
    }
    return single_data


def test_if_investiments_are_converted_to_dataclass_and_has_score(
        single_modificated_data
):
    single_object = Investiment(**single_modificated_data)

    assert single_object.score == \
        single_modificated_data['recovery'] / single_modificated_data['cost']


def test_if_convert_class_converts_string_keys_to_Risk_type(
        budget_ceiling_per_class
):

    converted = convert_class(budget_ceiling_per_class)

    assert list(converted.keys()) == [Risk.LOW, Risk.MEDIUM, Risk.HIGH]
