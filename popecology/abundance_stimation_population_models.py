# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com
import numpy as np


class SamplingPopulation:
    """Superclass for models designed to study abundance stimation techniques"""

    def __init__(self, initial_size: float) -> None:
        if initial_size <= 0:
            raise Exception("Initial population size must be a positive number")
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
        initial_size: int,
        capture_distribution: tuple[float, float],
        death_distribution: tuple[float, float],
        birth_distribution: tuple[float, float],
        inmigration_rate: int,
        mark_lost_probability: float,
    ) -> None:
        # TODO: complete docstring
        """Model for abundance stimination using capture-mark-recapture (CMR) methods.

        Assumptions:
            - All samplings have the same probability distribution.
            - There is only one kind of mark and it does not allows to distinct between individuals.
            - There are not deaths caused by the capture or marking process.
            - Death and birth probability are constant.

        X_distribution represents the conditional probabilities [P(X|unmarked), P(X|marked)], such that:
        P(X|unmarked) * P(unmarked) + P(X|marked) * P(marked) = P(X)

        Args:
            initial_size (float): Initial population size before ANY sampling
            capture_distribution (tuple[float, float]): _description_
            death_distribution (tuple[float, float]): _description_
            birth_distribution (tuple[float, float]): _description_
            inmigration_rate (float): _description_
            mark_lost_probability (float): _description_
        """
        super().__init__(initial_size)

        # Initialize population state variables
        self.current_unmarked: int = initial_size
        self.current_marked: int = 0
        self.current_time_step: int = 0

        # Initialize population state and samples records
        self.population_record: list[dict[str, int]] = [
            {self.unmarked_id: initial_size, self.marked_id: 0}
        ]
        self.sample_record: list[dict[str, int]] = [
            {self.unmarked_id: 0, self.marked_id: 0}
        ]
        self.time_step_record: list[int] = [0]

        # Population parameters: distributions and probabilities
        self.capture_distribution: tuple[float, float] = self.__distribution_validator(
            capture_distribution, "capture_distribution"
        )
        self.death_distribution: tuple[float, float] = self.__distribution_validator(
            death_distribution, ""
        )
        self.birth_distribution: tuple[float, float] = self.__distribution_validator(
            birth_distribution, "birth_distribution"
        )

        # TODO checker for non-negative value
        assert inmigration_rate >= 0
        self.inmigration_rate = inmigration_rate

        # check and assing probability values
        self.mark_lost_probability: float = self.__check_valid_probability_value(
            mark_lost_probability, "mark_lost_probability"
        )

    def __distribution_validator(
        self, distribution: tuple[float, float], msg: str
    ) -> tuple[float, float]:
        return (
            self.__check_valid_probability_value(
                distribution[0], msg + " at P(X|unmarked)"
            ),
            self.__check_valid_probability_value(
                distribution[1], msg + " at P(X|marked)"
            ),
        )

    def __check_valid_probability_value(self, probability: float, msg: str) -> float:
        if probability < 0 or probability > 1:
            raise Exception(
                "{}:\nA probability must be a non-negative value equal or lower than 1.0".format(
                    msg
                )
            )
        return probability

    def __update_records(self, new_sample_record: dict[str, int] | None = None):
        self.population_record.append(
            {
                self.unmarked_id: self.current_unmarked,
                self.marked_id: self.current_marked,
            }
        )
        self.time_step_record.append(self.current_time_step)
        if new_sample_record is not None:
            self.sample_record.append(new_sample_record)

    def __sample_with_replacement(self) -> dict[str, int]:
        unmarked_sampled: int = np.random.binomial(
            self.current_unmarked, self.capture_distribution[0]
        )
        marked_sampled: int = np.random.binomial(
            self.current_marked, self.capture_distribution[1]
        )
        return {self.unmarked_id: unmarked_sampled, self.marked_id: marked_sampled}

    def __sample_and_mark(self) -> dict[str, int]:
        # TODO Erro handling

        # take a sample for the population
        sample = self.__sample_with_replacement()
        total_sampled = sum(sample.values())

        # update mark states
        self.current_unmarked -= total_sampled
        self.current_marked += total_sampled
        self.__update_records(sample)
        return sample

    def __sample_but_not_mark(self) -> dict[str, int]:
        # TODO Erro handling

        sample = self.__sample_with_replacement()
        self.__update_records(sample)
        return sample

    def time_interlude(self):
        """Describes how the population changes between two CONSECUTIVE samplings

        First compute mark lost, next deaths, and finally new individuals.
        """
        # Individuals that lost their marks
        lost_marks: int = np.random.binomial(
            self.current_marked, self.mark_lost_probability
        )
        self.current_unmarked += lost_marks
        self.current_marked -= lost_marks

        # Dead individuals
        dead_unmarked: int = np.random.binomial(
            self.current_unmarked, self.death_distribution[0]
        )
        dead_marked: int = np.random.binomial(
            self.current_marked, self.death_distribution[1]
        )

        self.current_unmarked += dead_unmarked
        self.current_marked -= dead_marked

        # New individuals
        births_from_unmarked: int = np.random.binomial(
            self.current_unmarked, self.birth_distribution[0]
        )
        births_from_marked: int = np.random.binomial(
            self.current_marked, self.birth_distribution[1]
        )

        # Born and inmigration balance
        self.current_unmarked = (
            births_from_unmarked + births_from_marked + self.inmigration_rate
        )

        # update time counter
        self.current_time_step += 1
        # Update records
        self.__update_records()

    def sample(self, with_mark: bool = False) -> dict[str, int]:
        if with_mark:
            return self.__sample_and_mark()
        else:
            return self.__sample_but_not_mark()
