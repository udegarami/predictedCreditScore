import os
#import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsClassifier as KNC
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

#import logging

#logging.basicConfig(level=logging.WARN)
#logger = logging.getLogger(__name__)

 
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    #warnings.filterwarnings("ignore")
    np.random.seed(40)

    path = 'dataset/'
    data = pd.read_csv(path + "application_train.csv")
        #logger.exception(
         #   "Unable to download training & test CSV, check your internet connection. Error: %s", e
#        )

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["TARGET"], axis=1)
    test_x = test.drop(["TARGET"], axis=1)
    train_y = train[["TARGET"]]
    test_y = test[["TARGET"]]

    k = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    ls = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    p = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5

    with mlflow.start_run():
        
        lr = KNC(n_neighbors=k, weights='uniform', algorithm='auto', leaf_size=ls, p=p, metric='minkowski', metric_params=None, n_jobs=None)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("KNN model (k_neighbors={:f}, leaf_size={:f}, p={:f}):".format(k, ls, p))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(lr, "model", registered_model_name="ElasticnetWineModel")
        else:
            mlflow.sklearn.log_model(lr, "model")