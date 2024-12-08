from statsmodels.tsa.api import SimpleExpSmoothing, Holt, ExponentialSmoothing
from metrics import MetricsPrinter

def simple_exponential_smoothening(target):
    time_series = target
    model_single = SimpleExpSmoothing(time_series)
    model_single_fit = model_single.fit()
    actual = time_series.values
    predicted = model_single_fit.fittedvalues.values
    MetricsPrinter.metric_printer(actual, predicted)

def holt_smoothening(target):
    time_series = target
    model_double = Holt(time_series)
    model_double_fit = model_double.fit()
    actual = time_series.values
    predicted = model_double_fit.fittedvalues.values
    MetricsPrinter.metric_printer(actual, predicted)

def exponential_smoothening(target):
    time_series = target
    model_triple = ExponentialSmoothing(time_series, seasonal_periods=12, trend='add', seasonal='add')
    model_triple_fit = model_triple.fit()
    actual = time_series.values
    predicted = model_triple_fit.fittedvalues.values
    MetricsPrinter.metric_printer(actual, predicted)