from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from metrics import MetricsPrinter
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
import warnings
from sklearn.model_selection import train_test_split

warnings.simplefilter('ignore')

def apply_linear_regression(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())])
    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)
    MetricsPrinter.metric_printer(y_test, y_pred)

def apply_support_vector_regression(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([("scaler", StandardScaler()), ("model", SVR())])
    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)
    MetricsPrinter.metric_printer(y_test, y_pred)

def apply_random_forest_regression(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([("scaler", StandardScaler()), ("model", RandomForestRegressor())])
    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)
    MetricsPrinter.metric_printer(y_test, y_pred)

def apply_decision_tree_regression(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([("scaler", StandardScaler()), ("model", DecisionTreeRegressor())])
    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)
    MetricsPrinter.metric_printer(y_test, y_pred)

def apply_XGB(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    dtrain_reg = xgb.DMatrix(x_train, label=y_train)
    dtest_reg = xgb.DMatrix(x_test, label=y_test)
    params_xgb = {'objective': 'reg:squarederror', 'max_depth': 3, 'learning_rate': 0.1}
    model_xgb = xgb.train(params=params_xgb, dtrain=dtrain_reg, num_boost_round=50)
    prediction_xgb = model_xgb.predict(dtest_reg)
    MetricsPrinter.metric_printer(y_test, prediction_xgb)


def apply_LGBM(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    params_lgbm = {'task': 'train', 'boosting': 'gbdt', 'objective': 'regression', 'num_leaves': 10, 'learning_rate': 0.05}
    lgb_train = lgb.Dataset(x_train, label=y_train)
    lgb_eval = lgb.Dataset(x_test, label=y_test, reference=lgb_train)
    model_lgbm = lgb.train(params=params_lgbm, train_set=lgb_train, valid_sets=[lgb_train, lgb_eval], num_boost_round=100)
    prediction_lgbm = model_lgbm.predict(x_test)
    MetricsPrinter.metric_printer(y_test, prediction_lgbm)

def apply_GBR(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model_gbr = GradientBoostingRegressor(n_estimators=300, learning_rate=0.1, random_state=42, max_features=5)
    model_gbr.fit(x_train, y_train)
    prediction_gbr = model_gbr.predict(x_test)
    MetricsPrinter.metric_printer(y_test, prediction_gbr)


    
