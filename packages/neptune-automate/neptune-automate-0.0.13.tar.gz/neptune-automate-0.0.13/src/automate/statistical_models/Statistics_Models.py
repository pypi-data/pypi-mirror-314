from statsmodels.tsa.arima.model import ARIMA
from automate.metrics import MetricsPrinter
from statsmodels.tsa.statespace.sarimax import SARIMAX

def apply_ARIMA(data, p, d, q, target_variable_string):
    train_size = int(len(data) * 0.8)
    train = data[:train_size].copy()
    test = data[train_size:].copy()
    train_series = train[target_variable_string]
    test_series = test[target_variable_string]
    model = ARIMA(train_series, order=(p, d, q))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=len(test_series))[:len(test_series)]
    MetricsPrinter.metric_printer(test_series, forecast)



def apply_SARIMA(data, p, d, q,target_variable_string ):
    train_size = int(len(data) * 0.8)
    train = data[:train_size].copy()
    test = data[train_size:].copy()
    train_series = train[target_variable_string]
    test_series = test[target_variable_string]
    sarima_model = ARIMA(train_series, order=(p, d, q), seasonal_order=(0, 0, 0, 12))
    sarima_result = sarima_model.fit()
    predicted = sarima_result.predict(start=1, end=len(train_series))
    MetricsPrinter.metric_printer(test_series, predicted)

def apply_SARIMAX(data, p, d, q, target_variable_string, exog_vars=None):
    train_size = int(len(data) * 0.8)
    train = data[:train_size].copy()
    test = data[train_size:].copy()
    train_series = train[target_variable_string]
    test_series = test[target_variable_string]
    exog_train = train[exog_vars] if exog_vars else None
    exog_test = test[exog_vars] if exog_vars else None
    sarimax_model = SARIMAX(
        train_series,
        order=(p, d, q),
        seasonal_order=(0, 0, 0, 12),
        exog=exog_train,
    )
    sarimax_result = sarimax_model.fit()
    predicted = sarimax_result.predict(
        start=train_series.index[0],
        end=train_series.index[-1],
        exog=exog_test
    )
    MetricsPrinter.metric_printer(test_series, predicted)