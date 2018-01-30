""" 
Distance Metric Algorithm.

Abstract class representing a Distance Metric Learning algorithm.
"""

from numpy.linalg import inv, cholesky
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array
from .dml_utils import metric_to_linear

class DML_Algorithm(BaseEstimator,TransformerMixin):


    def __init__(self):
    	raise NotImplementedError('Class DML_Algorithm is abstract and cannot be instantiated.')


    # A DML Algorithm can compute either a Mahalanobis metric matrix or an associated linear transformation.
    # DML subclasses must override one of the following methods (metric or transformer), according to their computatoin way.
    def metric(self):
        """Computes the Mahalanobis matrix from the transformation matrix.
        .. math:: M = L^{\\top} L
    
        Returns
        -------
        M : (d x d) matrix
        """
        L = self.transformer()
        return L.T.dot(L)

    def transformer(self):
        """Computes the transformation matrix from the Mahalanobis matrix.
    
        L = inv(cholesky(M))
    
        Returns
        -------
        L : (d x d) matrix
        """
        try:
            L = inv(cholesky(self.metric()))
            return L
        except:
            L = metric_to_linear(self.metric())
            return L
    
    def transform(self, X=None):
        """Applies the metric transformation.
    
        Parameters
        ----------
        X : (n x d) matrix, optional
            Data to transform. If not supplied, the training data will be used.
    
        Returns
        -------
        transformed : (n x d) matrix
            Input data transformed to the metric space by :math:`XL^{\\top}`
        """
        if X is None:
            X = self.X_
        else:
            X = check_array(X, accept_sparse=True)
        L = self.transformer()
        return X.dot(L.T)
