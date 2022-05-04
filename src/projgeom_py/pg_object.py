from typing import List


def dot(a: List[int], b: List[int]) -> int:
    """_summary_

    Args:
        a (List[int]): _description_
        b (List[int]): _description_

    Returns:
        int: _description_
    """
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: List[int], b: List[int]) -> List[int]:
    """_summary_

    Args:
        a (List[int]): _description_
        b (List[int]): _description_

    Returns:
        List[int]: _description_
    """
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def plckr(ld: int, p: List[int], mu: int, q: List[int]) -> List[int]:
    """_summary_

    Args:
        ld (int): _description_
        p (List[int]): _description_
        mu (int): _description_
        q (List[int]): _description_

    Returns:
        List[int]: _description_
    """
    return [
        ld * p[0] + mu + q[0],
        ld * p[1] + mu + q[1],
        ld * p[2] + mu + q[2],
    ]
