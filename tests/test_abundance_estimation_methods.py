# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com

from popecology import abundance_estimation_methods as aem
from numpy import isnan
import pytest

# Validator


def test_validator_check_non_negative_value_raises_exception():
    with pytest.raises(Exception):
        aem.Validator.check_non_negative_value([1, 2, -5])
    with pytest.raises(Exception):
        aem.Validator.check_non_negative_value([1, 2, -5], only_positive=True)
    with pytest.raises(Exception):
        aem.Validator.check_non_negative_value([1, 2, 0], only_positive=True)
    # does not raise exception
    aem.Validator.check_non_negative_value([1, 2, 0])


# LincolnPetersen


def test_LincolnPetersen_simple():
    captured: int = 87
    recaptured_unmarked: int = 7
    recaptured_marked: int = 7
    estimator = aem.LincolnPetersen.simple_biased_statistic(
        captured, recaptured_unmarked, recaptured_marked
    )
    assert abs(estimator - 174) <= 0.0000000005


def test_LincolnPetersen_simple_zero_marked_recaptures():
    captured: int = 87
    recaptured_unmarked: int = 7
    recaptured_marked: int = 0
    estimator = aem.LincolnPetersen.simple_biased_statistic(
        captured, recaptured_unmarked, recaptured_marked
    )
    assert isnan(estimator)


def test_LincolnPetersen_bailey():
    captured: int = 87
    recaptured_unmarked: int = 7
    recaptured_marked: int = 7

    bailey_summary = aem.LincolnPetersen.bailey_unbiased_summary(
        captured, recaptured_unmarked, recaptured_marked
    )

    assert (
        abs(bailey_summary[aem.LincolnPetersen.estimator_id] - 163.125) <= 0.0000000005
    )
    assert (
        abs(bailey_summary[aem.LincolnPetersen.standard_error_id] - 37.1451965266)
        <= 0.0000000005
    )


def test_LincolnPetersen_chapman():
    captured: int = 87
    recaptured_unmarked: int = 7
    recaptured_marked: int = 7

    chapman_summary = aem.LincolnPetersen.chapman_unbiased_summary(
        captured, recaptured_unmarked, recaptured_marked
    )

    assert abs(chapman_summary[aem.LincolnPetersen.estimator_id] - 164) <= 0.0000000005
    assert (
        abs(chapman_summary[aem.LincolnPetersen.standard_error_id] - 35.8236421003)
        <= 0.0000000005
    )
