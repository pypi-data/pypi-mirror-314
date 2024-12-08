from simplreg.evaluation import evaluate_model
from simplreg.model_training import train_model
from simplreg.preprocessing import preprocess_data
from simplreg.visualization import plot_feature_importance

def simplereg_pipeline(df, target_column, task_type):
    """Simple ML pipeline --> Preprocess, train, eval, visualize"""
    # Preprocess the data
    X_train, X_test, y_train, y_test = preprocess_data(df, target_column)

    # Train the model
    model = train_model(X_train, y_train, task_type)

    # Evaluate the model
    evaluate_model(model, X_test, y_test, task_type)

    # Visualize feature importance if it's a classification task
    if task_type == 'classification':
        plot_feature_importance(model, feature_names=df.columns[:-1])