# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com
from numpy import log
from numpy import power
from enum import Enum


class DeforestationFormula(str, Enum):
    FOREST_CHANGE_PUYRAVAUD = "Puyravaud"
    FOREST_CHANGE_FAO = "FAO"
    ANNUAL_DEFORESTATION_FEARNSIDE_LIU = "Fearnside-Liu"
    ANNUAL_DEFORESTATION_WRI = "WRI"


class DeforestationCalculator:
    """
    Collection of methods for determining forest coverture change. Equations are based on:

    Puyravaud, J.-P. (2003). Standardizing the calculation of the annual rate of deforestation.
    Forest Ecology and Management, 177(1–3), 593–596. https://doi.org/10.1016/S0378-1127(02)00335-3

    Raises:
        Warning: time parameters may be inverted
        Exception: requested invalid formula
        NotImplementedError: requested a not implemented yet method
    """

    INVALID_TYPE: str = "Choose a valid deforestation rate formula.\n"
    WARN_POTENTIAL_TIME_INCONSISTENCY: str = "Time time 1 is not lower than time 2.\n"

    @staticmethod
    def calculate_deforestation_rate(
        formula: DeforestationFormula,
        area_t1: float,
        area_t2: float,
        year_t1: float,
        year_t2: float,
    ) -> float:
        # check cronological consistency
        if not year_t1 < year_t2:
            raise Warning(DeforestationCalculator.WARN_POTENTIAL_TIME_INCONSISTENCY)

        # check valid formula parameter
        if not isinstance(formula, DeforestationFormula):
            raise Exception(DeforestationCalculator.INVALID_TYPE)

        parameters: dict[str, float] = {
            "area_t1": area_t1,
            "area_t2": area_t2,
            "year_t1": year_t1,
            "year_t2": year_t2,
        }

        if formula.name == DeforestationFormula.FOREST_CHANGE_PUYRAVAUD.name:
            return DeforestationCalculator.__puyravaud_annual_rate_of_forest_change(
                **parameters
            )

        if formula.name == DeforestationFormula.FOREST_CHANGE_FAO.name:
            return DeforestationCalculator.__fao_annual_rate_of_forest_change(
                **parameters
            )

        if formula.name == DeforestationFormula.ANNUAL_DEFORESTATION_FEARNSIDE_LIU.name:
            return DeforestationCalculator.__fearnside_liu_annual_deforestation(
                **parameters
            )

        if formula.name == DeforestationFormula.ANNUAL_DEFORESTATION_WRI.name:
            return DeforestationCalculator.__wri_annual_deforestation(**parameters)

        raise NotImplementedError

    @staticmethod
    def __puyravaud_annual_rate_of_forest_change(
        area_t1: float, area_t2: float, year_t1: float, year_t2: float
    ) -> float:
        r: float = 1 / (year_t2 - year_t1) * log(area_t2 / area_t1)
        return r

    @staticmethod
    def __fao_annual_rate_of_forest_change(
        area_t1: float, area_t2: float, year_t1: float, year_t2: float
    ) -> float:
        q: float = power(area_t2 / area_t1, 1 / (year_t2 - year_t1)) - 1
        return q

    @staticmethod
    def __fearnside_liu_annual_deforestation(area_t1, area_t2, year_t1, year_t2):
        # TODO: docstring
        # TODO: testing
        R = (area_t2 - area_t1) / (year_t2 - year_t1)
        return R

    @staticmethod
    def __wri_annual_deforestation(area_t1, area_t2, year_t1, year_t2):
        # TODO: docstring
        # TODO: testing
        P = (area_t2 - area_t1) / (area_t1 * (year_t2 - year_t1))
        return P
