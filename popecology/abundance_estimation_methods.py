# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com

from numpy import sqrt


class LincolnPetersen:
    estimator_id: str = "abundance"
    standard_error_id: str = "sd_error"

    @staticmethod
    def __bailey_unbiased_statistic(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> float:
        return (
            (captured)
            * (recaptured_unmarked + recaptured_marked + 1)
            / (recaptured_marked + 1)
        )

    @staticmethod
    def __chapman_unbiased_statistic(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> float:
        return (
            (captured + 1)
            * (recaptured_unmarked + recaptured_marked + 1)
            / (recaptured_marked + 1)
        ) - 1

    @staticmethod
    def __bailey_standard_error(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> float:
        variance_numerator = (
            (captured**2)
            * (recaptured_unmarked + recaptured_marked + 1)
            * (recaptured_unmarked)
        )
        variance_denominator = (recaptured_marked + 1) ** 2 * (recaptured_marked + 2)
        return sqrt(variance_numerator / variance_denominator)

    @staticmethod
    def __chapman_standard_error(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> float:
        variance_numerator = (
            (captured + 1)
            * (recaptured_unmarked + recaptured_marked + 1)
            * (captured - recaptured_marked)
            * recaptured_unmarked
        )
        variance_denominator = (recaptured_marked + 1) ** 2 * (recaptured_marked + 2)
        return sqrt(variance_numerator / variance_denominator)

    @staticmethod
    def simple_biased_statistic(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> float:
        Validator.check_positive_integer(
            [captured, recaptured_unmarked, recaptured_marked]
        )

        return captured * (recaptured_unmarked + recaptured_marked) / recaptured_marked

    @staticmethod
    def bailey_unbiased_summary(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> dict[str, float]:
        Validator.check_positive_integer(
            [captured, recaptured_unmarked, recaptured_marked]
        )
        return {
            LincolnPetersen.estimator_id: LincolnPetersen.__bailey_unbiased_statistic(
                captured, recaptured_unmarked, recaptured_marked
            ),
            LincolnPetersen.standard_error_id: LincolnPetersen.__bailey_standard_error(
                captured, recaptured_unmarked, recaptured_marked
            ),
        }

    @staticmethod
    def chapman_unbiased_summary(
        captured: int, recaptured_unmarked: int, recaptured_marked: int
    ) -> dict[str, float]:
        Validator.check_positive_integer(
            [captured, recaptured_unmarked, recaptured_marked]
        )
        return {
            LincolnPetersen.estimator_id: LincolnPetersen.__chapman_unbiased_statistic(
                captured, recaptured_unmarked, recaptured_marked
            ),
            LincolnPetersen.standard_error_id: LincolnPetersen.__chapman_standard_error(
                captured, recaptured_unmarked, recaptured_marked
            ),
        }


class Validator:
    @staticmethod
    def check_positive_integer(values: list[int]):
        for v in values:
            if v <= 0:
                raise Exception("All values must be positive integers")
