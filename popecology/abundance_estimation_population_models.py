# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com
import numpy as np


class SamplingPopulation:
    """Superclass for models designed to study abundance stimation techniques"""

    def __init__(self, initial_size: int) -> None:
        if initial_size <= 0:
            raise Exception("Initial population size must be a positive number")
        self.initial_size: int = initial_size
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
        inmigration_rate: int,
        mark_lost_probability: float,
    ) -> None:
        # TODO: complete docstring
        """Model for abundance stimination using capture-mark-recapture (CMR) methods.

        Assumptions:
            - All samplings have the same probability distribution.
            - There is only one kind of mark and it does not allows to distinct between individuals.
            - There are not deaths caused by the capture or marking process.
            - Death probability is constant.

        X_distribution represents the conditional probabilities [P(X|unmarked), P(X|marked)], such that:
        P(X|unmarked) * P(unmarked) + P(X|marked) * P(marked) = P(X)

        Args:
            initial_size (float): Initial population size before ANY sampling
            capture_distribution (tuple[float, float]): _description_
            death_distribution (tuple[float, float]): _description_
            inmigration_rate (float): _description_
            mark_lost_probability (float): _description_
        """
        super().__init__(initial_size)

        # Initialize population state variables
        self._current_unmarked: int = initial_size
        self._current_marked: int = 0
        self._current_time_step: int = 0

        # Initialize population state and samples records
        self.population_record: list[dict[str, int]] = [
            {self.unmarked_id: initial_size, self.marked_id: 0}
        ]
        self.sample_record: list[dict[str, int]] = [
            {self.unmarked_id: 0, self.marked_id: 0}
        ]
        self.time_step_record: list[int] = [0]

        # Population parameters: distributions and probabilities
        self._capture_distribution: tuple[float, float] = self.__distribution_validator(
            capture_distribution, "capture_distribution"
        )
        self._death_distribution: tuple[float, float] = self.__distribution_validator(
            death_distribution, ""
        )
        self._inmigration_rate = self.__check_is_natural_number(
            inmigration_rate, include_zero=True, msg="inmigration_rate"
        )

        # check and assing probability values
        self._mark_lost_probability: float = self.__check_valid_probability_value(
            mark_lost_probability, "mark_lost_probability"
        )

    def __check_valid_probability_value(self, probability: float, msg: str) -> float:
        if probability < 0 or probability > 1:
            raise Exception(
                "{}:\nA probability must be a non-negative value equal or lower than 1.0".format(
                    msg
                )
            )
        return probability

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

    def __check_is_natural_number(self, value: int, msg: str, include_zero=True) -> int:
        if include_zero and value < 0:
            raise Exception("{}:\nMust be a non-negative value.".format(msg))

        if not include_zero and value <= 0:
            raise Exception("{}:\nMust be a positive value.".format(msg))

        return value

    def __update_records(self, new_sample_record: dict[str, int] | None = None):
        self.population_record.append(
            {
                self.unmarked_id: self._current_unmarked,
                self.marked_id: self._current_marked,
            }
        )
        self.time_step_record.append(self._current_time_step)
        if new_sample_record is None:
            self.sample_record.append({"no_sample_u": 0, "no_sample_m": 0})
        else:
            self.sample_record.append(new_sample_record)

    def __sample_without_replacement(self, trap_number: int) -> dict[str, int]:
        """Obtain a sample without replacement.

        For each i trap:

        First, determine if trap successfully captured an individual.
            P(capture|unmarked) * P(unmarked_i) + P(capture|marked) * P(marked_i) = P(capture_i)
        Second, given a successful capture, define whether it is marked or doesn't.
            P(unmarked|captured) = P(captured|unmarked) P(unmarked_i) / P(capture_i)

        Args:
            trap_number (int): The number of traps. A trap can capture only one individual.
            A captured individual cannot be trapped by another trap.

        Returns:
            dict[str, int]: Number of marked and unmarked captured individuals.
        """

        population_current_size = self._current_unmarked + self._current_marked
        if trap_number > population_current_size:
            raise Exception("Sample size cannot be bigger than the actual population")

        unmarked_sampled: int = 0
        capture_failure_count: int = 0

        for i in range(0, trap_number):
            p_unmarked: float = max(self._current_unmarked - unmarked_sampled, 0) / (
                population_current_size - i + capture_failure_count
            )

            # P(captured|unmarked) P(unmarked) + P(captured|marked) P(marked), P(marked) = 1 - P(unmarked)
            total_probability: float = (
                self._capture_distribution[0] - self._capture_distribution[1]
            ) * p_unmarked + self._capture_distribution[1]

            captured_something: bool = np.random.binomial(1, total_probability) == 1

            if not captured_something:
                capture_failure_count += 1
                continue

            # If captured_something is True, necessarily total_probability ≠ 0.
            p_unmarked_given_captured: float = (
                self._capture_distribution[0] * p_unmarked / total_probability
            )
            unmarked_sampled += np.random.binomial(1, p_unmarked_given_captured) == 1
        marked_sampled = trap_number - unmarked_sampled - capture_failure_count
        return {self.unmarked_id: unmarked_sampled, self.marked_id: marked_sampled}

    def sample_and_mark(self, sample_size: int) -> dict[str, int]:
        # take a sample for the population
        sample = self.__sample_without_replacement(sample_size)

        # update population marks state
        self._current_unmarked = self._current_unmarked - sample[self.unmarked_id]
        self._current_marked = self._current_marked + sample[self.unmarked_id]

        # update records
        self.__update_records(sample)

        return sample

    def sample_but_not_mark(self, sample_size: int) -> dict[str, int]:
        # take a sample for the population
        sample = self.__sample_without_replacement(sample_size)

        # update records
        self.__update_records(sample)

        return sample

    def time_interlude(self):
        # TODO: complete docstring

        """Describes how the population changes if sampling time is bigger enough."""

        # TODO: check and evaluate if the mathematical model is appropriate.

        # Individuals that lost their marks
        lost_marks: int = np.random.binomial(
            self._current_marked, self._mark_lost_probability
        )
        self._current_unmarked += lost_marks
        self._current_marked -= lost_marks

        # Dead individuals
        dead_unmarked: int = np.random.binomial(
            self._current_unmarked, self._death_distribution[0]
        )
        dead_marked: int = np.random.binomial(
            self._current_marked, self._death_distribution[1]
        )

        self._current_unmarked += dead_unmarked
        self._current_marked -= dead_marked

        # Inmigration balance
        self._current_unmarked += self._inmigration_rate

        # update time counter
        self._current_time_step += 1
        # Update records
        self.__update_records()
