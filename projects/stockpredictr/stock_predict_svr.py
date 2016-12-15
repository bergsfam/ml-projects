import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

#plt.switch_backend('macosx')

dates = []
prices = []

def get_data(filename):
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            dates.append(int(row[0].split('-')[0])) # grabs the day value, does this need to be an int?
            prices.append(float(row[1])) # grabs the day's opening price
    return

def predict_prices(dates, prices, x):
    dates = np.reshape(dates, (len(dates), 1))

    svr_lin = SVR(kernel = 'linear', C = 1e3)
    svr_poly = SVR(kernel = 'poly', C = 1e3, degree = 2)
    svr_rbf = SVR(kernel = 'rbf', C = 1e3, gamma = 0.1)

    svr_lin.fit(dates, prices)
    print 'Got to svr_lin.fit'
    svr_poly.fit(dates, prices)
    print 'Got to svr_poly.fit'
    svr_rbf.fit(dates, prices)
    print 'Got to svr_rbf.fit'

    '''
    print 'Getting ready to plot'
    plt.scatter(dates, prices, color = 'black', label = 'Data')
    print 'Mid-plotting'
    plt.plot(dates, svr_rbf.predict(dates), color = 'red', label = 'RBF model')
    print 'predicted rbf'
    plt.plot(dates, svr_lin.predict(dates), color = 'green', label = 'Linear model')
    print 'predicted linear'
    plt.plot(dates, svr_poly.predict(dates), color = 'blue', label = 'Polynomial model')
    print 'predicted poly'
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')
    plt.legend(loc=2)
    plt.show()
    print 'Should have plotted'
    '''

    lin_predict = svr_lin.predict(x)[0]
    print 'predicted lin'
    poly_predict = svr_poly.predict(x)[0]
    print 'predicted poly'
    rbf_predict = svr_rbf.predict(x)[0]
    print 'predicted rbf'

    return lin_predict, poly_predict, rbf_predict

get_data('aapl_oct.csv')
print 'Got the monthly data'

predicted_price = predict_prices(dates, prices, 31)

print predicted_price
