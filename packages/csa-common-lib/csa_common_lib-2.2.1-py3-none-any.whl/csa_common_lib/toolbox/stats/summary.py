"""
This module provides functions and utilities for performing statistical
analyses and generating summary tables.
"""

import numpy as np
import pandas as pd

from .insights import co_occurrence
from numpy import ndarray


def variable_importance_by_weights(combi_compound:list, X_cols:list):
    """
    Calculate a table for variable importance as a function of the grid
    cell weights. This is NOT relevance-based importance.

    Parameters
    ----------
    combi_compound : list
        List of arrays representing the weighted matrix.
    X_cols : list
        List of variable (column) names.

    Returns
    -------
    pd.DataFrame
        DataFrame containing variable importance statistics, including 
        median, standard deviation, and percentiles (5th, 20th, 50th, 80th, 95th).
    """
    
    
    # Convert the list of arrays into a 2D NumPy array
    combi_compound = np.vstack(combi_compound)
    
    # Calculate medians, standard deviations, and percentiles for each column
    medians = np.median(combi_compound, axis=0)
    std_devs = np.std(combi_compound, axis=0)
    percentiles = {
        '5th Percentile': np.percentile(combi_compound, 5, axis=0),
        '20th Percentile': np.percentile(combi_compound, 20, axis=0),
        '50th Percentile': np.percentile(combi_compound, 50, axis=0),
        '80th Percentile': np.percentile(combi_compound, 80, axis=0),
        '95th Percentile': np.percentile(combi_compound, 95, axis=0),
    }
    
    # Create a DataFrame of results sorted by the highest medians
    result = {
        'Median': medians,
        'Std Dev': std_devs
    }
    result.update(percentiles)
    
    return pd.DataFrame(result, index=X_cols).sort_values(by='Median', ascending=False)


def tstats_and_betas(yhats:ndarray, y_actuals:ndarray, y_linear:ndarray, 
                     fits:ndarray, percentile_low:int=20, percentile_high:int=80):
    """
    Calculate and return a table of beta coefficients and t-statistics 
    for subsamples of high, mid, and low fit.

    Parameters
    ----------
    yhats : ndarray [N-by-1]
        Column vector of relevance-based prediction outcomes.
    y_actuals : ndarray [N-by-1]
        Column vector of realized dependent variable outcomes for 
        comparison with prediction outcomes.
    y_linear : ndarray [N-by-1]
        Column vector of standard linear regression prediction outcomes.
    fits : ndarray [N-by-1]
        Prediction fit scores.
    percentile_low : int, optional
        The lower percentile cutoff for subsampling, by default 20.
    percentile_high : int, optional
        The upper percentile cutoff for subsampling, by default 80.

    Returns
    -------
    pd.DataFrame
        DataFrame containing beta coefficients and t-statistics for linear 
        and excess RBP components at various levels of fit.
    """
    
    
    # Convert inputs to arrays
    yhats = np.array(yhats)
    y_actuals = np.array(y_actuals)
    y_linear = np.array(y_linear)
    fits = np.array(fits)
    
    # Get high, mid, and low fits based on percentiles
    high_fits, mid_fits, low_fits = split_data_by_percentile(fits, percentile_low, percentile_high)
    
    # Block 1: Full sample analysis
    full_sample = linear_component_analysis(yhats, y_actuals, y_linear)
    
    # Block 2: High fit sample analysis
    high_fit = linear_component_analysis(
        yhats[high_fits], 
        y_actuals[high_fits], 
        y_linear[high_fits]
    )
    
    # Block 3: Mid fit sample analysis
    mid_fit = linear_component_analysis(
        yhats[mid_fits], 
        y_actuals[mid_fits], 
        y_linear[mid_fits]
    )
    
    # Block 4: Low fit sample analysis
    low_fit = linear_component_analysis(
        yhats[low_fits], 
        y_actuals[low_fits], 
        y_linear[low_fits]
    )
    
    # Compile results into a DataFrame
    results = {
        'Full Sample Linear Component': [full_sample['beta_linear'], full_sample['t_linear']],
        'Full Sample Excess RBP Component': [full_sample['beta_nonlinear'], full_sample['t_nonlinear']],
        'High Fit Sample Linear Component': [high_fit['beta_linear'], high_fit['t_linear']],
        'High Fit Sample Excess RBP Component': [high_fit['beta_nonlinear'], high_fit['t_nonlinear']],
        'Mid Fit Sample Linear Component': [mid_fit['beta_linear'], mid_fit['t_linear']],
        'Mid Fit Sample Excess RBP Component': [mid_fit['beta_nonlinear'], mid_fit['t_nonlinear']],
        'Low Fit Sample Linear Component': [low_fit['beta_linear'], low_fit['t_linear']],
        'Low Fit Sample Excess RBP Component': [low_fit['beta_nonlinear'], low_fit['t_nonlinear']]
    }
    
    return pd.DataFrame(results, index=['Beta', 'T-Statistic'])


