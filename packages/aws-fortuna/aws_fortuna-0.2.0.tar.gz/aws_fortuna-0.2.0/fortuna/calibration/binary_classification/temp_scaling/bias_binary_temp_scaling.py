import numpy as np

from fortuna.calibration.binary_classification.temp_scaling.base import (
    BaseBinaryClassificationTemperatureScaling,
)


class BiasBinaryClassificationTemperatureScaling(
    BaseBinaryClassificationTemperatureScaling
):
    """
    A temperature scaling class for binary classification.
    It scales the probability that the target variables is positive with a single learnable parameters.
    The method minimizes the expected bias.
    """

    def fit(self, probs: np.ndarray, targets: np.ndarray):
        self._check_probs(probs)
        self._check_targets(targets)
        self._temperature = np.mean(probs) / np.mean(targets)
