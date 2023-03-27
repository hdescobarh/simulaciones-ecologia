from popecology import abundance_estimation_population_models as aspm
import pytest

# Test SamplingPopulation superclass


def test_correct_initialization_SamplingPopulation():
    initial_size: int = 5
    mySamplingPopulation = aspm.SamplingPopulation(initial_size)
    assert mySamplingPopulation.initial_size == initial_size


def test_fails_to_create_SamplingPopulation():
    with pytest.raises(Exception):
        aspm.SamplingPopulation(0)
    with pytest.raises(Exception):
        aspm.SamplingPopulation(-1)


# Test CmrPopulation creation


def test_create_CmrPopulation_instance():
    aspm.CmrPopulation(
        initial_size=10,
        capture_distribution=(0.5, 1),
        death_distribution=(0.5, 0),
        inmigration_rate=10000,
        mark_lost_probability=1.0,
    )

    aspm.CmrPopulation(
        initial_size=1,
        capture_distribution=(0, 0),
        death_distribution=(0, 0),
        inmigration_rate=0,
        mark_lost_probability=0,
    )


def test_create_CmrPopulation_instance_with_correct_parameters_assingment():
    initial_size = 10
    capture_distribution = (0.5, 0.1)
    death_distribution = (0.5, 0.3)
    inmigration_rate = 10000
    mark_lost_probability = 0.3

    myCmrPopulation = aspm.CmrPopulation(
        initial_size,
        capture_distribution,
        death_distribution,
        inmigration_rate,
        mark_lost_probability,
    )
    assert myCmrPopulation.initial_size == initial_size
    assert myCmrPopulation._current_unmarked == initial_size
    assert myCmrPopulation._current_marked == 0
    assert myCmrPopulation._current_time_step == 0
    assert myCmrPopulation._capture_distribution == capture_distribution
    assert myCmrPopulation._death_distribution == death_distribution
    assert myCmrPopulation._inmigration_rate == inmigration_rate
    assert myCmrPopulation._mark_lost_probability == mark_lost_probability


def test_fails_to_create_CmrPopulation_invalid_capture_distribution():
    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(-0.5, 0.5),
            death_distribution=(0.5, 0.5),
            inmigration_rate=0,
            mark_lost_probability=0,
        )
    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(0.5, 15),
            death_distribution=(0.5, 0.5),
            inmigration_rate=0,
            mark_lost_probability=0,
        )


def test_fails_to_create_CmrPopulation_invalid_death_distribution():
    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(0.5, 0.5),
            death_distribution=(5, 0.5),
            inmigration_rate=0,
            mark_lost_probability=0,
        )
    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(0.5, 0.5),
            death_distribution=(0.5, -1),
            inmigration_rate=0,
            mark_lost_probability=0,
        )


def test_fails_to_create_CmrPopulation_invalid_inmigration_rate():
    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(0.5, 0.5),
            death_distribution=(0.5, 0.5),
            inmigration_rate=-30,
            mark_lost_probability=0,
        )


def test_fails_to_create_CmrPopulation_invalid_mark_lost_probability():
    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(0.5, 0.5),
            death_distribution=(0.5, 0.5),
            inmigration_rate=0,
            mark_lost_probability=-1,
        )

    with pytest.raises(Exception):
        aspm.CmrPopulation(
            initial_size=10,
            capture_distribution=(0.5, 0.5),
            death_distribution=(0.5, 0.5),
            inmigration_rate=0,
            mark_lost_probability=11,
        )


# Test CmrPopulaton methods


def test_CmrPopulation_sample_and_mark_fails_for_invalid_size():
    myPopulation = aspm.CmrPopulation(
        initial_size=5,
        capture_distribution=(1, 0.5),
        death_distribution=(0.5, 0.5),
        inmigration_rate=0,
        mark_lost_probability=0,
    )
    with pytest.raises(Exception):
        myPopulation.sample_and_mark(10)


def test_CmrPopulation_sample_and_mark_sample_size_equals_to_pop_size():
    myPopulation = aspm.CmrPopulation(
        initial_size=10,
        capture_distribution=(1, 0.5),
        death_distribution=(0.5, 0.5),
        inmigration_rate=0,
        mark_lost_probability=0,
    )
    myPopulation.sample_and_mark(10)
    assert myPopulation._current_unmarked == 0


def test_CmrPopulation_sample_and_mark_cannot_capture_unmarked():
    myPopulation = aspm.CmrPopulation(
        initial_size=15,
        capture_distribution=(0, 1),
        death_distribution=(0.5, 0.5),
        inmigration_rate=0,
        mark_lost_probability=0,
    )
    myPopulation.sample_and_mark(10)
    assert myPopulation._current_unmarked == 15
