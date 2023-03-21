# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com

from growth_models import Growth


class SamplingPopulation:
    """Superclass for models designed to study abundance stimation techniques"""

    def __init__(self, initial_size: float, growth_model: type[Growth]) -> None:
        if initial_size <= 0:
            raise Exception("Initial population size must be a positive number")
        self.growth_model = growth_model(initial_size)
        self.marked_id: str = "marked"
        self.unmarked_id: str = "unmarked"


class CmrPopulation(SamplingPopulation):
    """Model for abundance stimination using capture-mark-recapture (CMR) methods.

    Assumptions:
        - All samplings have the same probability distribution.
        - There is only one kind of mark and it does not allows to distinct between individuals.
        - All captured individual is marked.

    Args:
        SamplingPopulation(class): superclass for all populations to study abundance stimation techniques.
    """

    def __init__(
        self,
        initial_size: float,
        growth_model: type[Growth],
        capture_distribution: tuple[float, float, float],
        mortality_distribution: tuple[float, float, float],
        natality_distribution: tuple[float, float, float],
        mark_lost_probability: float,
    ) -> None:
        # BUG: Correct formulas. The implemented equation is wrong; the correct expression is:
        #  P(X | no marked) * P(no marked) + P(X|marked) * P(marked) =
        #  P( X and no marked) + P( X and marked) = P(X)

        """Initialices an istance of capture-mark-recapture class.
        Distributions describe how behaves a trait X with respect to marked state. In order:
            1st. P( X | no marked) = a
            2nd. P( X | marked ) = b
            3rd. P(X), such that a + b = P(X)

        Args:
            initial_size (float): True population size before any sampling or marking.
            growth_model (type[Growth]): Population Growth model (e.g. linear, logistic, exponential, etc.)
            capture_distribution (tuple[float, float, float]): Modelf for capture probability. X:= capture
            mortality_distribution (tuple[float, float, float]): Modelf for mortality. X:= dead at next sampling
            natality_distribution (tuple[float, float, float]): Model for natality. X:= new individuals at next sampling
            mark_lost_probability (float): Probability of list the mark at next sampling.
        """
        super().__init__(initial_size, growth_model)

        # Initialize population state variables
        self.current_unmarked: int | float = initial_size
        self.current_marked: int | float = 0.0
        self.current_time_step: int = 0

        # Initialize population state and samples records
        self.population_record: list[dict[str, int | float]] = [
            {self.unmarked_id: initial_size, self.marked_id: 0}
        ]
        self.sample_record: list[dict[str, int | float]] = [
            {self.unmarked_id: 0, self.marked_id: 0}
        ]

        # Population parameters: distributions and probabilities
        self.capture_distribution: tuple[
            float, float, float
        ] = self.__distribution_validator(capture_distribution, "")
        self.mortality_distribution: tuple[
            float, float, float
        ] = self.__distribution_validator(mortality_distribution, "")
        self.natality_distribution: tuple[
            float, float, float
        ] = self.__distribution_validator(natality_distribution, "")

        # check and assing probability values
        self.__check_valid_probability_value(mark_lost_probability)
        self.mark_lost_probability: float = mark_lost_probability

    def __distribution_validator(
        self, distribution: tuple[float, float, float], id_msg: str
    ) -> tuple[float, float, float]:
        # BUG: the equation is wrong. P(A| ¬M) + P(A|M) ≠ P(A)
        # Check values correspond to a partition. P(A| ¬M) + P(A|M) = P(A)
        if sum(distribution[0:2]) != distribution[2]:
            raise Exception(
                "{}.\nThe last value represents the total probability and must\
                      be equall to the sum of the other values".format(
                    id_msg
                )
            )
        # check probabilities are valid. P(A) >= 0
        self.__check_valid_probability_value(distribution[2])
        return distribution

    def __check_valid_probability_value(self, probability: float) -> None:
        if probability < 0 or probability > 1:
            raise Exception(
                "A probability must be a non-negative value equal or lower than 1.0"
            )

    def __sample_and_mark(self):
        # take a sample for the population

        # update mark states

        # update records

        # TODO: implement function
        pass

    def __sample_but_not_mark(self):
        # take a sample and do nothing more

        # TODO: implement function
        pass

    def time_interlude_independent_of_growth_model(self):
        """Describes how the population changes between two CONSECUTIVE samplings"""
        # born individuals
        # die individuals
        # some individuals lost their mark
        # update time counter

        # IMPORTANT! remember tu update population size accordingly to growth function.
        # TODO: implement function
        pass

    def sample(self):
        """Simulations the sampling (capture/recapture) process"""
        # TODO: implement function
        pass
