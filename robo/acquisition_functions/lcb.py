import logging
import numpy as np

from robo.acquisition_functions.base_acquisition import BaseAcquisitionFunction


logger = logging.getLogger(__name__)


class LCB(BaseAcquisitionFunction):

    def __init__(self, model, par=0.0):
        r"""
        The lower confidence bound acquisition_functions functions that computes for a
        test point the acquisition_functions value by:

        .. math::

        LCB(X) := \mu(X) - \kappa\sigma(X)

        Parameters
        ----------
        model: Model object
            A model that implements at least
                 - predict(X)
                 - getCurrentBestX().
            If you want to calculate derivatives than it should also support
                 - predictive_gradients(X)

        X_lower: np.ndarray (D)
            Lower bounds of the input space
        X_upper: np.ndarray (D)
            Upper bounds of the input space
        par: float
            Controls the balance between exploration
            and exploitation of the acquisition_functions function. Default is 0.01
        """
        self.par = par
        super(LCB, self).__init__(model)

    def compute(self, X, derivative=False, **kwargs):
        """
        Computes the LCB acquisition_functions value and its derivatives.

        Parameters
        ----------
        X: np.ndarray(N, D), The input point where the acquisition_functions function
            should be evaluate. The dimensionality of X is (N, D), with N as
            the number of points to evaluate at and D is the number of
            dimensions of one X.

        derivative: Boolean
            If is set to true also the derivative of the acquisition_functions
            function at X is returned.

        Returns
        -------
        np.ndarray(1,1)
            LCB value of X
        np.ndarray(1,D)
            Derivative of LCB at X (only if derivative=True)
        """
        mean, var = self.model.predict(X)

        # Minimize in f so we maximize the negative lower bound
        acq = - (mean - self.par * np.sqrt(var))
        if derivative:
            dm, dv = self.model.predictive_gradients(X)
            grad = -(dm - self.par * dv / (2 * np.sqrt(var)))
            return acq, grad
        else:
            return acq