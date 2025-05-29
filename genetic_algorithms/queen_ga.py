import random
from ga import Individual, genetic_algorithm
from queens_fitness import fitness_fn_negative
from typing import Self

n = 8  # 8-Queens problem


class Board(Individual):
    def __init__(self, gene: tuple[int, ...]):
        self.gene = gene

    def get_fitness(self) -> float:
        # Return negative number of conflicts (maximize zero-conflict boards)
        return fitness_fn_negative(self.gene)

    def mutate(self) -> Self:
        # Swap two random columns
        i, j = random.sample(range(n), 2)
        g = list(self.gene)
        g[i], g[j] = g[j], g[i]
        return Board(tuple(g))

    def reproduce(self, other: Self) -> Self:
        # Single-point crossover
        point = random.randint(1, n - 2)
        child_gene = self.gene[:point] + other.gene[point:]
        return Board(child_gene)

    def __hash__(self):
        return hash(self.gene)

    def __repr__(self):
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"

    @classmethod
    def create_random(cls) -> Self:
        gene = list(range(n))
        random.shuffle(gene)
        return cls(tuple(gene))


def get_initial_population(count: int) -> set[Board]:
    population = set()
    while len(population) < count:
        population.add(Board.create_random())
    return population


def main():
    minimal_fitness = 0  # Best fitness is 0 conflicts
    initial_population = get_initial_population(100)

    fittest = genetic_algorithm(
        initial_population,
        minimal_fitness=minimal_fitness,
        num_of_generations=1000,
        should_trim_population=True
    )

    print(f"Fittest Individual: {fittest} - fitness: {fittest.get_fitness()}")


if __name__ == '__main__':
    main()
