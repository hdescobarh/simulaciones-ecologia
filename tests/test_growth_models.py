from popecology import growth_models
import pytest

# Test Growth general class


def test_valid_instance_of_growth():
    myGrowth = growth_models.Growth(100.0)
    assert myGrowth.initial_size == 100.0


def test_fails_because_of_invalid_parameter():
    with pytest.raises(Exception):
        growth_models.Growth(-100.0)


def test_fails_to_call_growth_function():
    myGrowth = growth_models.Growth(100.0)
    with pytest.raises(NotImplementedError):
        myGrowth.general_function(1)


def test_failst_to_call_growth_progression():
    myGrowth = growth_models.Growth(100.0)
    with pytest.raises(NotImplementedError):
        myGrowth.time_progression()


# test simple linear model


def test_valid_instance_of_SimpleLinear():
    initial_size = 100
    mySimpleLinear = growth_models.SimpleLinear(initial_size)
    assert mySimpleLinear.initial_size == initial_size


def test_fails_SimplLinear_growth_function():
    initial_size = 100
    slope = 5
    mySimpleLinear = growth_models.SimpleLinear(initial_size)
    with pytest.raises(Exception):
        mySimpleLinear.general_function(-1, slope)


def test_SimplLinear_growth_function():
    initial_size = 100
    slope = 4
    mySimpleLinear = growth_models.SimpleLinear(initial_size)
    assert mySimpleLinear.general_function(5, slope) == 120


def test_SimpleLinear_growth_progression():
    initial_size = 100
    commond_difference = 4
    mySimpleLinear = growth_models.SimpleLinear(initial_size)
    assert mySimpleLinear.time_progression(5, 0, 100, commond_difference) == 120
