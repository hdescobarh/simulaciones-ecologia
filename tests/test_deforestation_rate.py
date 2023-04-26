# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com

from landecology import deforestation_rate as dr
import pytest


# DeforestationCalculator


def test_fails_because_invalid_formula_request():
    param_1 = [39520530, 38616050, 1989, 1999]
    with pytest.raises(Exception):
        dr.DeforestationCalculator.calculate_deforestation_rate("a", *param_1)  # type: ignore


def test_raises_warning_for_time_iconsistency():
    param_1 = [39520530, 38616050, 1999, 1950]
    with pytest.raises(Warning):
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_PUYRAVAUD, *param_1
        )


def test_annual_rate_of_forest_change_puyravaud():
    delta_error = 0.00009
    param_1, output_1 = [39520530, 38616050, 1989, 1999], -0.0023
    param_2, output_2 = [7025420, 6499040, 2000, 2010], -0.0078
    param_3, output_3 = [22870, 19390, 2010, 2020], -0.0165
    param_4, output_4 = [2410, 940, 1950, 1960], -0.0942

    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_PUYRAVAUD, *param_1
        )
        - output_1
        <= delta_error
    )
    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_PUYRAVAUD, *param_2
        )
        - output_2
        <= delta_error
    )

    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_PUYRAVAUD, *param_3
        )
        - output_3
        <= delta_error
    )

    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_PUYRAVAUD, *param_4
        )
        - output_4
        <= delta_error
    )


def test_annual_rate_of_forest_change_fao():
    delta_error = 0.00009
    param_1, output_1 = [39520530, 38616050, 1989, 1999], -0.0023
    param_2, output_2 = [7025420, 6499040, 2000, 2010], -0.0078
    param_3, output_3 = [22870, 19390, 2010, 2020], -0.0164
    param_4, output_4 = [2410, 940, 1950, 1960], -0.0899

    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_FAO, *param_1
        )
        - output_1
        <= delta_error
    )
    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_FAO, *param_2
        )
        - output_2
        <= delta_error
    )

    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_FAO, *param_3
        )
        - output_3
        <= delta_error
    )

    assert (
        dr.DeforestationCalculator.calculate_deforestation_rate(
            dr.DeforestationFormula.FOREST_CHANGE_FAO, *param_4
        )
        - output_4
        <= delta_error
    )
