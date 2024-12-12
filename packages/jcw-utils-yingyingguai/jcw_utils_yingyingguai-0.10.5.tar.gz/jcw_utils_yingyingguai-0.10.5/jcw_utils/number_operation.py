from typing import Union, Tuple, List, Optional
import math

def linspace(
    start: Union[float, int],
    stop: Union[float, int],
    num: int = 50,
    endpoint: bool = True,
    retstep: bool = False,
    dtype: Optional[type] = None
) -> Union[List[float], Tuple[List[float], float]]:
    """
    仿制numpy.linspace函数，功能是完全一样的。
    endpoint:为True时，stop是最后一个值，为False时，stop不是最后一个值。
    retstep:为True时，返回一个元组，包含生成的序列和步长。
    dtype:指定返回的序列的数据类型。
    """
    if num <= 0:
        raise ValueError("num must be a positive integer.")

    if num == 1:
        result = [start]
        step = 0.0 if start == stop else stop - start
    else:
        step = (stop - start) / (num - 1) if endpoint else (stop - start) / num
        result = [start + i * step for i in range(num)]

    # Apply dtype if provided
    if dtype is not None:
        result = list(map(dtype, result))

    return (result, step) if retstep else result


