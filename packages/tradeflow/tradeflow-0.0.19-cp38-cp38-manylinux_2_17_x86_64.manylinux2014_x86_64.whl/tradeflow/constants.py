import logging
from enum import Enum


class OrderSelectionMethodAR(Enum):
    INFORMATION_CRITERION = "information_criterion"
    PACF = "pacf"

    def __str__(self) -> str:
        return self._value_


class FitMethodAR(Enum):
    YULE_WALKER = "yule_walker"
    OLS_WITH_CST = "ols_with_cst"

    def __str__(self) -> str:
        return self._value_


class InformationCriterion(Enum):
    AIC = "aic"
    BIC = "bic"
    HQIC = "hqic"

    def __str__(self) -> str:
        return self._value_
