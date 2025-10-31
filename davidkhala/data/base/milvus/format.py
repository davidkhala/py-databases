from typing import Union

import numpy as np


def normalize_vector(vec:Union[np.ndarray, list]) -> np.ndarray:
    """
    L2 normalize
    """
    vec = np.array(vec, dtype=np.float32)
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("输入向量的模长为 0，无法归一化")
    return vec / norm