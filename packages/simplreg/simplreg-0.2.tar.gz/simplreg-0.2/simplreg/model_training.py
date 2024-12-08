from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression

def train_model(X_train, y_train, train_type):
    """Train the model based on the type: regression or classification"""

    if train_type == 'regression':
        model = RandomForestRegressor(random_state=42)
    elif train_type == 'classification':
        model = RandomForestClassifier(random_state=42)
    else:
        raise ValueError('Invalid model type. Choose between regression and clasification')
    
    model.fit(X_train, y_train)
    return model
   