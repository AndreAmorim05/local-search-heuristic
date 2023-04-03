from .data import *
from .investiment import *

data = {
    "budget_ceiling": 2_400_000,
    "budget_ceiling_per_class": {
        "low": 1_200_000,
        "medium": 1_500_000,
        "high": 900_000
    },
    "min_investiments_per_class": {
        "low": 2,
        "medium": 2,
        "high": 1
    },
    "investiments": [
        {"description": "Ampliação da capacidade do armazém ZDP em 5%", "cost": 470_000, "recovery":410_000, "risk": 0},
        {"description": "Ampliação da capacidade do armazém MGL em 7%", "cost": 400_000, "recovery":330_000, "risk": 0},
        {"description": "Compra de empilhadeira", "cost": 170_000, "recovery":140_000, "risk": 1},
        {"description": "Projeto de P&D I", "cost": 270_000, "recovery":250_000, "risk": 1},
        {"description": "Projeto de P&D II", "cost": 340_000, "recovery":320_000, "risk": 1},
        {"description": "Aquisição de novos equipamentos", "cost": 230_000, "recovery":320_000, "risk": 1},
        {"description": "Capacitação de funcionários", "cost": 50_000, "recovery":90_000, "risk": 1},
        {"description": "Ampliação da estrutura de carga rodoviária", "cost": 440_000, "recovery":190_000, "risk": 2},
        {"description": "Construção de datacenter", "cost": 320_000, "recovery":120_000, "risk": 2},
        {"description": "Aquisição de empresa concorrente", "cost": 800_000, "recovery":450_000, "risk": 2},
        {"description": "Compra de serviços em nuvem", "cost": 120_000, "recovery":80_000, "risk": 0},
        {"description": "Criação de aplicativo mobile e desktop", "cost": 150_000, "recovery":120_000, "risk": 0},
        {"description": "Terceirização do serviço de otimização da logística", "cost": 300_000, "recovery":380_000, "risk": 1},
    ]
}
