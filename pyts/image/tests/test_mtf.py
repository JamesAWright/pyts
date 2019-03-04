"""Testing for Markov Transition Field."""

import numpy as np
from itertools import product
from ..mtf import (_markov_transition_matrix,
                   _markov_transition_field,
                   _aggregated_markov_transition_field,
                   MarkovTransitionField)


def test_markov_transition_matrix():
    """Test '_markov_transition_matrix' function."""
    X_binned = np.asarray([[0, 1, 2, 3],
                           [0, 2, 1, 3]])
    n_samples = 2
    n_timestamps = 4
    n_bins = 5

    arr_actual = _markov_transition_matrix(
        X_binned, n_samples, n_timestamps, n_bins
    )
    arr_desired = np.empty((n_samples, n_bins, n_bins))
    arr_desired[0] = [[0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    arr_desired[1] = [[0, 0, 1, 0, 0],
                      [0, 0, 0, 1, 0],
                      [0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    np.testing.assert_array_equal(arr_actual, arr_desired)


def test_markov_transition_field():
    """Test '_markov_transition_field' function."""
    n_samples = 2
    n_timestamps = 5
    n_bins = 3

    X_binned = np.asarray([[0, 1, 2, 0, 1],
                           [0, 2, 0, 1, 1]])

    X_mtm = np.empty((n_samples, n_bins, n_bins))
    X_mtm[0] = [[0, 1, 0],
                [0, 0, 1],
                [1, 0, 0]]
    X_mtm[1] = [[0.0, 0.5, 0.5],
                [0.0, 1.0, 0.0],
                [1.0, 0.0, 0.0]]

    arr_actual = _markov_transition_field(
        X_binned, X_mtm, n_samples, n_timestamps, n_bins
    )
    arr_desired = np.empty((n_samples, n_timestamps, n_timestamps))
    arr_desired[0] = [[0, 1, 0, 0, 1],
                      [0, 0, 1, 0, 0],
                      [1, 0, 0, 1, 0],
                      [0, 1, 0, 0, 1],
                      [0, 0, 1, 0, 0]]
    arr_desired[1] = [[0.0, 0.5, 0.0, 0.5, 0.5],
                      [1.0, 0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.5, 0.0, 0.5, 0.5],
                      [0.0, 0.0, 0.0, 1.0, 1.0],
                      [0.0, 0.0, 0.0, 1.0, 1.0]]
    np.testing.assert_array_equal(arr_actual, arr_desired)


def test_aggregated_markov_transition_field():
    """Test 'aggregated_markov_transition_field' function."""
    n_samples = 2
    n_timestamps = 4
    image_size = 2
    start = [0, 2]
    end = [2, 4]
    X_mtf = np.empty((n_samples, n_timestamps, n_timestamps))
    X_mtf[0] = np.asarray([[0, 1, 2, 0],
                           [1, 0, 2, 0],
                           [1, 1, 0, 0],
                           [0, 1, 2, 2]])
    X_mtf[1] = np.asarray([[2, 1, 2, 0],
                           [0, 1, 3, 0],
                           [0, 1, 2, 0],
                           [0, 0, 0, 0]])

    arr_actual = _aggregated_markov_transition_field(
        X_mtf, n_samples, image_size, start, end
    )
    arr_desired = np.empty((n_samples, image_size, image_size))
    arr_desired[0] = np.asarray([[0.5, 1.0],
                                 [0.75, 1.0]])
    arr_desired[1] = np.asarray([[1.0, 1.25],
                                 [0.25, 0.5]])
    np.testing.assert_array_equal(arr_actual, arr_desired)


def test_MarkovTransitionField():
    """Test 'MarkovTransitionField' class."""
    X = np.tile(np.arange(8), 2).reshape(2, 8)

    # Parameter check
    def type_error_list():
        type_error_list_ = [
            "'image_size' must be an integer or a float.",
            "'n_bins' must be an integer."
        ]
        return type_error_list_

    def value_error_list(image_size):
        value_error_list_ = [
            "If 'image_size' is an integer, it must be greater "
            "than or equal to 1 and lower than or equal to the size "
            "of each time series (i.e. the size of the last dimension "
            "of X) (got {0}).".format(image_size),
            "If 'image_size' is a float, it must be greater "
            "than or equal to 0 and lower than or equal to 1 "
            "(got {0}).".format(image_size),
            "'n_bins' must be greater than or equal to 2.",
            "'strategy' must be 'uniform', 'quantile' or 'normal'."
        ]
        return value_error_list_

    image_size_list = [1., -1, 2., None]
    n_bins_list = [0, 2, None]
    strategy_list = ['quantile', 'normal', 'uniform', None]
    overlapping_list = [True, False]

    for (image_size, n_bins, strategy, overlapping) in product(
        image_size_list, n_bins_list, strategy_list, overlapping_list
    ):
        mtf = MarkovTransitionField(image_size, n_bins, strategy, overlapping)
        try:
            mtf.fit_transform(X)
        except ValueError as e:
            if str(e) in value_error_list(image_size):
                pass
            else:
                raise ValueError("Unexpected ValueError: {}".format(e))
        except TypeError as e:
            if str(e) in type_error_list():
                pass
            else:
                raise TypeError("Unexpected TypeError: {}".format(e))

    # Accurate result check
    image_size, n_bins, quantiles = 2, 4, 'quantile'

    mtf = MarkovTransitionField(image_size, n_bins, quantiles)
    arr_actual = mtf.fit_transform(X)

    # X_binned = np.array([0, 0, 1, 1, 2, 2, 3, 3])
    # X_mtm = np.asarray([[0.5, 0.5, 0.0, 0.0],
    #                    [0.0, 0.5, 0.5, 0.0],
    #                    [0.0, 0.0, 0.5, 0.5],
    #                    [0.0, 0.0, 0.0, 1.0]])
    # X_mtf = np.asarray([[0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0],
    #                    [0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0],
    #                    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0],
    #                    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0],
    #                    [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5],
    #                    [0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5],
    #                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
    #                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]])
    arr_desired = np.asarray([[0.375, 0.125],
                              [0.000, 0.500]])

    np.testing.assert_array_equal(arr_actual[0], arr_desired)
