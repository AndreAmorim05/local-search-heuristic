import json
from dataclasses import asdict

from flask import Flask, request

from optimal.optimizer import Optimizer
from optimal.utils import Risk, data, data_converted

app = Flask(__name__)


def convert_class(data, default=None):
    d = data
    for i, element in enumerate(data):
        if element['risk'] == Risk.LOW:
            d[i]['risk'] = 0

        elif element['risk'] == Risk.MEDIUM:
            d[i]['risk'] = 1

        else:
            d[i]['risk'] = 2

    return d


@app.route("/", methods=['GET'])
def home():
    updated_data = data_converted(data)
    optimizer = Optimizer(**updated_data)

    selected = optimizer.optimize()

    selected = list(map(asdict, selected))

    selected = convert_class(selected)

    data_return = {
        "cost": sum(investiment['cost'] for investiment in selected),
        "recovery": sum(investiment['recovery'] for investiment in selected),
        "investiments": selected
    }

    return json.dumps(data_return)


@app.route("/solution", methods=['POST'])
def solution():
    updated_data = None
    if request.get_json():
        updated_data = request.get_json()
    else:
        updated_data = data_converted(data)

    optimizer = Optimizer(**updated_data)
    selected = optimizer.optimize()

    selected = list(map(asdict, selected))

    selected = convert_class(selected)

    data_return = {
        "cost": sum(investiment['cost'] for investiment in selected),
        "recovery": sum(investiment['recovery'] for investiment in selected),
        "investiments": selected
    }

    return json.dumps(data_return)
