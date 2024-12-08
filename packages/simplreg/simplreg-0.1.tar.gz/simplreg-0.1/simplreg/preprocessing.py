from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

def preprocess_data(df, target_column):
    # Fill missing values
    imputer = SimpleImputer(strategy='mean')
    df.iloc[:, :-1] = imputer.fit_transform(df.iloc[:, :-1])
    
    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
