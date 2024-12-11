# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import Any, Callable, Dict, List, Optional
import logging
import psutil
import threading

from azureml.train.automl.runtime._dask.mpi_dask_cluster import MpiDaskCluster
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings

logger = logging.getLogger(__name__)


class DaskJob:

    @staticmethod
    def run(
            driver_func: Callable[..., Any],
            azure_automl_settings: AzureAutoMLSettings,
            driver_func_args: List[Optional[Any]] = [],
            driver_func_kwargs: Dict[str, Any] = {},
            worker_per_core: bool = True,
    ) -> Any:
        """Initialize a Dask cluster and run the driver function on it."""
        cluster = MpiDaskCluster()
        cpu_count = max(1, psutil.cpu_count())
        # If the task type is forecasting, we allow workers on rank 0.
        # Also, we create upto 1 worker per CPU core. On rank 0,
        # number of workers will be CPU_CORE_COUNT - 2. This is done to leave
        # room for 2 processes- dask scheduler and the main script.
        if azure_automl_settings.is_timeseries:
            start_worker_on_rank_0 = True
            max_worker_count = cpu_count
        else:
            start_worker_on_rank_0 = False
            max_worker_count = int(max(1, cpu_count / 4))
        rank = cluster.start(max_worker_count, worker_per_core, start_worker_on_rank_0)

        try:
            # Only run the driver function on rank 0
            if rank == "0":
                return driver_func(*driver_func_args, **driver_func_kwargs)
        except Exception as e:
            logger.error(f"Failure during dask job: {type(e)}")
            raise
        finally:
            if rank == "0":
                logger.info("Shutting down dask cluster.")
                shutdown_thread = threading.Thread(target=lambda c: c.shutdown(), args=(cluster,))
                shutdown_thread.start()
                shutdown_thread.join(timeout=10)
                if shutdown_thread.is_alive():
                    logger.info("Failed to shut down dask cluster.")
                else:
                    logger.info("Successfully shut down dask cluster.")
