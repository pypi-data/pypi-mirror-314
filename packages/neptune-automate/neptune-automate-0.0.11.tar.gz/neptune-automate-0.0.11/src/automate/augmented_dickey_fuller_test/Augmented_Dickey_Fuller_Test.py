from statsmodels.tsa.stattools import adfuller

def check_stationarity(target_variable):
    series = target_variable.values
    result = adfuller(series)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:', result[4])
    if result[1] < 0.05:
        print('The series is stationary')
    else:
        print('The series is non-stationary')

