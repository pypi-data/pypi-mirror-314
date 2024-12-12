"""Test of weighted median calculations."""

import numpy as np

from gdptools.agg import stats_methods


def test_weighted_median():
    """Test weighted median calculation."""
    ndata = np.array([[1, 1, 4, 5, 8], [1, 1, np.nan, 5, 8]])
    wghts = np.array([0.4, 0.1, 0.2, 0.2, 0.1])

    # Test masked weighted median function
    masked_median = stats_methods.MAWeightedMedian(ndata, wghts, np.nan)

    np.testing.assert_allclose(masked_median.get_stat(), np.array([3.0, 3.66666667]), rtol=1e-4, verbose=True)

    # Test unmasked weighted median function
    median = stats_methods.WeightedMedian(ndata, wghts, np.nan)

    np.testing.assert_allclose(median.get_stat(), np.array([3.0, np.nan]), rtol=1e-4, verbose=True)
