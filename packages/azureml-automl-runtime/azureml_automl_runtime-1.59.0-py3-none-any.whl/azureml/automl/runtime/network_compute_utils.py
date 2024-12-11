# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Network & compute related utility methods for the package."""

import json
import logging
import os

from typing import Optional

from azureml.automl.core.constants import RunHistoryEnvironmentVariableNames
from azureml.core.run import Run
from azureml.automl.core.shared import logging_utilities

logger = logging.getLogger(__name__)


def get_vnet_name(cluster_name: Optional[str]) -> Optional[str]:
    """
    Return the name of vnet (if set) for current workspace and compute that is used for the run
    in context. Return None otherwise.

    :param cluster_name: name of compute cluster, possibly lower-cased.
    :return: Name of vnet.
    :rtype: str
    """
    vnet_name = None
    if cluster_name is not None:
        try:
            azureml_run = Run.get_context()
            workspace = azureml_run.experiment.workspace
            # Beware of exact match check due to casing.
            compute_targets = {k.lower(): v for k, v in workspace.compute_targets.items() if isinstance(k, str)}
            vnet_name = compute_targets[cluster_name.lower()].vnet_name
        except Exception as ex:
            logger.warning("Encountered error while getting vnet name from current run.")
            logging_utilities.log_traceback(ex, logger, is_critical=False)
    return vnet_name


def get_cluster_name() -> Optional[str]:
    """
    Return the name of compute cluster that is used for the run in context.

    :return: Name of compute cluster.
    :rtype: str
    """
    cluster_name = None
    try:
        compute_context = os.environ.get(RunHistoryEnvironmentVariableNames.AZUREML_CR_COMPUTE_CONTEXT, "")
        compute_context_dict = json.loads(compute_context)
        cluster_name = compute_context_dict["cluster_name"]
    except Exception as ex:
        logger.warning("Encountered error while getting compute cluster name.")
        logging_utilities.log_traceback(ex, logger, is_critical=False)
    return cluster_name
