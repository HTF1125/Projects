import warnings
from typing import Optional, List, Dict, Callable
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform
import numpy as np
import pandas as pd
from .. import core



class Portfolio:
    def __init__(
        self,
        asset_cov: pd.DataFrame,
        asset_ret: Optional[pd.Series] = None,
        asset_cor: Optional[pd.DataFrame] = None,
        asset_pxs: Optional[pd.DataFrame] = None,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
        sum_weight: float = 1.0,
        min_return: Optional[float] = None,
        max_return: Optional[float] = None,
        min_risk: Optional[float] = None,
        max_risk: Optional[float] = None,
        risk_free: float = 0.02,
    ) -> None:
        self.constraints = {}
        self.asset_cov = asset_cov
        self.assets = self.asset_cov.index
        self.asset_ret = asset_ret
        self.asset_cor = asset_cor
        self.asset_pxs = asset_pxs
        self.risk_free = risk_free
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.sum_weight = sum_weight
        self.min_return = min_return
        self.max_return = max_return
        self.min_risk = min_risk
        self.max_risk = max_risk

    @property
    def cov(self) -> pd.DataFrame:
        if self.asset_cov is None:
            raise ValueError("Cov is None")
        return self.asset_cov

    @property
    def ret(self) -> pd.Series:
        if self.asset_ret is None:
            raise ValueError("Ret is None")
        return self.asset_ret

    @property
    def cor(self) -> pd.DataFrame:
        if self.asset_cor is None:
            warnings.warn("Cor not availabel. Trying to convert from Cov.")
            return core.cov_to_cor(self.cov)
        return self.asset_cor

    @property
    def min_weight(self) -> Optional[Dict]:
        return self.constraints.get("min_weight")

    @min_weight.setter
    def min_weight(self, min_weight: Optional[float]) -> None:
        if min_weight is None:
            self.constraints.pop("min_weight", None)
            return
        self.constraints.update(
            {"min_weight": {"type": "ineq", "fun": lambda w: (w - min_weight)}}
        )

    @property
    def max_weight(self) -> Optional[Dict]:
        return self.constraints.get("max_weight")

    @max_weight.setter
    def max_weight(self, max_weight: Optional[float]) -> None:
        if max_weight is None:
            self.constraints.pop("max_weight", None)
            return
        self.constraints.update(
            {"max_weight": {"type": "ineq", "fun": lambda w: -(w - max_weight)}}
        )

    @property
    def sum_weight(self) -> Optional[Dict]:
        return self.constraints.get("sum_weight")

    @sum_weight.setter
    def sum_weight(self, sum_weight: Optional[float]) -> None:
        if sum_weight is None:
            self.constraints.pop("sum_weight", None)
            return
        self.constraints.update(
            {"sum_weight": {"type": "eq", "fun": lambda w: (np.sum(w) - sum_weight)}}
        )

    @property
    def min_return(self) -> Optional[Dict]:
        return self.constraints.get("min_return")

    @min_return.setter
    def min_return(self, min_return: Optional[float]) -> None:
        if min_return is None:
            self.constraints.pop("min_return", None)
            return
        try:
            fun = lambda w: (core.ExpectedReturn(w, self.ret) - min_return)
            self.constraints.update({"min_return": {"type": "ineq", "fun": fun}})
        except Exception as exc:
            print(exc)

    @property
    def max_return(self) -> Optional[Dict]:
        return self.constraints.get("max_return")

    @max_return.setter
    def max_return(self, max_return: Optional[float]) -> None:
        if max_return is None:
            self.constraints.pop("max_return", None)
            return
        try:
            fun = lambda w: -(core.ExpectedReturn(w, self.ret) - max_return)
            self.constraints.update({"max_return": {"type": "ineq", "fun": fun}})

        except Exception as exc:
            print(exc)

    @property
    def min_risk(self) -> Optional[Dict]:
        return self.constraints.get("min_risk")

    @min_risk.setter
    def min_risk(self, min_risk: Optional[float]) -> None:
        if min_risk is None:
            self.constraints.pop("min_risk", None)
            return

        try:
            fun = lambda w: (core.ExpectedRisk(w, self.cov) - min_risk)
            self.constraints.update({"min_risk": {"type": "ineq", "fun": fun}})
        except Exception as exc:
            print(exc)

    @property
    def max_risk(self) -> Optional[Dict]:
        return self.constraints.get("max_risk")

    @max_risk.setter
    def max_risk(self, max_risk: Optional[float]) -> None:
        if max_risk is None:
            self.constraints.pop("max_risk", None)
            return
        try:
            fun = lambda w: -(core.ExpectedRisk(w, self.cov) - max_risk)
            self.constraints.update({"max_risk": {"type": "ineq", "fun": fun}})
        except Exception as exc:
            print(exc)

    def __solve__(
        self,
        objective: Callable,
        method: str = "SLSQP",
        extra_constraints: Optional[List[Dict]] = None,
    ) -> pd.Series:
        constraints = list(self.constraints.values())
        if extra_constraints:
            constraints.extend(extra_constraints)

        x0 = np.ones(len(self.assets)) / len(self.assets)

        prob = minimize(fun=objective, x0=x0, method=method, constraints=constraints)

        if prob.success:
            data = prob.x + 1e-16
            weight = pd.Series(data=data, index=self.assets, name="Weight")
            return weight.round(6)
        warnings.warn(message="Optimization Unsuccessful.")
        return pd.Series({})

    def solve(self) -> pd.Series:
        raise NotImplementedError("must implement `solve` method in portfolio class")