def y_actual_means(yhats:ndarray, y_actuals:ndarray, fits:ndarray, 
                   percentile_low:int=20, percentile_high:int=80):
    """
    Calculate the mean of actual values (`y_actuals`) at high and low 
    prediction (`yhats`) and fit (`fits`) levels.

    Parameters
    ----------
    yhats : ndarray [N-by-1]
        Column vector of relevance-based prediction outcomes.
    y_actuals : ndarray [N-by-1]
        Column vector of realized dependent variable outcomes for 
        comparison with prediction outcomes.
    fits : ndarray [N-by-1]
        Prediction fit scores.
    percentile_low : int, optional
        The lower percentile cutoff for subsampling, by default 20.
    percentile_high : int, optional
        The upper percentile cutoff for subsampling, by default 80.

    Returns
    -------
    pd.DataFrame
        Table containing mean `y_actual` values at varying levels of 
        prediction and fit.
    """
    
    
    # Convert inputs to arrays
    yhats = np.array(yhats)
    y_actuals = np.array(y_actuals)
    fits = np.array(fits)
    
    # Get high and low yhat indices based on percentiles
    high_yhats, _, low_yhats = split_data_by_percentile(yhats, percentile_low, percentile_high)
    
    # Block 1: Full sample mean
    full_sample = np.mean(y_actuals)
    
    # Block 2: High yhat sample analysis
    y_actuals_high_yhat = y_actuals[high_yhats]
    fits_high_yhat = fits[high_yhats]
    high_pred = np.mean(y_actuals_high_yhat)
    
    # Get high and low fits for high yhat
    high_fits, _, low_fits = split_data_by_percentile(fits_high_yhat, percentile_low, percentile_high)
    high_pred_w_high_fit = np.mean(y_actuals_high_yhat[high_fits])
    high_pred_w_low_fit = np.mean(y_actuals_high_yhat[low_fits])
    
    # Block 3: Low yhat sample analysis
    y_actuals_low_yhat = y_actuals[low_yhats]
    fits_low_yhat = fits[low_yhats]
    low_pred = np.mean(y_actuals_low_yhat)
    
    # Get high and low fits for low yhat
    high_fits, _, low_fits = split_data_by_percentile(fits_low_yhat, percentile_low, percentile_high)
    low_pred_w_high_fit = np.mean(y_actuals_low_yhat[high_fits])
    low_pred_w_low_fit = np.mean(y_actuals_low_yhat[low_fits])
    
    # Create the result DataFrame
    results = {
        'Full Sample': full_sample,
        'High Prediction': high_pred,
        'High Prediction w/ High Fit': high_pred_w_high_fit,
        'High Prediction w/ Low Fit': high_pred_w_low_fit,
        'Low Prediction': low_pred,
        'Low Prediction w/ High Fit': low_pred_w_high_fit,
        'Low Prediction w/ Low Fit': low_pred_w_low_fit
    }
    
    return pd.DataFrame(results, index=['Y Actual Mean']).T


