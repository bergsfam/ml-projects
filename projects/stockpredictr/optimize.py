import numpy as np
import scipy.optimize as sco
import pandas as pd 

def min_func_sharpe(weights, rets):
    weights = np.array(weights)
    pret = np.sum(rets.mean() * weights)
    pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov(), weights)))
    return -(pret / pvol)

def optimize_portfolio(portfolio_values):
    rets = portfolio_values.pct_change().dropna()

    asset_count = len(rets.columns)
    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(asset_count))

    opts = sco.minimize(min_func_sharpe, asset_count * [1. / asset_count,], args=rets, bounds=bnds, constraints=cons)

    weights = opts['x']

    return weights
