# Module: internal.Pipeline
# Author: Antoni Baum (Yard1) <antoni.baum@protonmail.com>
# License: MIT

# Provides a Pipeline supporting partial fitting and several attributes needed for plotting.

import imblearn.pipeline
from sklearn.utils import _print_elapsed_time
from sklearn.base import BaseEstimator, TransformerMixin

class Pipeline(imblearn.pipeline.Pipeline):
    def fit(self, X, y=None, **fit_kwargs):
        result = super().fit(X, y=y, **fit_kwargs)

        try:
            self.coef_ = self._final_estimator.coef_
        except:
            pass
        try:
            self.feature_importances_ = self._final_estimator.feature_importances_
        except:
            pass
        return result


# this class will be automatically switched to when needed by the
# estimator_pipeline context
class PartialFitPipeline(Pipeline):
    def partial_fit(self, X, y, classes=None, sample_weight=None):
        """Fit the model.

        Fit all the transforms/samplers one after the other and
        transform/sample the data, then fit the transformed/sampled
        data using the final estimator.

        Parameters
        ----------
        X : iterable
            Training data. Must fulfill input requirements of first step of the
            pipeline.

        y : iterable, default=None
            Training targets. Must fulfill label requirements for all steps of
            the pipeline.

        **fit_params : dict of str -> object
            Parameters passed to the ``fit`` method of each step, where
            each parameter name is prefixed such that parameter ``p`` for step
            ``s`` has key ``s__p``.

        Returns
        -------
        self : Pipeline
            This estimator.
        """
        try:
            self.Xt_
        except:
            self.Xt_ = None
            self.yt_ = None
        if self.Xt_ is None or self.yt_ is None:
            Xt, yt, _ = self._fit(X, y)
            self.Xt_ = Xt
            self.yt_ = yt
        else:
            Xt = self.Xt_
            yt = self.yt_
        with _print_elapsed_time("Pipeline", self._log_message(len(self.steps) - 1)):
            if self._final_estimator != "passthrough":
                self._final_estimator.partial_fit(
                    Xt, yt, classes=classes, sample_weight=sample_weight
                )
        return self
