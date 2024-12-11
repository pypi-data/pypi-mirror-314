# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Computation of AutoML model evaluation metrics."""
from azureml.training.tabular.score.scoring import (
    score_classification,
    score_regression,
    score_forecasting,
    aggregate_scores
)
