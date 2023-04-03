import pytest

from optimal.optimizer import Optimizer
from optimal.utils import convert_investments, data_converted


@pytest.fixture(scope="session")
def mock_infeasible_data():
    data = {
        "budget_ceiling": 10_000,
        "budget_ceiling_per_class": {
            "low": 15,
            "medium": 10,
            "high": 5
        },
        "min_investiments_per_class": {
            "low": 1,
            "medium": 1,
            "high": 1
        },
        "investiments": [
            {"description": "Investimento Risco Baixo 1", "cost": 15, "recovery": 50, "risk": 0},
            {"description": "Investimento risco Baixo 2", "cost": 16, "recovery": 100, "risk": 0},
            {"description": "Investimento risco Medio 1", "cost": 10, "recovery": 25, "risk": 1},
            {"description": "Investimento risco Medio 2", "cost": 11, "recovery": 50, "risk": 1},
            {"description": "Investimento risco Alto 1", "cost": 5, "recovery": 30, "risk": 2},
            {"description": "Investimento risco Alto 2", "cost": 6, "recovery": 60, "risk": 2}
        ]
    }

    return data_converted(data)


@pytest.fixture(scope="session")
def mock_not_infeasible_data():
    data = {
        "budget_ceiling": 3,
        "budget_ceiling_per_class": {
            "low": 15,
            "medium": 10,
            "high": 5
        },
        "min_investiments_per_class": {
            "low": 1,
            "medium": 1,
            "high": 1
        },
        "investiments": [
            {"description": "Investimento Risco Baixo 1", "cost": 15, "recovery": 50, "risk": 0},
            {"description": "Investimento risco Baixo 2", "cost": 16, "recovery": 100, "risk": 0},
            {"description": "Investimento risco Medio 1", "cost": 10, "recovery": 25, "risk": 1},
            {"description": "Investimento risco Medio 2", "cost": 11, "recovery": 50, "risk": 1},
            {"description": "Investimento risco Alto 1", "cost": 5, "recovery": 30, "risk": 2},
            {"description": "Investimento risco Alto 2", "cost": 6, "recovery": 60, "risk": 2}
        ]
    }

    return data_converted(data)


def test_if_build_initial_solution_returns_expected_solution(converted_data):
    initial_solution = Optimizer(**converted_data).build_initial_solution()
    expected_solution = convert_investments([
        {"description": "Compra de serviços em nuvem", "cost": 120_000, "recovery":80_000, "risk": 0},
        {"description": "Criação de aplicativo mobile e desktop", "cost": 150_000, "recovery":120_000, "risk": 0},
        {"description": "Capacitação de funcionários", "cost": 50_000, "recovery":90_000, "risk": 1},
        {"description": "Compra de empilhadeira", "cost": 170_000, "recovery":140_000, "risk": 1},
        {"description": "Construção de datacenter", "cost": 320_000, "recovery":120_000, "risk": 2},
    ])

    assert initial_solution == expected_solution


def test_if_build_scored_initial_solution_returns_expected_solution(
        converted_data
):
    initial_solution = Optimizer(**converted_data).build_scored_solution()
    expected_solution = convert_investments([
        {"description": "Ampliação da capacidade do armazém ZDP em 5%", "cost": 470_000, "recovery":410_000, "risk": 0},
        {"description": "Ampliação da capacidade do armazém MGL em 7%", "cost": 400_000, "recovery":330_000, "risk": 0},
        {"description": "Capacitação de funcionários", "cost": 50_000, "recovery": 90_000, "risk": 1},
        {"description": "Aquisição de novos equipamentos", "cost": 230_000, "recovery":320_000, "risk": 1},
        {"description": "Aquisição de empresa concorrente", "cost": 800_000, "recovery":450_000, "risk": 2}
    ])

    assert initial_solution == expected_solution


def test_optimizer_rises_error_if_problem_is_infeasible_by_violate_budget_ceiling(
        mock_infeasible_data
):
    optimizer = Optimizer(**mock_infeasible_data)
    solution = optimizer.optimize(scored=False)
    expected_solution = [
        mock_infeasible_data["investiments"][1],
        mock_infeasible_data["investiments"][3],
        mock_infeasible_data["investiments"][5],
    ]

    assert solution == expected_solution

def test_optimizer_score_rises_error_if_problem_is_infeasible_by_violate_budget_ceiling(
        mock_infeasible_data
):
    optimizer = Optimizer(**mock_infeasible_data)
    solution = optimizer.optimize()
    expected_solution = [
        mock_infeasible_data["investiments"][0],
        mock_infeasible_data["investiments"][2],
        mock_infeasible_data["investiments"][4],
    ]

    assert solution == expected_solution


def test_optimizer_respects_the_budget_ceiling(mock_not_infeasible_data):
    optimizer = Optimizer(**mock_not_infeasible_data)
    with pytest.raises(ValueError) as exc:
        optimizer.optimize(scored=False)

    assert str(exc.value) == "There is no feasible solution. Impossible to choose \
                     the minimum number of investments per class without \
                     exceed the budget ceiling"


def test_optimizer_score_respects_the_budget_ceiling(mock_not_infeasible_data):
    optimizer = Optimizer(**mock_not_infeasible_data)
    with pytest.raises(ValueError) as exc:
        optimizer.optimize()

    assert str(exc.value) == "There is no feasible solution. Impossible to choose \
                     the minimum number of investments per class without \
                     exceed the budget ceiling"


def test_if_sorted_candidates_function_sorts_data(mock_infeasible_data):
    optimizer = Optimizer(**mock_infeasible_data)
    solution = optimizer.optimize(scored=False)
    expected_sort = [
        mock_infeasible_data["investiments"][0],
        mock_infeasible_data["investiments"][4],
        mock_infeasible_data["investiments"][2],
    ]
    assert expected_sort == optimizer.sorted_candidates(solution)


def test_if_scan_retuns_correct_values(mock_infeasible_data):
    optimizer = Optimizer(**mock_infeasible_data)
    solution = optimizer.optimize(scored=False)
    assert optimizer.scan(solution, target='cost') == 33
