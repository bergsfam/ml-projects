import pandas_datareader.data as web
import pandas as pd
import numpy as np
import datetime as dt

def get_data(start, end, symbols):
    data = pd.DataFrame()
    for sym in symbols:
        data[sym] = web.DataReader(sym, 'yahoo', start, end)['Adj Close']
    data.columns = symbols
    return data

def allocate_data(raw_data, allocations, start_val):
    normed = raw_data / raw_data.ix[0]
    alloced = normed * allocations
    port_data = alloced * start_val
    port_data['Portfolio'] = port_data.sum(axis=1)
    return port_data

def calc_sharpe_ratio(df_returns, risk_free, sample_freq):
    df_returns = df_returns - risk_free
    mean = df_returns.mean()
    std = df_returns.std()
    K = np.sqrt(sample_freq)
    sharpe_ratio = mean / std * K
    return sharpe_ratio

def compute_portfolio_stats(prices, rfr, sf):
    cum_return = prices['Portfolio'][-1] / prices['Portfolio'][0] - 1
    daily_rets = prices['Portfolio'].pct_change().dropna()
    avg_daily_return = daily_rets.mean()
    std_dev_daily_return = daily_rets.std()
    sharpe_ratio = calc_sharpe_ratio(daily_rets, rfr, sf)
    return cum_return, avg_daily_return, std_dev_daily_return, sharpe_ratio

def plot_returns(portfolio_data, benchmark):
    portfolio_data['Benchmark'] = benchmark['Portfolio']
    (portfolio_data[['Portfolio', 'Benchmark']] / portfolio_data[['Portfolio', 'Benchmark']].ix[0]).plot()
    return

def assess_portfolio(sd, ed, syms, allocs, sv, rfr=0.0, sf=252.0, gen_plot=False):
    portfolio_values = get_data(sd, ed, syms)
    portfolio_values = allocate_data(portfolio_values, allocs, sv)
    spy = get_data(sd, ed, ['SPY'])
    spy = allocate_data(spy, [1.0], sv)
    cr, adr, sddr, sr = compute_portfolio_stats(portfolio_values, rfr, sf)
    ev = portfolio_values['Portfolio'][-1]

    print "Start Date:", sd
    print "End Date:", ed
    print "Symbols:", syms
    print "Allocations:", allocs
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

    if gen_plot:
        plot_returns(portfolio_values, spy)


    return cr, adr, sddr, sr, ev