def split_data_by_percentile(data:ndarray, percentile_low:int=20, 
                             percentile_high:int=80):
    """
    Determine the indices for high, mid, and low ranges based 
    on the specified percentiles cutoffs.

    Parameters
    ----------
    data : ndarray
        The data for which the percentile cutoffs are calculated.
    percentile_low : int, optional
        The lower percentile cutoff for low data, by default 20.
    percentile_high : int, optional
        The upper percentile cutoff for high data, by default 80.

    Returns
    -------
    tuple of np.ndarray
        - high_indexes : ndarray
            Indices of data values that fall in the high percentile range.
        - mid_indexes : ndarray
            Indices of data values that fall in the mid percentile range.
        - low_indexes : ndarray
            Indices of data values that fall in the low percentile range.
    """
    
    
    data = np.array(data)  # Ensure the input is a numpy array
    high_value = np.percentile(data, percentile_high)
    low_value = np.percentile(data, percentile_low)
    
    high_indexes = np.where(data >= high_value)[0]
    low_indexes = np.where(data <= low_value)[0]
    mid_indexes = np.where((data > low_value) & (data < high_value))[0]
    
    return high_indexes, mid_indexes, low_indexes


def co_occurrence_summary(yhat:ndarray, y_actual:ndarray, fits:ndarray, 
                         percentile_low:int = 20, percentile_high:int = 80) -> pd.DataFrame:
    """
    Generates a summary table of Informativeness-weighted Co-occurrence (IWCO)
    values for yhat and y_actual at different levels of fit and prediction.

    Parameters
    ----------
    yhats : ndarray [N-by-1]
        Column vector of relevance-based prediction outcomes.
    y_actuals : ndarray [N-by-1]
        Column vector of realized dependent variable outcomes for 
        comparison with prediction outcomes.
    fits : ndarray [N-by-1]
        Prediction fit scores.
    percentile_low : int, optional
        Lower percentile cutoff for categorizing high, mid, and low groups. 
        Default is 20.
    percentile_high : int, optional
        Upper percentile cutoff for categorizing high, mid, and low groups. 
        Default is 80.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing IFWCO values for yhat and y_actual at 
        various levels of fit and predictions.
    """
    
    # Convert inputs to numpy arrays
    yhat = np.array(yhat)
    y_actual = np.array(y_actual)
    fits = np.array(fits)

    # Split data by percentiles
    high_yhat_indices, _, low_yhat_indices = \
        split_data_by_percentile(yhat, percentile_low, percentile_high)
        
    high_fit_indices, _, low_fit_indices = \
        split_data_by_percentile(fits, percentile_low, percentile_high)

    # Calculate means and standard deviations for the full sample
    mean_yhat, std_yhat = np.mean(yhat), np.std(yhat)
    mean_y_actual, std_y_actual = np.mean(y_actual), np.std(y_actual)

    # Full sample IWCO
    iwco_fullsample = co_occurrence(yhat, y_actual, mean_yhat, std_yhat, 
                                      mean_y_actual, std_y_actual)

    # High fit IWCO
    iwco_highfit = co_occurrence(
        yhat[high_fit_indices], y_actual[high_fit_indices], 
        mean_yhat, std_y_actual, mean_y_actual, std_y_actual
    )

    # Low fit IWCO
    iwco_lowfit = co_occurrence(
        yhat[low_fit_indices], y_actual[low_fit_indices], 
        mean_yhat, std_yhat, mean_y_actual, std_y_actual
    )

    # High prediction IFWCO calculations
    high_predictions, high_predictions_high_fit, high_predictions_low_fit = \
        _calculate_cooccurrence_by_prediction_group(yhat, y_actual, fits, 
                                                    high_yhat_indices, 
                                                    percentile_low, percentile_high)

    # Low prediction IFWCO calculations
    low_predictions, low_predictions_high_fit, low_predictions_low_fit = \
        _calculate_cooccurrence_by_prediction_group(yhat, y_actual, fits, 
                                                    low_yhat_indices, 
                                                    percentile_low, percentile_high)

    # Set up results table
    results = {
        'Full Sample': iwco_fullsample,
        'High Fit': iwco_highfit,
        'Low Fit': iwco_lowfit,
        'High Prediction': high_predictions,
        'High Prediction w/ High Fit': high_predictions_high_fit,
        'High Prediction w/ Low Fit': high_predictions_low_fit,
        'Low Prediction': low_predictions,
        'Low Prediction w/ High Fit': low_predictions_high_fit,
        'Low Prediction w/ Low Fit': low_predictions_low_fit
    }

    return pd.DataFrame(results, index=['Informativeness-Weighted Co-Occurrence']).T


