import warnings
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from numpy.typing import ArrayLike
from scipy.optimize import minimize, OptimizeResult
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils import check_X_y

from sklearn.linear_model import LogisticRegression
class CSLogitClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, C=1.0, loss_fn='aec', optimize_fn=None, robust=False, fit_intercept=True):
        self.C = C
        self.loss_fn = loss_fn
        self.robust = robust
        self.fit_intercept = fit_intercept
        self.optimal_weights = None
        if optimize_fn is None:
            self.optimize_fn = _optimize

    def fit(self, X: ArrayLike, y: ArrayLike, cost_matrix: ArrayLike) -> 'CSLogitClassifier':
        X, y = check_X_y(X, y, accept_sparse=True)
        self.classes_ = np.unique(y)
        if len(self.classes_) != 2:
            raise ValueError("This solver needs samples of 2 classes"
                             " in the data, but the data contains only one"
                             " class: %r" % self.classes_[0])

        if self.robust:
            cost_matrix = self.transform_cost_matrix(X, y, cost_matrix)

        sample_weights = self.get_sample_weights(y, cost_matrix)

        result = self.optimize_fn(self.loss_fn, X, y, None, self.C, None, self.fit_intercept)

        return self


def _optimize(objective, X, y, sample_weight, C, bounds, fit_intercept, max_iter=10000, tolerance=1e-4, **kwargs) -> OptimizeResult:
    n_threads = 1
    n_samples, n_features = X.shape

    initial_weights = np.zeros(
        (1, n_features + int(fit_intercept)), order="F", dtype=X.dtype
    )

    sw_sum = n_samples if sample_weight is None else np.sum(sample_weight)

    l2_reg_strength = 1.0 / (C * sw_sum)
    result = minimize(
        objective,
        initial_weights,
        method="L-BFGS-B",
        jac=True,
        args=(X, y, sample_weight, l2_reg_strength, n_threads),
        options={
            "maxiter": max_iter,
            "maxls": 50,  # default is 20
            "gtol": tolerance,
            "ftol": 64 * np.finfo(float).eps,
        },
        **kwargs,
    )
    _check_optimize_result(
        result,
        max_iter,
    )

    return result


def _check_optimize_result(result, max_iter=None):
    """Check the OptimizeResult for successful convergence

    Parameters
    ----------
    result : OptimizeResult
       Result of the scipy.optimize.minimize function.

    max_iter : int, default=None
       Expected maximum number of iterations.
    """
    # handle both scipy and scikit-learn solver names
    if result.status != 0:
        try:
            # The message is already decoded in scipy>=1.6.0
            result_message = result.message.decode("latin1")
        except AttributeError:
            result_message = result.message
        warning_msg = (
            "L-BFGS failed to converge (status={}):\n{}.\n\n"
            "Increase the number of iterations (max_iter) "
            "or scale the data as shown in:\n"
            "    https://scikit-learn.org/stable/modules/"
            "preprocessing.html"
        ).format(result.status, result_message)
        warnings.warn(warning_msg, ConvergenceWarning, stacklevel=2)

