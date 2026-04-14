import numpy as np

def locate(
        value: float,
        array : np.ndarray
) -> int:
    """
    Return index from the array's element closest to value.

    :param value: float to search
    :param array: array in which to search
    :return: array index
    """
    dist = abs(value - array)
    index = np.argmin(dist)
    return index