def _calculate_cooccurrence_by_prediction_group(yhat:ndarray,
        y_actual:ndarray, fits:ndarray, group_indices:ndarray, 
        percentile_low:int=20, percentile_high:int=80) -> tuple:
    """
    Calculates the informativeness-weighted co-occurrence (IWCO) values
    by high and low prediction value groups and by high and low fit 
    subgroups.

    Parameters
    ----------
    yhats : ndarray [N-by-1]
        Column vector of relevance-based prediction outcomes.
    y_actuals : ndarray [N-by-1]
        Column vector of realized dependent variable outcomes for 
        comparison with prediction outcomes.
    fits : ndarray [N-by-1]
        Prediction fit scores.
    group_indices : ndarray [N-by-1]
        Indices representing the specific group (e.g., high or low yhat) 
        to be analyzed.
    percentile_low : int
        Lower percentile cutoff for categorizing high and low fit subgroups.
    percentile_high : int
        Upper percentile cutoff for categorizing high and low fit subgroups.

    Returns
    -------
    tuple
        Tuple containing IWCO values for:
        - IWCO, full sample
        - IWCO, high fit subgroup
        - IWCO, low fit subgroup
    """

    # Filter yhat, y_actual, and fits based on group indices
    group_yhat = yhat[group_indices]
    group_y_actual = y_actual[group_indices]
    group_fits = fits[group_indices]
    
    # Calculate mean and standard deviation for the group
    mean_yhat = np.mean(group_yhat)
    std_yhat = np.std(group_yhat)
    mean_y_actual = np.mean(group_y_actual)
    std_y_actual = np.std(group_y_actual)

    # Calculate IFWCO for the full group
    iwco_fullsample = co_occurrence(group_yhat, group_y_actual, 
                                     mean_yhat, std_yhat, 
                                     mean_y_actual, std_y_actual)

    # Further split group into high fit and low fit subgroups
    high_fit_indices, _, low_fit_indices = split_data_by_percentile(
        group_fits, percentile_low, percentile_high)
    
    # Calculate IFWCO for high fit subgroup
    iwco_highfit = co_occurrence(
        group_yhat[high_fit_indices], 
        group_y_actual[high_fit_indices], 
        mean_yhat, std_yhat, mean_y_actual, std_y_actual
    )

    # Calculate IFWCO for low fit subgroup
    iwco_lowfit = co_occurrence(group_yhat[low_fit_indices], 
                                  group_y_actual[low_fit_indices], 
                                  mean_yhat, std_yhat, 
                                  mean_y_actual, std_y_actual
    )

    return iwco_fullsample, iwco_highfit, iwco_lowfit


