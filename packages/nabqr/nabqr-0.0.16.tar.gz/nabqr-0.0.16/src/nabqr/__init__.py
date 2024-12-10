"""NABQR: Neural Additive Bayesian Quantile Regression

A method for sequential error-corrections tailored for wind power forecast in Denmark.
"""

from .nabqr import run_nabqr_pipeline
from .visualization import visualize_results
from .functions import (
    variogram_score_single_observation,
    variogram_score_R_multivariate,
    calculate_crps,
    calculate_qss,
    pipeline,
)
from .helper_functions import (
    set_n_smallest_to_zero,
    set_n_closest_to_zero,
    quantile_score,
    simulate_correlated_ar1_process,
)
from .functions_for_TAQR import (
    rq_simplex_final,
    one_step_quantile_prediction,
    run_taqr,
)

__version__ = "0.0.16"

__all__ = [
    # Main pipeline
    "run_nabqr_pipeline",
    
    # Visualization
    "visualize_results",
    
    # Core functions
    "variogram_score_single_observation",
    "variogram_score_R_multivariate",
    "calculate_crps",
    "calculate_qss",
    "pipeline",
    
    # Helper functions
    "set_n_smallest_to_zero",
    "set_n_closest_to_zero",
    "quantile_score",
    "simulate_correlated_ar1_process",
    
    # TAQR functions
    "rq_simplex_final",
    "one_step_quantile_prediction",
    "run_taqr",
]