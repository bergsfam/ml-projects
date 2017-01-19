import pandas_datareader.data as web
import pandas as pd
import numpy as np

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

def calc_sharpe_ratio(df_returns, risk_free=0.0, sample_freq=252.0):
    df_returns = df_returns - risk_free
    mean = df_returns.mean()
    std = df_returns.std()
    K = np.sqrt(sample_freq)
    sharpe_ratio = mean / std * K
    return sharpe_ratio

def compute_portfolio_stats(prices, rfr=0.0, sf=252.0):
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
    #spy = get_data(sd, ed, ['SPY'])
    #spy = allocate_data(spy, [1.0], sv)
    spy = get_benchmark(start_date=sd, end_date=ed, start_val=sv)
    cr, adr, sddr, sr = compute_portfolio_stats(portfolio_values, rfr, sf)
    ev = portfolio_values['Portfolio'][-1]

    print "Start Date:", sd
    print "End Date:", ed
    print "Symbols:", syms
    print "Allocations: ", ['%5.3f' % val for val in allocs]
    print "Sharpe Ratio: %5.3f" % sr
    print "Volatility (stdev of daily returns): %5.3f" % sddr
    print "Average Daily Return: %5.3f" % adr
    print "Cumulative Return: %5.3f" % cr

    if gen_plot:
        plot_returns(portfolio_values, spy)


    return cr, adr, sddr, sr, ev

def get_benchmark(start_date, end_date, symbols=['SPY'], allocation=[1.0], start_val=1.0):
    '''
    Get a benchmark portfolio, default is S&P500

    Input:
        Start Date and End Date of portfolio
        symbols = list of stock symbols, defaults to SPY

    Output:
        Pandas Dataframe
            Index = Date
            Symbols = Columns (Adj Close) values Normalized by allocation
            Portfolio is last column, normalized and allocated
    '''
    benchmark = get_data(start_date, end_date, symbols)
    benchmark = allocate_data(benchmark, [1.0], start_val)

    return benchmark

def print_results(my_portfolio, benchmark, create_plot=False):
    '''
    Calculates and prints results

    Input: two DataFrames and create_plot=True
    '''

    port_stats = compute_portfolio_stats(my_portfolio)
    bench_stats = compute_portfolio_stats(benchmark)
    port_ev = my_portfolio['Portfolio'][-1]
    bench_ev = benchmark['Portfolio'][-1]
    sd = my_portfolio.index[0]
    ed = my_portfolio.index[-1]
    my_syms = my_portfolio.columns[1:-1].values

    print "Start Date:", sd
    print "End Date:", ed
    print "Portfolio contains:", my_syms
    print "\n"
    print "                    Portfolio vs. Benchmark"
    print "Sharpe Ratio:           %5.3f vs. %5.3f" % (port_stats[3], bench_stats[3])
    print "Volatility:             %5.3f vs. %5.3f" % (port_stats[2], bench_stats[2])
    print "Average Daily Return: %7.5f vs. %7.5f" % (port_stats[1], bench_stats[1])
    print "Cumulative Return:      %5.3f vs. %5.3f" % (port_stats[0], bench_stats[0])
    print "Final Value:       %10.2f vs. %10.2f" % (port_ev, bench_ev)
    print "\n"

    if create_plot:
        plot_returns(my_portfolio, benchmark)
