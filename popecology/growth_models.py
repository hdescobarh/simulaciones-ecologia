# python3
# author: Hans D. Escobar. H - e-mail: escobar.hans@gmail.com


class Growth:
    """Superclass for all models of population Growth. All population must have a positive size at time = 0."""

    def __init__(self, initial_size: float) -> None:
        if initial_size <= 0:
            raise Exception("Initial size must be a positive number")
        self.initial_size = initial_size

    def general_function(self, time_point: int | float) -> float:
        """A general function f(t), such that t is time and f(t) is the size of the population at time t"""
        raise NotImplementedError

    def time_progression(self) -> float:
        """A progression in time t, where a_t is the size of the population at time t and a_t(a_{t-1})"""
        raise NotImplementedError


class SimpleLinear(Growth):
    """Describes the population growth as a linear function of the time with infinite capacity.

    Args:
        Growth (class): Superclass for all population growth models.
    """

    def __init__(self, initial_size: float, slope: float) -> None:
        super().__init__(initial_size)
        self.slope = slope

    def general_function(self, time_point: int | float) -> float:
        """Describes the population growth as a function of the time.

        Args:
            time_point (int | float): time of development from the intial obseved state
            (population size with regard an arbitary initial time = 0).

        Returns:
            float: The population size at time = time_point.
        """
        if time_point < 0:
            raise Exception("Time must be a non-negative value.")
        return self.initial_size + (self.slope * time_point)

    def time_progression(self, t_n: int, t_x: int, size_tx: float) -> float:
        """Represents the population size as a arithmetic progression:
            a_n = a_x + (n - x) * d

        Args:
            t_n (int): _description_
            t_x (int): _description_
            size_tx (float): _description_

        Returns:
            float: population size at timepoint t_n
        """
        return size_tx + (t_n - t_x) * self.slope
