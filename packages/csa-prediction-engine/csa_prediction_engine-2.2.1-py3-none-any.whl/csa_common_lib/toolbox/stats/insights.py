import numpy as np


def co_occurrence(A:np.ndarray, B: np.ndarray, 
                  mean_A: float = None, std_A: float = None, 
                  mean_B: float = None, std_B: float = None) -> float:
    """
    Calculates the informativeness-weighted co-occurrence between two
    vectors.
    
    Parameters
    ----------
    A : ndarray [N-by-1]
        Column vector.
    B : ndarray [N-by-1]
        Column vector.
    mean_A : float, optional
        Mean of vector A. If None, the mean is calculated.
    std_A : float, optional
        Standard deviation of vector A. If None, the standard deviation
        is calculated.
    mean_B : float, optional
        Mean of vector B. If None, the mean is calculated.
    std_B : float, optional
        Standard deviation of vector B. If None, the standard deviation
        is calculated.

    Returns
    -------
    float
        Informativeness-weighted co-occurrence.
    """
    
    
    # Calculate mean and standard deviation if not provided
    if mean_A is None:
        mean_A = np.mean(A)
    if std_A is None:
        std_A = np.std(A)
    if mean_B is None:
        mean_B = np.mean(B)
    if std_B is None:
        std_B = np.std(B)
    
    # Calculate z-scores for predicted and actual values
    z_A = (A - mean_A) / std_A
    z_B = (B - mean_B) / std_B
    
    # Calculate informativeness of each pair
    informativeness = 0.5 * (z_A**2 + z_B**2)
    
    # Calculate co-occurrence of each pair
    co_occurrence = (z_A * z_B) / informativeness
    
    # Calculate weights based on informativeness
    weights = informativeness / np.sum(informativeness)
    
    # Weighted co-occurrence
    weighted_co_occurrence = co_occurrence * weights
    
    # Sum of weighted co-occurrence gives the correlation coefficient
    return np.sum(weighted_co_occurrence)

