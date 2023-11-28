import random
from math import fsum, isclose


class RandomGen:
    """
    A class that generates random numbers based on specified probabilities.

    Attributes:
        _random_nums (list): List of numbers that can be randomly generated.
        _probabilities (list): List of probabilities corresponding to each number in _random_nums.
        _cumulative_probabilities (list): Cumulative probabilities to aid in number generation.
    """

    def __init__(self, random_nums: list, probabilities: list = None):
        """
        Initialize the RandomGen instance with a list of numbers and optionally their probabilities.

        Args:
            random_nums (list): List of numbers that can be randomly generated.
            probabilities (list, optional): Probabilities for each number.
                                            Defaults to None in which case equal probabilities are assigned.

        Raises:
            ValueError: If input validation fails.
        """
        self.set_random_nums(random_nums)
        self.set_probabilities(probabilities)

    def set_random_nums(self, random_nums: list):
        """
        Set the list of random numbers.

        Args:
            random_nums (list): List of numbers that can be randomly generated.

        Raises:
            ValueError: If random_nums is empty.
        """
        if not random_nums:
            raise ValueError("The list random_nums must not be empty.")
        self._random_nums = random_nums

    def set_probabilities(self, probabilities: list = None):
        """
        Set the probabilities for the random numbers.

        Args:
            probabilities (list, optional): Probabilities for each number.
                                            Defaults to None in which case equal probabilities are assigned.

        Raises:
            ValueError: If the probabilities list is invalid.
        """
        if probabilities:
            if len(self._random_nums) != len(probabilities):
                raise ValueError("The lists random_nums and probabilities must contain the same number of elements.")
            if any(p < 0 for p in probabilities):
                raise ValueError("All provided probabilities must be non-negative.")
            if not isclose(fsum(probabilities), 1.0):
                raise ValueError("The sum of the probabilities must be approximately 1.")
        else:
            # Assign equal probabilities if none are provided
            probabilities = [1 / len(self._random_nums) for _ in self._random_nums]
        self._probabilities = probabilities
        # Calculate cumulative probabilities to aid in number generation
        self._cumulative_probabilities = [fsum(self._probabilities[:i+1]) for i in range(len(self._probabilities))]

    def next_num(self):
        """
        Generate a random number based on the initialized probabilities.

        Returns:
            A random number from _random_nums list.
        """
        rand_num = random.random()
        return self._random_nums[self._find_index(rand_num)]

    def _find_index(self, rand_num):
        """
        Find the index of the cumulative probability that is greater than the given random number.

        Args:
            rand_num (float): A random number between 0 and 1.

        Returns:
            int: The index of the selected random number in _random_nums.
        """
        left, right = 0, len(self._cumulative_probabilities) - 1
        while left < right:
            mid = left + (right - left) // 2
            if self._cumulative_probabilities[mid] < rand_num:
                left = mid + 1
            else:
                right = mid
        return left
