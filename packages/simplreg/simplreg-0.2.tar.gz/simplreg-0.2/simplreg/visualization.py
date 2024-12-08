import matplotlib.pyplot as plt
import seaborn as sns

def plot_feature_importance(model, feature_names):
    """Plot the feature importance for tree based model"""
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        sns.barplot(x=importance, y=feature_names)
        sns.title('Feature Importance')
        sns.show()
    else:
        raise AttributeError('Model does not have feature_importances_ attribute')


