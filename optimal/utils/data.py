from .investiment import Investiment, Risk


def convert_investments(data):
    investments = list()
    for investiment in data:
        if investiment['risk'] == 0:
            investiment['risk'] = Risk.LOW
        elif investiment['risk'] == 1:
            investiment['risk'] = Risk.MEDIUM
        else:
            investiment['risk'] = Risk.HIGH
        inv = Investiment(**investiment)
        investments.append(inv)

    return investments


def convert_class(data, default=None):
    d = data
    for _class, _ in data.copy().items():
        if _class == 'low':
            d[Risk.LOW] = d.pop(_class, default)

        elif _class == 'medium':
            d[Risk.MEDIUM] = d.pop(_class, default)

        else:
            d[Risk.HIGH] = d.pop(_class, default)

    return d


def data_converted(data):
    new_data = data
    new_data['min_investiments_per_class'] = convert_class(
        new_data['min_investiments_per_class']
    )
    new_data['budget_ceiling_per_class'] = convert_class(
        new_data['budget_ceiling_per_class']
    )
    new_data['investiments'] = convert_investments(
        new_data['investiments']
    )

    return new_data
