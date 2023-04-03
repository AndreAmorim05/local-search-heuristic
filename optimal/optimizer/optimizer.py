from optimal.utils import Investiment, Risk


class Optimizer:
    """
    Optimizer class, responsible for manipulate data and do optimization above it.
    This class has two approachs of optimization, the 'gluttonous' one, that is
    in general less efficient and the 'scored' one that is the best one.
    """
    def __init__(
        self,
        investiments: list[dict],
        min_investiments_per_class: dict[Risk, float],
        budget_ceiling_per_class: dict[Risk, int],
        budget_ceiling: float
    ):
        self.investiments = investiments
        self.budget_ceiling = budget_ceiling
        self.budget_ceiling_per_class = budget_ceiling_per_class
        self.min_investiments_per_class = min_investiments_per_class


    def scan(self, data, key=None, value=None, target='cost'):
        """
        scan method
        """
        count = 0
        if not key and not value:
            if target == 'cost':
                return sum(element.cost for element in data)
            elif target == 'recovery':
                return sum(element.recovery for element in data)

        for element in data:
            if key == 'risk':
                if element.risk != value:
                    continue
                if target == 'recovery':
                    count += element.recovery
                elif target == 'cost':
                    count += element.cost
        return count


    def sorted_candidates(
            self,
            current_solution,
            target='recovery',
            reverse=True
    ):
        candidates = [
            x for x in self.investiments if x not in current_solution
        ]

        if target == 'recovery':
            sort = sorted(
                candidates,
                key=lambda x: x.recovery,
                reverse=reverse
            )

        elif target == 'score':
            sort = sorted(
                candidates,
                key=lambda x: x.score,
                reverse=reverse
            )

        else:
            sort = sorted(
                candidates,
                key=lambda x: x.cost,
                reverse=reverse
            )

        return sort


    def build_initial_solution(self) -> list[Investiment]:
        """
        Constructs a feasible initial solution,
        choosing the investments with the lowest possible cost
        respecting the minimum limit per class
        Returns list with selected investments
        """

        selected = list()

        for _class, ceiling in self.budget_ceiling_per_class.items():
            min_investiments = self.min_investiments_per_class[_class]
            investiments_of_selected_class = [
                investiment for investiment in self.investiments
                if investiment.risk == _class
            ]
            investiments_of_selected_class.sort(key=lambda x: x.cost)
            selected_investiments = investiments_of_selected_class[
                :min_investiments
            ]

            cost_of_selected_class = self.scan(selected_investiments)
            current_total_cost = self.scan(selected)

            if cost_of_selected_class > ceiling:
                raise ValueError(
                    f"There is no feasible solution. Minimum class cost \
                    {_class} is R$ {cost_of_selected_class} that \
                    exceeds the ceiling of R$ {ceiling}"
                )

            if cost_of_selected_class + \
                    current_total_cost > \
                    self.budget_ceiling:
                raise ValueError(
                    "There is no feasible solution. Impossible to choose \
                     the minimum number of investments per class without \
                     exceed the budget ceiling"
                )

            selected += selected_investiments

        return selected


    def build_scored_solution(self) -> list[Investiment]:
        _sorted = self.sorted_candidates([], target='score')
        selected = list()

        for _class, ceiling in self.budget_ceiling_per_class.items():
            min_investiments = self.min_investiments_per_class[_class]
            investiments_of_selected_class = [
                investiment for investiment in _sorted
                if investiment.risk == _class
            ]
            # investiments_of_selected_class.sort(key=lambda x: x.cost)
            selected_investiments = investiments_of_selected_class[
                :min_investiments
            ]
            cost_of_selected_class = self.scan(selected_investiments)
            current_total_cost = self.scan(selected)

            if cost_of_selected_class > ceiling:
                raise ValueError(
                    f"There is no feasible solution. Minimum class cost \
                    {_class} is R$ {cost_of_selected_class} that \
                    exceeds the ceiling of R$ {ceiling}"
                )

            if cost_of_selected_class + \
                    current_total_cost > \
                    self.budget_ceiling:
                raise ValueError(
                    "There is no feasible solution. Impossible to choose \
                     the minimum number of investments per class without \
                     exceed the budget ceiling"
                )

            selected += selected_investiments

        return selected


    def mutate(self, data, candidate) -> list[Investiment]:
        mutated_data = data
        risc = candidate.risk
        filtered_data = filter(lambda x: x.risk == risc, mutated_data)
        for index, element in enumerate(filtered_data):
            if element.recovery < candidate.recovery:
                for i, el in enumerate(mutated_data):
                    if el != element:
                        continue

                    mutated_data[i] = candidate
                    if self.min_investiments_per_class[risc] < self.scan(
                        mutated_data,
                        key='risk',
                        value=risc,
                        target='recovery'
                    ):
                        return data
                return mutated_data
            else:
                return data


    def insertion(self, current_solution, candidate) -> list[Investiment]:
        base_data = current_solution

        if self.scan(base_data, 'risk', candidate.risk, 'cost') + \
                candidate.cost > self.budget_ceiling_per_class[candidate.risk]:
            return current_solution

        base_data.append(candidate)

        if self.scan(base_data, target='cost') > self.budget_ceiling:
            base_data.pop()

        return base_data


    def optimize(self, scored=True, iteration_number: int = 10)\
             -> list[Investiment]:
        current_solution = list()
        _sorted = list()

        if scored:
            try:
                current_solution = self.build_scored_solution()
            except:
                current_solution = self.build_initial_solution()
            _sorted = self.sorted_candidates(current_solution, target='score')
        else:
            current_solution = self.build_initial_solution()
            _sorted = self.sorted_candidates(current_solution)

        if not scored:
            while len(_sorted) > 0:
                candidate = _sorted.pop(0)
                current_solution = self.mutate(current_solution, candidate)

            _sorted = self.sorted_candidates(current_solution)

        while len(_sorted) > 0:
            candidate = _sorted.pop(0)
            current_solution = self.insertion(current_solution, candidate)

        return current_solution
