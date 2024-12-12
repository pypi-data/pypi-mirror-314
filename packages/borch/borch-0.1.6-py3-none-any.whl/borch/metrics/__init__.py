"""Metrics.
=======

Module implementing metrics for torch tensors

"""

from borch.metrics import metrics
from borch.metrics.rv_metrics import (
    accuracy,
    all_metrics,
    calculate_metric,
    mean_squared_error,
    module_metrics,
    suggest_metric_fns,
)
