from optimal.optimizer import Optimizer
from optimal.utils import data, data_converted

if __name__ == "__main__":
    updated_data = data_converted(data)
    optimizer = Optimizer(**updated_data)

    selected = optimizer.optimize()

    print("Os investiments selected foram:")
    for investiment in selected:
        print(f'\t{investiment}')

    print(f"O cost total é R$ \
            {sum(investiment.cost for investiment in selected)} \
    ")
    print(f"O recovery esperado total é R$ \
            {sum(investiment.recovery for investiment in selected)} \
    ")
#     updated_data = data_converted(data)
#     optimizer = Optimizer(**updated_data)

#     selected = optimizer.build_scored_solution()

#     print("Os investiments selected foram:")
#     for investiment in selected:
#         print(f'\t{investiment}')

#     print(optimizer.scan(selected))
#     print(optimizer.scan(selected, target='recovery'))