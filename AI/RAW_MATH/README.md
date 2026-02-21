# RAW_MATH

Pure-Python math utilities.

## Modules
- `algebra.py`: Vector ops, dot, matmul, transpose, shape.
- `statistics.py`: Mean/median/mode/variance/stddev/quantile/zcov/corr.
- `probability.py`: Factorial, nCr/nPr, binomial PMF/CDF, normal PDF/CDF.
- `geometry.py`: Euclidean/Manhattan/Cosine/Haversine distances.

## Quick start
```python
from RAW_MATH import mean, stddev, haversine_distance

values = [1, 2, 3, 4]
print(mean(values), stddev(values))
print(haversine_distance(40.7, -74.0, 34.0, -118.2))
```
