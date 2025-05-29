import random
from ga import Individual, genetic_algorithm
from typing import Self


class NumberIndividual(Individual):
    def __init__(self, gene: tuple[int, int, int]):
        self.gene = gene

    def get_fitness(self) -> float:
        # Convert binary tuple to integer
        return sum(bit * (2 ** i) for i, bit in enumerate(reversed(self.gene)))

    def mutate(self) -> Self:
        # Flip one random bit
        index = random.randint(0, 2)
        mutated_gene = list(self.gene)
        mutated_gene[index] ^= 1
        return NumberIndividual(tuple(mutated_gene))

    def reproduce(self, other: Self) -> Self:
        # Single-point crossover
        point = random.randint(1, 2)
        child_gene = self.gene[:point] + other.gene[point:]
        return NumberIndividual(child_gene)

    def __hash__(self):
        return hash(self.gene)

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def main():
    minimal_fitness = 7  # maximum possible for 3-bit binary
    initial_population = {
        NumberIndividual((1, 0, 0)),
        NumberIndividual((0, 1, 0)),
        NumberIndividual((0, 0, 1)),
        NumberIndividual((0, 0, 0)),
    }

    fittest = genetic_algorithm(initial_population, minimal_fitness)
    print("Fittest Individual:", fittest)


if __name__ == '__main__':
    main()
