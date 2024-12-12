from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
import pickle


class KNNModel:
    """
    The model itself. This class contains methods for creation of the model itself and its evaluation
    """

    def __init__(self, train_test, n_neighbors=9, p=1, weights='distance', algorithm='ball_tree'):
        """
        The initialization of model class accepts training-testing set created by Preprocessor class and it starts the model with parameters
        passed during initialization. The defaults have been chosen through testing and evaluation.
        """
        self.train_test = train_test
        self.model = KNeighborsRegressor(n_neighbors=n_neighbors, p=p, weights=weights, algorithm=algorithm)


    def fit_model(self, X_train, y_train) -> None:
        """
        The method to fit (train) the model
        """        
        self.model.fit(X_train, y_train)


    def evaluate_model(self) -> None:
        """
        The main method of model class, it will fit and evaluate the model along different metrics
        """
        X_train, X_test, y_train, y_test = self.train_test
        self.fit_model(X_train, y_train)

        y_prediction = self.model.predict(X_test)
        y_train_prediction = self.model.predict(X_train)
        MAE = round(mean_absolute_error(y_test, y_prediction), 2)
        MAE_train = round(mean_absolute_error(y_train, y_train_prediction), 2)
        RMSE = round(mean_squared_error(y_test, y_prediction), 2)
        RMSE_train = round(mean_squared_error(y_train, y_train_prediction), 2)
        R2 = round(r2_score(y_test, y_prediction), 2)
        R2_train = round(r2_score(y_train, y_train_prediction), 2)
        MAPE = round(mean_absolute_percentage_error(y_test, y_prediction), 2)
        MAPE_train = round(mean_absolute_percentage_error(y_train, y_train_prediction), 2)

        print(f'Values for (train/test)\nMean absolute error: {MAE_train} / {MAE}\nMean squared error: {RMSE_train} / {RMSE}\nR2 score: {R2_train} / {R2}\nMean absolute procentage error:  {MAPE_train * 100}% / {MAPE * 100}%')
    
    def save_knn(self) -> None:
        """
        Method for saving model to json format for deployment
        """
        X_train, X_test, y_train, y_test = self.train_test
        self.fit_model(X_train, y_train)
        pickle.dump(self.model, open('knn_reg.sav', 'wb'))
