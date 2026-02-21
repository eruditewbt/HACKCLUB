"""Raw math utilities (no third-party dependencies)."""
from .algebra import add_vec, sub_vec, dot, scalar_mul, matmul, transpose, shape
from .statistics import (
    mean,
    median,
    mode,
    variance,
    stddev,
    quantile,
    zscores,
    covariance,
    correlation,
)
from .probability import factorial, ncr, npr, binomial_pmf, binomial_cdf, normal_pdf, normal_cdf
from .geometry import euclidean_distance, manhattan_distance, cosine_distance, haversine_distance
