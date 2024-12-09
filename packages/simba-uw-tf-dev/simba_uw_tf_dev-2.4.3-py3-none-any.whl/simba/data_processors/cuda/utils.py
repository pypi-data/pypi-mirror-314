import math
from typing import Any, Dict, Tuple

import numpy as np
from numba import cuda, float64, guvectorize



@cuda.jit(device=True)
def _cuda_sum(x: np.ndarray):
    s = 0
    for i in range(x.shape[0]):
        s += x[i]
    return s

@cuda.jit(device=True)
def _cuda_sin(x, t):
    for i in range(x.shape[0]):
        v = math.sin(x[i])
        t[i] = v
    return t

@cuda.jit(device=True)
def _cuda_cos(x, t):
    for i in range(x.shape[0]):
        v = math.cos(x[i])
        t[i] = v
    return t

@cuda.jit(device=True)
def _cuda_std(x: np.ndarray, x_hat: float):
    std = 0
    for i in range(x.shape[0]):
        std += (x[0] - x_hat) ** 2
    return std

@cuda.jit(device=True)
def _rad2deg(x):
    return x * (180/math.pi)

@cuda.jit(device=True)
def _deg2rad(x):
    return x * (math.pi/180)

@cuda.jit(device=True)
def _cross_test(x, y, x1, y1, x2, y2):
    cross = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
    return cross < 0


@cuda.jit(device=True)
def _cuda_mean(x):
    s = 0
    for i in range(x.shape[0]):
        s += x[i]
    return s / x.shape[0]

@cuda.jit(device=True)
def _cuda_mse(img_1, img_2):
    s = 0.0
    for i in range(img_1.shape[0]):
        for j in range(img_1.shape[1]):
            k = (img_1[i, j] - img_2[i, j]) ** 2
            s += k
    return s / (img_1.shape[0] * img_1.shape[1])


@cuda.jit(device=True)
def _cuda_luminance_pixel_to_grey(r: int, g: int, b: int):
    r = 0.2126* r
    g = 0.7152 * g
    b = 0.0722 * b
    return b + g + r

@cuda.jit(device=True)
def _cuda_digital_pixel_to_grey(r: int, g: int, b: int):
    r = 0.299 * r
    g = 0.587 * g
    b = 0.114 * b
    return b + g + r

@cuda.jit(device=True)
def _euclid_dist(x, y):
    return math.sqrt(((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2))

@cuda.jit(device=True)
def _cuda_matrix_multiplication(mA, mB, out):
    """ Matrix multiplication"""
    for i in range(mA.shape[0]):
        for j in range(mB.shape[1]):
            for k in range(mA.shape[1]):
                out[i][j] += mA[i][k] * mB[k][j]
    return out

@cuda.jit(device=True)
def _cuda_2d_transpose(x, y):
    """ Transpose a 2d array """
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            y[j][i] = x[i][j]
    return y

@cuda.jit(device=True)
def _cuda_subtract_2d(x: np.ndarray, vals: np.ndarray) -> np.ndarray:
    """ Subtract 1d array values for every row in a 2d array"""
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i][j] = x[i][j] - vals[j]
    return x


@cuda.jit(device=True)
def _cuda_add_2d(x: np.ndarray, vals: np.ndarray) -> np.ndarray:
    """ Add 1d array values for every row in a 2d array"""
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i][j] = x[i][j] + vals[j]
    return x

def _cuda_available() -> Tuple[bool, Dict[int, Any]]:
    """
    Check if GPU available. If True, returns the GPUs, the model, physical slots and compute capabilitie(s).

    :return: Two-part tuple with first value indicating with the GPU is available (bool) and the second value denoting GPU attributes (dict).
    :rtype: Tuple[bool, Dict[int, Any]]
    """
    is_available = cuda.is_available()
    devices = None
    if is_available:
        devices = {}
        for gpu_cnt, gpu in enumerate(cuda.gpus):
            devices[gpu_cnt] = {'model': gpu.name.decode("utf-8"),
                                'compute_capability': float("{}.{}".format(*gpu.compute_capability)),
                                'id': gpu.id,
                                'PCI_device_id': gpu.PCI_DEVICE_ID,
                                'PCI_bus_id': gpu.PCI_BUS_ID}

    return is_available, devices


# @guvectorize([(float64[:], float64[:])], '(n) -> (n)', target='cuda')
# def _cuda_bubble_sort(arr, out):
#     """
#     :example:
#     >>> a = np.random.randint(5, 50, (5, 200)).astype('float64')
#     >>> d_a = cuda.to_device(a)
#     >>> _cuda_bubble_sort(d_a)
#     >>> d = d_a.copy_to_host()
#     """
#
#     for i in range(len(arr)):
#         for j in range(len(arr) - 1 - i):
#             if arr[j] > arr[j + 1]:
#                 arr[j], arr[j + 1] = arr[j + 1], arr[j]
#     out = arr