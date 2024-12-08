from sklearn.metrics import mean_squared_error, accuracy_score, r2_score, f1_score, classification_report
from tabulate import tabulate

def evaluate_model(model, X_test, y_test, test_type):
    """Evaluate the model based on the type: regression or classification"""

    predictions = model.predict(X_test)

    # Now based on the eval_type, display the metric table
    metrics_table = []
    if test_type == 'regression':
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        metrics_table.append(['Mean Squared Error', mse])
        metrics_table.append(['R2 Score', r2])
    
    elif test_type == 'classification':
        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions, average='weighted')
        metrics_table.append(['Accuracy', accuracy])
        metrics_table.append(['F1 Score', f1])
        metrics_table.append(['Classification Report', classification_report(y_test, predictions)])

    else:
        raise ValueError('Invalid test type. Choose between regression and classification')

    print(tabulate(metrics_table, headers=['Metric', 'Value'], tablefmt='pretty'))
    
