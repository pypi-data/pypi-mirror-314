# Template algorithms


def add_floats(number1: float, number2: float) -> float:
    """
    Adds two numbers together and returns the result.

    Args:
        number1 (float): The first number to add.(integer or float).
        number2 (float): The second number to add.(integer or float).

    Returns:
        float: The result of the addition of number1 and number2.
    """

    return number1 + number2


def concatenate_strings(str1: str, str2: str) -> str:
    """
    Concatenates two input strings and returns the result.

    Args:
        str1 (str): The first string to concatenate.
        str2 (str): The second string to concatenate.

    Returns:
        str: The concatenated result of str1 and str2.
    """
    return str1 + str2


def statistics_of_list(data: list) -> list:
    """
    Calculates the mean and median of a list of numbers.

    Args:
        data (list): List of numbers to calculate the statistics on.

    Returns:
        list: The calculated mean and median.
    """
    average = sum(data) / len(data)
    median = data[len(data) // 2]

    return [average, median]


def multiply_lists(list1: list, list2: list) -> list:
    """
    Multiplies two lists element-wise.

    Args:
        list1 (list): The first list to multiply.
        list2 (list): The second list to multiply.

    Returns:
        list: The element-wise multiplication of list1 and list2.
    """
    return [x * y for x, y in zip(list1, list2)]


def moving_average(data: list, periods: int = 3) -> list:
    """Defines the logic of the algorithm

    Args:
        data (list): List of numbers to calculate the moving average on.
        periods (int): Number of periods for the moving average.

    Returns:
        list: The calculated moving average.
    """
    return [
        sum(data[i : i + periods]) / periods for i in range(len(data) - periods + 1)
    ]
