import unittest
from random_gen.random_gen import RandomGen
from scipy.stats import chisquare

import time


class TestRandomGen(unittest.TestCase):
    """
    Test suite for the RandomGen class.
    """

    @staticmethod
    def generate_sample(gen: RandomGen, sample_size: int = 100000) -> dict:
        """
        Generate a sample of random numbers using the RandomGen instance.

        Args:
            gen (RandomGen): An instance of RandomGen.
            sample_size (int, optional): Number of random numbers to generate. Defaults to 100000.

        Returns:
            dict: A dictionary with counts of each generated number.
        """
        results = {num: 0 for num in gen._random_nums}
        for _ in range(sample_size):
            results[gen.next_num()] += 1
        return results

    def test_incorrect_initialization(self):
        """
        Test the initialization of RandomGen with invalid parameters.
        """
        # Test with empty list
        self.assertRaises(ValueError, RandomGen, random_nums=[])

        # Test with mismatched lengths of numbers and probabilities
        self.assertRaises(ValueError, RandomGen, random_nums=[1, 2, 3], probabilities=[0.2, 0.8])

        # Test with negative probability values
        self.assertRaises(ValueError, RandomGen, random_nums=[1, 2, 3], probabilities=[0.2, -0.2, 0.6])

        # Test with probabilities not summing to 1
        self.assertRaises(ValueError, RandomGen, random_nums=[1, 2, 3], probabilities=[0.2, 0.2, 0.2])

    def test_correct_initialization(self):
        """
        Test the correct initialization of RandomGen with valid parameters.
        """
        # Test with a specific set of numbers and probabilities
        test_gen = RandomGen([1, 2, 3, 4, 5], [0.125, 0.375, 0.25, 0.0625, 0.1875])
        self.assertEqual(test_gen._random_nums, [1, 2, 3, 4, 5])
        self.assertEqual(test_gen._probabilities, [0.125, 0.375, 0.25, 0.0625, 0.1875])
        self.assertEqual(test_gen._cumulative_probabilities, [0.125, 0.5, 0.75, 0.8125, 1.0])

        # Test initialization when no probabilities are provided
        test_gen_no_probabilities = RandomGen([1, 2, 3, 4])
        self.assertEqual(test_gen_no_probabilities._probabilities, [0.25, 0.25, 0.25, 0.25])
        self.assertEqual(test_gen_no_probabilities._cumulative_probabilities, [0.25, 0.5, 0.75, 1.0])

        # Test with a single number and no probabilities provided
        test_gen_single_element = RandomGen([5])
        self.assertEqual(test_gen_single_element._random_nums, [5])
        self.assertEqual(test_gen_single_element._probabilities, [1.0])
        self.assertEqual(test_gen_single_element._cumulative_probabilities, [1.0])

    def test_chi_square_distribution(self):
        """
        Test if the distribution of the generated numbers closely matches the expected distribution
        using the chi-square statistical test.

        The chi-square test compares the observed frequencies of the generated numbers
        against the expected frequencies (calculated from the given probabilities)
        to assess if the observed distribution deviates significantly from the expected one.

        Note to maintainers:
        When modifying random_nums, probabilities, or sample_size, ensure that:
        - All observed and expected frequencies are sufficient for a reliable chi-square test.
          Generally, each frequency should be at least 5, with a recommended minimum of 13.
          This ensures adequate statistical validity.
        - Adjustments to sample_size should maintain a balance between statistical reliability
          and computational efficiency. Larger samples improve reliability but increase computation time.
        """
        start = time.time()
        test_gen = RandomGen(random_nums=[-1, 0, 1, 2, 3], probabilities=[0.01, 0.3, 0.58, 0.1, 0.01])
        sample_size, p_value_tolerance = 50000, 0.05
        observed = self.generate_sample(test_gen, sample_size)
        observed_frequencies = [observed[num] for num in test_gen._random_nums]
        expected_frequencies = [p * sample_size for p in test_gen._probabilities]
        _, p_value = chisquare(observed_frequencies, f_exp=expected_frequencies)
        self.assertTrue(p_value > p_value_tolerance)
        end = time.time()
        print("test_chi_square_distribution: ", end - start)

    @unittest.skip("already covered in test_chi_square_distribution")
    def test_probability_distribution(self):
        """
        Test if the generated numbers follow the specified probability distribution.

        A simpler and more straightforward approach in comparison to test_chi_square_distribution (with slower execution).
        Useful when zero or close to zero probabilities need to be tested.
        """
        start = time.time()
        test_gen = RandomGen(random_nums=[-1, 0, 1, 2, 3], probabilities=[0.01, 0.3, 0.58, 0.1, 0.01])
        sample_size, tolerance = 1000000, 0.05
        results = self.generate_sample(test_gen, sample_size)
        for i, num in enumerate(test_gen._random_nums):
            expected_probability = test_gen._probabilities[i]
            observed_probability = results[num] / sample_size
            self.assertTrue(abs(expected_probability - observed_probability) <= expected_probability * tolerance)
        end = time.time()
        print("test_probability_distribution: ", end - start)

    def test_zero_probabilities(self):
        """
        Test the generation of numbers with zero probabilities.
        """
        test_gen = RandomGen(random_nums=[1, 2, 3], probabilities=[0.75, 0, 0.25])
        self.assertEqual(test_gen._cumulative_probabilities, [0.75, 0.75, 1.0])
        results = self.generate_sample(test_gen)
        self.assertEqual(results[2], 0)


if __name__ == '__main__':
    unittest.main()
