# Random Number Generator

## Description
This project implements the RandomGen class, which provides functionality for generating random numbers based on specified probabilities. It is important to note that this solution is not a 'generator' in the Python technical sense. Instead, the class provides a method next_num that returns random numbers following a predefined probability distribution.

## Dependencies
- Python 3.6 or later
- SciPy (for unit testing)

Install the required dependencies using:
```
pip install -r requirements.txt
```

## Usage
To use the `RandomGen` class, initialize it with a list of numbers and their corresponding probabilities. The `next_num` method can then be called to generate random numbers based on these probabilities.

Example:
```python
from random_gen.random_gen import RandomGen

# Example initialization
random_nums = [-1, 0, 1, 2, 3]
probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
gen = RandomGen(random_nums, probabilities)

# Generate a random number
print(gen.next_num())
```

## Testing
To run the unit tests:
```
python -m unittest tests/test_random_gen.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/mmesechka/RNGWithProbabilities/blob/master/LICENSE) file for details.