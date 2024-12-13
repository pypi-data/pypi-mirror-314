from .functions import *
from .helper_functions import simulate_correlated_ar1_process, set_n_closest_to_zero
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["no-latex"])
from .visualization import visualize_results
import datetime as dt


def run_nabqr_pipeline(
    n_samples=2000,
    phi=0.995,
    sigma=8,
    offset_start=10,
    offset_end=500,
    offset_step=15,
    correlation=0.8,
    data_source="NABQR-TEST",
    training_size=0.7,
    epochs=20,
    timesteps=[0, 1, 2, 6, 12, 24],
    quantiles=[0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99],
    X=None,
    actuals=None,
):
    """
    Run the complete NABQR pipeline, which may include data simulation, model training,
    and visualization. The user can either provide pre-computed inputs (X, actuals)
    or opt to simulate data if both are not provided.

    Parameters
    ----------
    n_samples : int, optional
        Number of time steps to simulate if no data provided, by default 5000.
    phi : float, optional
        AR(1) coefficient for simulation, by default 0.995.
    sigma : float, optional
        Standard deviation of noise for simulation, by default 8.
    offset_start : int, optional
        Start value for offset range, by default 10.
    offset_end : int, optional
        End value for offset range, by default 500.
    offset_step : int, optional
        Step size for offset range, by default 15.
    correlation : float, optional
        Base correlation between dimensions, by default 0.8.
    data_source : str, optional
        Identifier for the data source, by default "NABQR-TEST".
    training_size : float, optional
        Proportion of data to use for training, by default 0.7.
    epochs : int, optional
        Number of epochs for model training, by default 100.
    timesteps : list, optional
        List of timesteps to use for LSTM, by default [0, 1, 2, 6, 12, 24].
    quantiles : list, optional
        List of quantiles to predict, by default [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99].
    X : array-like, optional
        Pre-computed input features. If not provided along with `actuals`, the function
        will prompt to simulate data.
    actuals : array-like, optional
        Pre-computed actual target values. If not provided along with `X`, the function
        will prompt to simulate data.

    Returns
    -------
    tuple
        A tuple containing:
        - corrected_ensembles: pd.DataFrame
            The corrected ensemble predictions.
        - taqr_results: list of numpy.ndarray
            The TAQR results.
        - actuals_output: list of numpy.ndarray
            The actual output values.
        - BETA_output: list of numpy.ndarray
            The BETA parameters.
        - scores: pd.DataFrame
            The scores for the predictions and original/corrected ensembles.

    Raises
    ------
    ValueError
        If user opts not to simulate data when both X and actuals are missing.
    """

    # If both X and actuals are not provided, ask user if they want to simulate
    if X is None or actuals is None:
        if X is not None or actuals is not None:
            raise ValueError("Either provide both X and actuals, or none at all.")
        choice = (
            input(
                "X and actuals are not provided. Do you want to simulate data? (y/n): "
            )
            .strip()
            .lower()
        )
        if choice != "y":
            raise ValueError(
                "Data was not provided and simulation not approved. Terminating function."
            )

        # Generate offset and correlation matrix for simulation
        offset = np.arange(offset_start, offset_end, offset_step)
        m = len(offset)
        corr_matrix = correlation * np.ones((m, m)) + (1 - correlation) * np.eye(m)

        # Generate simulated data
        X, actuals = simulate_correlated_ar1_process(
            n_samples, phi, sigma, m, corr_matrix, offset, smooth=5
        )

        # Plot the simulated data with X in shades of blue and actuals in bold black
        plt.figure(figsize=(10, 6))
        cmap = plt.cm.Blues
        num_series = X.shape[1] if X.ndim > 1 else 1
        colors = [cmap(i) for i in np.linspace(0.3, 1, num_series)]  # Shades of blue
        if num_series > 1:
            for i in range(num_series):
                plt.plot(X[:, i], color=colors[i], alpha=0.7)
        else:
            plt.plot(X, color=colors[0], alpha=0.7)
        plt.plot(actuals, color="black", linewidth=2, label="Actuals")
        plt.title("Simulated Data")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()
        plt.show()

    # Run the pipeline
    corrected_ensembles, taqr_results, actuals_output, BETA_output = pipeline(
        X,
        actuals,
        data_source,
        training_size=training_size,
        epochs=epochs,
        timesteps_for_lstm=timesteps,
        quantiles_taqr=quantiles,
    )

    # Get today's date for file naming
    today = dt.datetime.today().strftime("%Y-%m-%d")

    # Visualize results
    visualize_results(actuals_output, taqr_results, f"{data_source} example")

    # Calculate scores
    scores = calculate_scores(
        actuals,
        taqr_results,
        X,
        corrected_ensembles,
        quantiles,
        data_source,
        plot_reliability=True,
    )

    return corrected_ensembles, taqr_results, actuals_output, BETA_output, scores


if __name__ == "__main__":
    run_nabqr_pipeline()
