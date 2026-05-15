import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import lightgbm as lgb

class Models:
    
    def get_gru_model(self, n_features):
        def log_cosh_loss(y_true, y_pred):
            error = y_pred - y_true
            return tf.reduce_mean(tf.math.log(tf.math.cosh(error)))
        
        model = Sequential([
            GRU( 128, return_sequences=True, input_shape=(50, n_features)), 
            BatchNormalization(),
            Dropout(0.3),
            GRU(64, return_sequences=True),
            BatchNormalization(),
            Dropout(0.2),
            GRU(32, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation="relu"),
            Dense(1)
        ])
        model.compile( optimizer=Adam(learning_rate=0.0005), loss=log_cosh_loss, metrics=["mae"] )
        return model

    def get_lgbm_model(self):
        return lgb.LGBMRegressor(
            verbosity=-1,
            force_col_wise=True,
            boosting_type="rf",
            objective="huber",
            learning_rate=0.01,
            n_estimators=500,
            num_leaves=64,
            max_depth=32,
            min_child_samples=16,
            subsample=0.8,
            subsample_freq=1,
            colsample_bytree=0.8,
            metric="mae",
            random_state=42
        )
    
    def get_ridge_model(self):
        return Ridge(alpha=1.0)
    
    def get_svm_model (self):
        return SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.01)
    
    def get_random_forest_model(self):
        return RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
    def get_knn_model(self, k):
        return KNeighborsRegressor(
            n_neighbors=k,
            weights='distance'
        )