class WeightParity(Portfolio):
    def solve(self) -> pd.Series:
        x0 = np.ones(len(self.assets)) / len(self.assets)
        return self.__solve__(objective=lambda w: core.l2_norm(np.subtract(w, x0)))


class MaxDiverse(Portfolio):
    def solve(self) -> pd.Series:
        vols = np.sqrt(np.diag(self.cov))
        return self.__solve__(
            objective=lambda w: -np.dot(w, vols) / core.ExpectedRisk(w, self.cov)
        )


class RiskParity(Portfolio):
    def solve(self) -> pd.Series:
        budgets = np.ones(len(self.assets)) / len(self.assets)
        weights = self.__solve__(
            objective=lambda w: core.l2_norm(
                np.subtract(
                    np.dot(self.cov, w) * w / core.ExpectedRisk(w, self.cov),
                    np.multiply(
                        budgets,
                        core.ExpectedRisk(w, self.cov),
                    ),
                )
            )
        )
        return weights


class MaxReturn(Portfolio):
    def solve(self) -> pd.Series:
        return self.__solve__(objective=lambda w: -core.ExpectedReturn(w, self.ret))


class MaxSharpe(Portfolio):
    def solve(self) -> pd.Series:
        return self.__solve__(
            objective=lambda w: core.ExpectedSharpe(w, self.ret, self.cov)
        )


class MinVola(Portfolio):
    def solver(self) -> pd.Series:
        return self.__solve__(objective=lambda w: core.ExpectedRisk(w, self.cov))


class InverseVar(Portfolio):
    def solver(self) -> pd.Series:
        cov = self.asset_cov
        if cov is None:
            raise

        inverse_w = 1.0 / np.diag(cov)
        inverse_w /= np.sum(inverse_w)
        return self.__solve__(
            objective=lambda w: core.l2_norm(np.subtract(w, inverse_w))
        )


class Hierarchy(Portfolio):
    def recursive_bisection(self, sorted_tree):
        left = sorted_tree[0 : int(len(sorted_tree) / 2)]
        right = sorted_tree[int(len(sorted_tree) / 2) :]
        cache = [(left, right)]
        if len(left) > 2:
            cache.extend(self.recursive_bisection(left))
        if len(right) > 2:
            cache.extend(self.recursive_bisection(right))
        return cache

    def mask_weights(self, weights: np.ndarray, include: List) -> np.ndarray:
        w = weights.copy()
        if include:
            for i, _ in enumerate(w):
                if i not in include:
                    w[i] = 0.0
        return w

    def get_cluster_sets(
        self, corr_matrix: np.ndarray, linkage_method: str = "single"
    ) -> List:
        dist = np.sqrt((1 - corr_matrix).round(5) / 2)
        clusters = linkage(squareform(dist), method=linkage_method)
        sorted_tree = list(to_tree(clusters, rd=False).pre_order())
        cluster_sets = self.recursive_bisection(sorted_tree)
        if not isinstance(cluster_sets, List):
            cluster_sets = [cluster_sets]
        return cluster_sets


class HERC(Hierarchy):
    """
    Hierarchical Equal Risk Contribution
    """

    def solve(self, linkage_method: str = "single") -> pd.Series:
        return self.__solve__(
            objective=lambda w: core.l2_norm(
                np.array(
                    [
                        core.ExpectedMarginalVol(
                            self.mask_weights(w, left_idx), self.cov
                        )
                        - core.ExpectedMarginalVol(
                            self.mask_weights(w, right_idx), self.cov
                        )
                        for left_idx, right_idx in self.get_cluster_sets(
                            self.cor.values, linkage_method
                        )
                    ]
                )
            )
        )


class HRP(Hierarchy):
    def solve(self, linkage_method: str = "single") -> pd.Series:
        return self.__solve__(
            objective=lambda w: core.l2_norm(
                np.array(
                    [
                        core.ExpectedRisk(self.mask_weights(w, left_idx), self.cov)
                        - core.ExpectedRisk(self.mask_weights(w, right_idx), self.cov)
                        for left_idx, right_idx in self.get_cluster_sets(
                            self.cor.values, linkage_method
                        )
                    ]
                )
            )
        )
