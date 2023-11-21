import numpy as np
import pandas as pd
from app import core
from itertools import product


class Opt:
    @classmethod
    def from_json(cls) -> "Opt":
        import json

        # Read data from the JSON file into a dictionary
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
        return cls(**data)

    def __init__(
        self,
        asset_init,
        asset_duration,
        target_weight,
        expected_returns,
        repayment_init,
        interest_init,
        capital_call,
        cashflow,
    ) -> None:
        self.asset_init = pd.Series(asset_init).fillna(0)
        self.target_weight = pd.Series(target_weight).fillna(0)
        self.asset_druation = pd.Series(asset_duration).fillna(0)
        self.expected_returns = pd.DataFrame(expected_returns).fillna(0)
        self.repayment_init = pd.DataFrame(repayment_init).fillna(0)
        self.interest_init = pd.DataFrame(interest_init).fillna(0)
        self.capital_call = pd.DataFrame(capital_call).fillna(0)

        if isinstance(cashflow, pd.DataFrame):
            cashflow = cashflow.sum(axis=1)
        self.cashflow = cashflow

        self.asset_init = pd.concat(
            [self.asset_init] * len(self.expected_returns), axis=1
        ).T.fillna(0)
        self.target_weight = pd.concat(
            [self.target_weight] * len(self.expected_returns), axis=1
        ).T.fillna(0)
        self.asset_druation = pd.concat(
            [self.asset_druation] * len(self.expected_returns), axis=1
        ).T.fillna(0)
        assert (
            self.expected_returns.shape
            == self.repayment_init.shape
            == self.interest_init.shape
            == self.capital_call.shape
        )
        self.shape = self.expected_returns.shape

    def constraint_function(self, investment):
        """
        Constraint function to enforce the target weights of assets.
        """
        investment = (
            pd.DataFrame(
                investment.reshape(
                    (
                        len(self.expected_returns.index),
                        len(self.expected_returns.columns),
                    )
                ),
                columns=self.expected_returns.columns,
                index=self.expected_returns.index,
            )
            * 1_000_000
        )

        print(round(investment.mean().mean(), 0))

        asset_final = self.asset_init.copy().fillna(0)
        asset_repay = self.repayment_init.copy().fillna(0)
        asset_inter = self.interest_init.copy().fillna(0)
        for year in investment.index[1:]:
            for asset in investment.columns:
                if asset == "Liq":
                    continue
                repay = float(asset_repay.loc[year, asset])
                inter = float(asset_inter.loc[year, asset])
                invest = (
                    investment.loc[year, asset] + self.capital_call.loc[year, asset]
                )
                asset_final.loc[year, "Liq"] += repay + inter - invest
                asset_final.loc[year, asset] += -repay - inter + invest

                duration = self.asset_druation.loc[year, asset]
                for n_year in investment.index[1:]:
                    if n_year <= year:
                        continue
                    asset_inter.loc[n_year, asset] += (
                        invest * self.expected_returns.loc[n_year, asset]
                    )
                    if n_year == year + int(duration):
                        asset_repay.loc[n_year, asset] += invest
                if asset.startswith("ACT"):
                    asset_final.loc[year, asset] = asset_final.loc[year - 1, asset] * (
                        self.expected_returns.loc[year, asset] + 1
                    )
        aw = asset_final.divide(asset_final.sum(axis=1), axis=0)
        obj = aw - self.target_weight
        jj = core.l2_norm(obj.apply(core.l2_norm, axis=1))
        print(jj)
        return jj * 10000000

    def opt(self):
        from scipy.optimize import minimize

        obj = lambda x: self.constraint_function(x)

        x0 = pd.DataFrame(
            data=0.0,
            columns=self.expected_returns.columns,
            index=self.expected_returns.index,
        ).values.flatten()
        prob = minimize(fun=obj, x0=x0, method="trust-constr")

        return prob





opt = Opt.from_json()
prob = opt.opt()

print(prob)
prob.x
