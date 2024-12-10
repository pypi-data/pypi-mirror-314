from typing import TypeVar
from geneticengine.solutions.individual import Individual
from geneticengine.problems import Problem


def best_individual(population: list[Individual], problem: Problem) -> Individual:
    """Returns the best individual of a population."""
    return max(population, key=lambda x: x.get_fitness(problem).maximizing_aggregate)


def is_better(problem: Problem, individual: Individual, other: Individual) -> bool:
    """Returns whether one individual is better than other.

    Requires the individuals to be evaluated.
    """
    return problem.is_better(individual.get_fitness(problem), other.get_fitness(problem))


T = TypeVar("T", bound=Individual)


def sort_population(population: list[T], problem: Problem) -> list[T]:
    """Sorts the population so the best one is first.

    Requires the individuals to be evaluated.
    """
    return sorted(population, key=lambda x: x.get_fitness(problem).maximizing_aggregate, reverse=True)