def linear_component_analysis(yhats:ndarray, y_actuals:ndarray, y_linear:ndarray) -> dict:
    """
    Analyzes the linear and non-linear components of the model by 
    calculating coefficients and t-statistics.

    Parameters
    ----------
    yhats : ndarray [N-by-1]
        Column vector of relevance-based prediction outcomes.
    y_actuals : ndarray [N-by-1]
        Column vector of realized dependent variable outcomes for 
        comparison with prediction outcomes.
    y_linear : ndarray [N-by-1]
        Column vector of standard linear regression prediction outcomes.

    Returns
    -------
    dict
        Dictionary containing linear component analysis results including 
        coefficients and t-statistics for linear and non-linear parts.
    """


    # Variable assignments: yhat = B1 * y_linear + B2 * (yhat - y_linear)
    x1 = np.array(y_linear)
    x2 = np.array(yhats) - x1
    y = np.array(y_actuals)

    # Sum of squares and products required for regression calculations
    ssx1 = np.sum(x1 ** 2)
    ssx2 = np.sum(x2 ** 2)
    sx1x2 = np.sum(x1 * x2)
    syx1 = np.sum(y * x1)
    syx2 = np.sum(y * x2)

    # Setting up the xTx matrix and calculating its inverse
    xTx = np.array([[ssx1, sx1x2], [sx1x2, ssx2]])
    det_xTx = np.linalg.det(xTx)
    xTx_inverse = np.array([[ssx2, -sx1x2], [-sx1x2, ssx1]]) / det_xTx

    # Calculating coefficients b1 and b2 using xTx inverse
    b1 = (ssx2 * syx1 - sx1x2 * syx2) / det_xTx
    b2 = (ssx1 * syx2 - sx1x2 * syx1) / det_xTx

    # Degrees of freedom
    df = y.shape[0] - 2

    # Predicted values and residuals
    pred_values = b1 * x1 + b2 * x2
    residuals = y - pred_values

    # Error term variance
    rss = np.sum(residuals ** 2)
    error_variance = rss / df

    # Variance-covariance matrix
    varcovar = error_variance * xTx_inverse

    # Calculating t-statistics for b1 and b2
    t_b1 = b1 / np.sqrt(varcovar[0, 0])
    t_b2 = b2 / np.sqrt(varcovar[1, 1])

    # Returning the analysis results in a dictionary
    return {
        'beta_linear': b1,
        'beta_nonlinear': b2,
        't_linear': t_b1,
        't_nonlinear': t_b2
    }


def model_analysis(yhats:ndarray, y_actuals:ndarray, y_linear:ndarray, 
                   fits:ndarray, combi_compound:list, X_cols:list=None, 
                   percentile_low:int=20, percentile_high:int=80):
    """
    Analyzes model performance by computing various metrics including 
    average Y for low/high yHat and fit, informativeness-weighted 
    co-occurrence, and regression coefficients of the linear and 
    non-linear components.

    Parameters
    ----------
    yhats : ndarray [N-by-1]
        Column vector of relevance-based prediction outcomes.
    y_actuals : ndarray [N-by-1]
        Column vector of realized dependent variable outcomes for 
        comparison with prediction outcomes.
    y_linear : ndarray [N-by-1]
        Column vector of standard linear regression prediction outcomes.
    fits : ndarray [N-by-1]
        Prediction fit scores.
    combi_compound : list
        Array of weighted matrix for variable importance analysis.
    X_cols : list, optional
        Array of variable (column) names. Defaults to None.
    percentile_low : int, optional
        Lower percentile cutoff for high/low splits. Defaults to 20.
    percentile_high : int, optional
        Upper percentile cutoff for high/low splits. Defaults to 80.

    Returns
    -------
    list
        List of pandas DataFrames containing summary statistics for 
        the given prediction analysis.
    """

    # If no column names are provided, use default range
    if X_cols is None:
        X_cols = list(range(len(combi_compound)))

    # Create the analysis tables
    y_actual_mean = y_actual_means(yhats, y_actuals, fits, percentile_low, percentile_high)
    ifwco = co_occurrence_summary(yhats, y_actuals, fits, percentile_low, percentile_high)
    lca = tstats_and_betas(yhats, y_actuals, y_linear, fits, percentile_low, percentile_high)
    var_importance = variable_importance_by_weights(combi_compound=combi_compound, X_cols=X_cols)

    # Pack the tables together in a list and return
    results_list = [y_actual_mean, ifwco, lca, var_importance]

    return results_list