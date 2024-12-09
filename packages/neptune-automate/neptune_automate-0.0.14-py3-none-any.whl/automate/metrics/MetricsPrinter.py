from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

def metric_printer(actual, predicted):
    R2_score = r2_score(actual, predicted)
    MAE = mean_absolute_error(actual, predicted)
    MSE = mean_squared_error(actual, predicted)
    RMSE = np.sqrt(MSE)
    print(f"RMSE: {RMSE}")
    print(f"MAE: {MAE}")
    print(f"MSE: {MSE}")
    print(f"R² Score: {R2_score}")